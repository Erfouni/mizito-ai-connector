"""Check that Mizito accepts a username + password login. Nothing is saved.

usage: uv run python check_login.py

Asks for your Mizito username and password (the password is not shown while you type), logs in once
and reports whether it worked. If it does, MIZITO_USERNAME / MIZITO_PASSWORD in .env will keep the
connector logged in by itself, even after the token expires.
"""
import getpass
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mizito_client import MizitoClient, MizitoError  # noqa: E402

print("Mizito username + password check (nothing is saved)\n")
username = input("Mizito username (mobile number or email): ").strip()
password = getpass.getpass("Mizito password (hidden while you type): ")
code = input("Two-step login code, only if you use two-step login (otherwise just Enter): ").strip() or None
if not username or not password:
    sys.exit("Username and password are both needed.")

client = MizitoClient(username=username, password=password, login_code=code)
try:
    client.login()
    info = client.call("workspace.userId", {}) or {}
except MizitoError as exc:
    print(f"\nFAILED: {exc}")
    sys.exit(1)

workspace = next((w.get("title") for w in info.get("workspaces") or [] if w.get("active")), info.get("wid"))
print(f"\nOK: logged in as {client.user_name(info.get('uid'))} (workspace: {workspace}).")
print("Username + password login works: the connector can renew its session by itself.")
print("(This test opened one extra Mizito session; you can end it under Profile > Security > Sessions.)")
