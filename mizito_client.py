"""Thin client for Mizito's internal web API (reverse-engineered from office.mizito.ir).

Every call is `POST {api_url}/api/<module>/<method>` with a JSON body and an
`x-token` header, e.g. `chat.getHistory` -> `/api/chat/getHistory`.
Login is `POST {api_url}/capi/session/create`. The token is scoped to one
workspace; `workspace.switch` returns a new token for another workspace.
"""
from __future__ import annotations

import hashlib
import html
import os
import re
import threading
from typing import Any

import httpx

try:  # surface our messages to the model instead of a generic "Error executing tool"
    from mcp.server.mcpserver.exceptions import ToolError as _Base
except ImportError:  # pragma: no cover - client used without the MCP SDK
    _Base = RuntimeError

DEFAULT_API_URL = "https://app.mizito.ir"


class MizitoError(_Base):
    pass


class MizitoAuthError(MizitoError):
    pass


class MizitoCodeRequired(MizitoAuthError):
    """Two-step login: Mizito has sent a code by SMS; log in again with it as login_code."""


def hash_password(password: str) -> str:
    """Same scheme as the web app: md5(pw) + "|" + sha256(pw), both hex."""
    raw = password.encode("utf-8")
    return hashlib.md5(raw).hexdigest() + "|" + hashlib.sha256(raw).hexdigest()


_ASCII_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def to_ascii_digits(text: str) -> str:
    """Persian and Arabic digits to 0-9, as the web login form does for the username, password and code."""
    return text.translate(_ASCII_DIGITS)


def login_username(username: str) -> str:
    """The username as the web login form sends it: a mobile number typed as 9121234567 or
    989121234567 gets its leading 0 or +."""
    name = to_ascii_digits(username.strip())
    if name.isdigit() and len(name) == 10:
        return "0" + name
    if name.isdigit() and len(name) == 12:
        return "+" + name
    return name


# capi/session/create answers other than success (status 1 or 5), as the web login form reads them.
# Status 7 means two-step login (MizitoCodeRequired); anything else is a wrong username or password.
_LOGIN_REFUSED = {
    6: "too many login attempts; Mizito accepts no new login for a few hours",
    8: "too many open Mizito sessions; end some in Mizito under Profile > Security",
}


_BLOCK_TAGS = re.compile(r"(?i)<\s*(br|/div|/p|/li)\s*/?>")
_TAGS = re.compile(r"<[^>]+>")


def html_to_text(value: Any) -> str:
    """Mizito stores message bodies as HTML; flatten to plain text."""
    if not value:
        return ""
    text = _BLOCK_TAGS.sub("\n", str(value))
    text = html.unescape(_TAGS.sub("", text)).replace("\xa0", " ")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# Task access tokens are JWTs that embed the user's session token in plain base64, so any
# JWT-looking value is kept out of tool results.
_SECRET_KEYS = {"access_token", "token", "x-token"}
_JWT = re.compile(r"eyJ[\w-]+\.[\w-]+\.[\w-]+")


def compact(value: Any, max_str: int = 4000) -> Any:
    """Drop empty fields, secrets and truncate huge strings so tool results stay small and safe."""
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if key in _SECRET_KEYS:
                continue
            item = compact(item, max_str)
            if item is None or item == "" or item == [] or item == {}:
                continue
            out[key] = item
        return out
    if isinstance(value, list):
        return [compact(item, max_str) for item in value]
    if isinstance(value, str):
        value = _JWT.sub("<redacted>", value)
        if len(value) > max_str:
            return value[:max_str] + "…"
    return value


