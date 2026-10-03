"""Log in to Mizito and check that it works; with --save, keep the login for the server.

    uv run python check_login.py                         # only check: nothing is saved
    python check_login.py --save /opt/mizito-mcp/.env    # check and save (install.sh and
                                                         # `mizito-connector login` run this)

Asks for your Mizito username (mobile number or email) and password; the password is not shown while
you type. If the account uses two-step login, it also asks for the code Mizito sends by SMS. To use a
token instead (localStorage.token in the Mizito web app), leave the username empty.

With --save, the login goes into that .env file and every other line in it is kept:
  - username + password (and the current token): the server logs in again by itself when needed;
  - with two-step login or a pasted token, only the token: when it expires, log in again.
Without a terminal, the login comes from MIZITO_USERNAME + MIZITO_PASSWORD, or MIZITO_TOKEN.
"""
from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mizito_client import MizitoAuthError, MizitoClient, MizitoCodeRequired, MizitoError, to_ascii_digits  # noqa: E402

ATTEMPTS = 3


def quoted(value: str) -> str:
    """Single-quoted the way python-dotenv reads it back, so any character in a password is safe."""
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def save_env(path: Path, values: dict[str, str]) -> None:
    """Set these keys in the .env file and keep every other line; the file is rewritten with mode 600."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    out, done = [], set()
    for line in lines:
        key = line.split("=", 1)[0].strip()
        if "=" in line and key in values:
            if key not in done:
                out.append(f"{key}={quoted(values[key])}")
                done.add(key)
            continue
        out.append(line)
    out += [f"{key}={quoted(value)}" for key, value in values.items() if key not in done]
    tmp = path.with_name(path.name + ".tmp")
    tmp.unlink(missing_ok=True)
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    os.replace(tmp, path)


def answers():
    """(username, password, token) to try: the environment first, then what is typed in."""
    user, password, token = (os.getenv(k, "") for k in ("MIZITO_USERNAME", "MIZITO_PASSWORD", "MIZITO_TOKEN"))
    if token or (user and password):
        yield user, password, token
    if not sys.stdin.isatty():
        return
    for _ in range(ATTEMPTS):
        user = input("Mizito username (mobile number or email): ").strip()
        if user:
            yield user, getpass.getpass("Mizito password (hidden while you type): "), ""
        else:
            yield "", "", getpass.getpass("No username: paste a Mizito token instead (hidden): ").strip()


def log_in(user: str, password: str, token: str) -> tuple[MizitoClient, bool]:
    """A logged-in client, and whether the account uses two-step login. Raises MizitoAuthError."""
    if not (user and password):
        if not token:
            raise MizitoAuthError("Give a username and password, or a token.")
        client = MizitoClient(token=token)
        try:
            client.call("workspace.userId", {})
        except MizitoAuthError:  # 401
            raise MizitoAuthError("Mizito did not accept this token.") from None
        return client, False
    client = MizitoClient(username=user, password=password)
    try:
        client.login()
        return client, False
    except MizitoCodeRequired:
        if not sys.stdin.isatty():
            raise MizitoAuthError(
                "This account uses two-step login: run this in a terminal to type the SMS code, or use MIZITO_TOKEN."
            ) from None
        print("Two-step login: Mizito has sent you a code by SMS.")
    for _ in range(ATTEMPTS):
        code = to_ascii_digits(input("Code from the SMS: ").strip())
        client = MizitoClient(username=user, password=password, login_code=code)
        try:
            client.login()
            return client, True
        except MizitoCodeRequired:
            print("Mizito did not accept that code. Type it again, or the newest code if another SMS came.")
    raise MizitoAuthError("The SMS code was not accepted.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Log in to Mizito and check that it works.")
    parser.add_argument("--save", metavar="ENV_FILE", type=Path, help="save the working login in this .env file")
    args = parser.parse_args()
    print("Mizito login" if args.save else "Mizito login check (nothing is saved)")

    client = None
    for user, password, token in answers():
        try:
            client, two_step = log_in(user, password, token)
            break
        except MizitoAuthError as exc:
            print(f"  Not accepted: {exc}")
        except MizitoError as exc:  # network trouble: typing the login again would not help
            print(f"FAILED: {exc}")
            return 1
    if client is None:
        print("FAILED: Mizito did not accept the login.")
        return 1

    info = client.call("workspace.userId", {}) or {}
    workspace = next((w.get("title") for w in info.get("workspaces") or [] if w.get("active")), info.get("wid"))
    print(f"OK: logged in as {client.user_name(info.get('uid'))} (workspace: {workspace}).")
    keep_password = bool(user and password) and not two_step
    if not args.save:
        if keep_password:
            print("Username + password login works: the connector can renew its session by itself.")
        print("(This test opened one Mizito session; you can end it in Mizito under Profile > Security.)")
        return 0

    save_env(args.save, {
        "MIZITO_TOKEN": client.token or "",
        "MIZITO_USERNAME": user if keep_password else "",
        "MIZITO_PASSWORD": password if keep_password else "",
        "MIZITO_LOGIN_CODE": "",
    })
    if keep_password:
        print("Saved: the server logs in again by itself whenever its Mizito session ends.")
    elif two_step:
        print("Saved. With two-step login the server cannot log in again by itself: if the connector")
        print("stops working one day, run  mizito-connector login  again.")
    else:
        print("Saved the token. When it expires, run  mizito-connector login  again.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