class MizitoClient:
    def __init__(
        self,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        login_code: str | None = None,
        api_url: str = DEFAULT_API_URL,
        timeout: float = 30.0,
    ):
        self.api_url = api_url.rstrip("/")
        self.token = token or None
        self._username = username or None
        self._password = password or None
        self._login_code = login_code or None
        self._login_refused: str | None = None
        self._lock = threading.Lock()
        self._http = httpx.Client(timeout=timeout, headers={"Accept": "application/json, text/plain, */*"})
        self._users: dict[str, str] | None = None
        self._dialog_titles: dict[str, str] = {}
        self._my_id: str | None = None

    @classmethod
    def from_env(cls) -> "MizitoClient":
        return cls(
            token=os.getenv("MIZITO_TOKEN"),
            username=os.getenv("MIZITO_USERNAME"),
            password=os.getenv("MIZITO_PASSWORD"),
            login_code=os.getenv("MIZITO_LOGIN_CODE"),
            api_url=os.getenv("MIZITO_API_URL", DEFAULT_API_URL),
        )

    # --- auth -------------------------------------------------------------

    @property
    def can_login(self) -> bool:
        return bool(self._username and self._password)

    def login(self) -> dict:
        if not self.can_login:
            raise MizitoAuthError("MIZITO_USERNAME / MIZITO_PASSWORD are not set.")
        try:
            resp = self._http.post(
                f"{self.api_url}/capi/session/create",
                json={
                    "username": login_username(self._username),
                    "password": hash_password(to_ascii_digits(self._password)),
                    "loginCode": to_ascii_digits(self._login_code) if self._login_code else None,
                    "regId": None,
                },
            )
        except httpx.HTTPError as exc:
            raise MizitoError(f"login -> network error talking to Mizito: {exc!r}") from exc
        try:
            data = resp.json()
        except ValueError:
            data = None
        if isinstance(data, dict) and data.get("blocked"):
            raise MizitoAuthError("Mizito login refused: the workspace admin has restricted your access.")
        if resp.status_code >= 400 or not isinstance(data, dict):
            raise MizitoError(f"login -> HTTP {resp.status_code}: Mizito did not answer the login normally")
        status = data.get("status")
        if status in (1, 5) and data.get("token"):
            self.token = data["token"]
            self._clear_caches()
            return data
        if status == 7 and not data.get("too_attempts"):
            raise MizitoCodeRequired("This account uses two-step login: Mizito has sent a code by SMS.")
        reason = _LOGIN_REFUSED.get(status) or (
            "too many attempts; try again later" if data.get("too_attempts") else "wrong username or password"
        )
        raise MizitoAuthError(f"Mizito login failed: {reason} (status {status!r}).")

    def _relogin(self) -> None:
        """Log in with the saved password. Once Mizito refuses it, it is not tried again until the server
        restarts: retrying a wrong password, or a two-step login, would only lock the account or send SMS."""
        if self._login_refused:
            raise MizitoAuthError(self._login_refused)
        try:
            self.login()
        except MizitoAuthError as exc:
            self._login_refused = f"{exc} Log in again: run `mizito-connector login` on the server (or update .env)."
            raise MizitoAuthError(self._login_refused) from exc

    # --- transport ----------------------------------------------------------

    def _post(self, endpoint: str, payload: dict | None) -> httpx.Response:
        return self._http.post(
            f"{self.api_url}/api/{endpoint.replace('.', '/')}",
            json=payload or {},
            headers={"x-token": self.token or ""},
        )

    def _send(self, endpoint: str, request) -> httpx.Response:
        """Run request() with the current token, logging in first / again on 401 when credentials allow."""
        with self._lock:
            if not self.token:
                if not self.can_login:
                    raise MizitoAuthError(
                        "No credentials: set MIZITO_TOKEN (or MIZITO_USERNAME/MIZITO_PASSWORD) in .env"
                    )
                self._relogin()
            try:
                resp = request()
                if resp.status_code == 401 and self.can_login:
                    self._relogin()
                    resp = request()
            except httpx.HTTPError as exc:
                raise MizitoError(f"{endpoint} -> network error talking to Mizito: {exc!r}") from exc
        return resp

    def upload(self, file_name: str, data: bytes, mime_type: str, send_as_file: bool = True) -> Any:
        """Upload a file like the web uploader: multipart field "upload" to /api/content/upload.
        Returns the media object (e.g. {"_": "messageMediaDocument", "document": {...}})."""
        def request() -> httpx.Response:
            return self._http.post(
                f"{self.api_url}/api/content/upload",
                headers={"x-token": self.token or ""},
                files={"upload": (file_name, data, mime_type)},
                data={"sendAsFile": "true" if send_as_file else "false"},
                timeout=180.0,
            )

        return self._decode("content.upload", self._send("content.upload", request))

    def fetch(self, url: str, max_bytes: int) -> tuple[bytes, str | None]:
        """Download a CDN file link (the link itself grants access; no session token is sent)."""
        try:
            with self._http.stream("GET", url, timeout=180.0) as resp:
                if resp.status_code >= 400:
                    raise MizitoError(f"file download -> HTTP {resp.status_code}")
                chunks, size = [], 0
                for chunk in resp.iter_bytes():
                    size += len(chunk)
                    if size > max_bytes:
                        raise MizitoError(f"file is larger than {max_bytes // 1_000_000} MB")
                    chunks.append(chunk)
                return b"".join(chunks), resp.headers.get("content-type")
        except httpx.HTTPError as exc:
            raise MizitoError(f"file download -> network error: {exc!r}") from exc

    def call(self, endpoint: str, payload: dict | None = None) -> Any:
        return self._decode(endpoint, self._send(endpoint, lambda: self._post(endpoint, payload)))

    def _decode(self, endpoint: str, resp: httpx.Response) -> Any:
        if resp.status_code == 401:
            raise MizitoAuthError(
                "Mizito rejected the saved login (401): the token expired or was revoked. "
                "Log in again: run `mizito-connector login` on the server (or put a fresh MIZITO_TOKEN in .env)."
            )
        if resp.status_code >= 400:
            detail = "HTML error page" if "html" in resp.headers.get("content-type", "") else resp.text[:300]
            raise MizitoError(f"{endpoint} -> HTTP {resp.status_code} ({detail}); wrong parameters or no access")
        try:
            data = resp.json() if resp.content else None
        except ValueError:  # a few endpoints (print views) answer with plain HTML
            data = resp.text
        if isinstance(data, dict) and data.get("db_error"):
            raise MizitoError(f"{endpoint} -> server reported db_error")
        return data

    # --- workspace ----------------------------------------------------------

    def switch_workspace(self, workspace_id: str) -> dict:
        data = self.call("workspace.switch", {"workspace_id": workspace_id}) or {}
        if not data.get("token"):
            raise MizitoError("workspace.switch did not return a token")
        self.token = data["token"]
        self._clear_caches()
        return data

    def _clear_caches(self) -> None:
        self._users = None
        self._dialog_titles = {}
        self._my_id = None

    # --- lookups ------------------------------------------------------------

    def my_user_id(self) -> str:
        if not self._my_id:
            self._my_id = (self.call("workspace.userId", {}) or {}).get("uid")
        return self._my_id

    def users(self, refresh: bool = False) -> dict[str, str]:
        if refresh or self._users is None:
            data = self.call("workspace.getUsers", {}) or {}
            self._users = {
                u["_id"]: " ".join(p for p in (u.get("first_name"), u.get("last_name")) if p).strip() or u["_id"]
                for u in data.get("users", [])
            }
        return self._users

    def user_name(self, user_id: str | None) -> str | None:
        if not user_id:
            return None
        users = self.users()
        if user_id not in users:
            users = self.users(refresh=True)
        return users.get(user_id, user_id)

    def dialog_title(self, dialog: dict) -> str:
        dialog_id = dialog["_id"]
        if dialog.get("title"):
            return dialog["title"]
        if dialog.get("peer_user"):
            return self.user_name(dialog["peer_user"]) or dialog_id
        if dialog_id not in self._dialog_titles:
            full = self.call("chat.getFullChat", {"dialog": dialog_id}) or {}
            self._dialog_titles[dialog_id] = full.get("title") or dialog_id
        return self._dialog_titles[dialog_id]
