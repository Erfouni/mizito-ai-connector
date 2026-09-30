#!/usr/bin/env bash
# Mizito AI Connector: one-command installer for an Ubuntu / Debian server.
#
#   git clone https://github.com/Erfouni/mizito-ai-connector.git
#   cd mizito-ai-connector
#   sudo bash deploy/install.sh            # install, or update after `git pull`
#   sudo bash deploy/install.sh url        # show your connector address again
#
# It asks two things only: the domain that points to this server, and your Mizito login.
# Everything else is automatic: Python environment, background service, HTTPS certificate, nginx and
# the secret connector address. Running it again keeps your settings and updates the code.
#
# Answers can also be given as environment variables (then nothing is asked):
#   MIZITO_DOMAIN, and MIZITO_TOKEN or MIZITO_USERNAME + MIZITO_PASSWORD (+ MIZITO_LOGIN_CODE)
# Optional: LETSENCRYPT_EMAIL, PIP_INDEX_URL (a PyPI mirror if pypi.org is blocked),
#   MIZITO_ENABLE_WRITE=0 (read-only), MIZITO_ENABLE_CRM=1, MIZITO_ENABLE_ADMIN=1,
#   MIZITO_SKIP_TLS=1 (no nginx/HTTPS: for tests or when you run your own reverse proxy).
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/mizito-mcp}"
APP_USER="${APP_USER:-mizito-mcp}"
SERVICE="${SERVICE:-mizito-mcp}"
PORT="${MCP_PORT:-8765}"
SKIP_TLS="${MIZITO_SKIP_TLS:-0}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$APP_DIR/.env"
NGINX_SITE="${NGINX_SITE:-mizito}"
SITE="/etc/nginx/sites-available/$NGINX_SITE"
WEBROOT="/var/www/letsencrypt"

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
ok()   { printf '    \033[32m%s\033[0m\n' "$*"; }
warn() { printf '    \033[33m%s\033[0m\n' "$*"; }
die()  { printf '\n\033[1;31mERROR: %s\033[0m\n\n' "$*" >&2; exit 1; }

ask() {  # ask VAR "question"   (skipped when VAR is already set, e.g. from the environment)
    local var="$1" question="$2" reply
    [ -n "${!var:-}" ] && return 0
    [ -r /dev/tty ] || die "$var is not set and there is no terminal to ask for it"
    read -r -p "    $question: " reply </dev/tty
    printf -v "$var" '%s' "$reply"
}

ask_secret() {  # like ask, without echoing what is typed
    local var="$1" question="$2" reply
    [ -n "${!var:-}" ] && return 0
    [ -r /dev/tty ] || die "$var is not set and there is no terminal to ask for it"
    read -r -s -p "    $question: " reply </dev/tty
    echo >/dev/tty
    printf -v "$var" '%s' "$reply"
}

env_get() {  # value of KEY in the .env file, without quotes
    [ -f "$ENV_FILE" ] || return 0
    sed -n "s/^$1=//p" "$ENV_FILE" | tail -n 1 | sed -e "s/^'\(.*\)'\$/\1/" -e 's/^"\(.*\)"$/\1/'
}

connector_url() {
    local domain path
    domain="$(env_get MCP_PUBLIC_HOST)"
    path="$(env_get MCP_HTTP_PATH)"
    if [ -n "$domain" ]; then echo "https://$domain$path"; else echo "http://127.0.0.1:$PORT$path"; fi
}

mcp_call() {  # mcp_call '<json-rpc body>' [base url]  -> response body
    curl -sS --max-time 90 -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
        -d "$1" "${2:-http://127.0.0.1:$PORT}$(env_get MCP_HTTP_PATH)"
}

pick_python() {  # the newest python >= 3.11 on this machine
    local p
    for p in python3.13 python3.12 python3.11 python3; do
        if command -v "$p" >/dev/null 2>&1 && "$p" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
            echo "$p"
            return 0
        fi
    done
    return 1
}

[ "$(id -u)" -eq 0 ] || die "Run it as root:  sudo bash deploy/install.sh"
if [ "${1:-}" = "url" ]; then
    [ -f "$ENV_FILE" ] || die "Not installed yet: run  sudo bash deploy/install.sh"
    connector_url
    exit 0
fi
command -v apt-get >/dev/null 2>&1 || die "This installer supports Ubuntu / Debian (apt-get)."
if [ ! -f "$REPO_DIR/server.py" ] || [ ! -d "$REPO_DIR/mizito" ]; then
    die "Run it from the downloaded repository: sudo bash deploy/install.sh"
fi

cat <<'EOF'

  Mizito AI Connector installer
  Connects your Mizito account to Claude.ai and ChatGPT through this server.
EOF

# ---------------------------------------------------------------------------------------------------
say "1/7  Settings"
NEW_ENV=0
if [ -f "$ENV_FILE" ]; then
    DOMAIN="$(env_get MCP_PUBLIC_HOST)"
    ok "Keeping your settings in $ENV_FILE (edit that file to change them)"
    [ "$SKIP_TLS" = 1 ] || [ -n "$DOMAIN" ] || die "MCP_PUBLIC_HOST (your domain) is missing in $ENV_FILE"
else
    NEW_ENV=1
    DOMAIN="${MIZITO_DOMAIN:-}"
    if [ "$SKIP_TLS" != 1 ]; then
        ask DOMAIN "Domain that points to this server, e.g. mcp.example.com"
        DOMAIN="$(printf '%s' "$DOMAIN" | tr '[:upper:]' '[:lower:]' | sed -e 's#^https\?://##' -e 's#/.*$##')"
        [[ "$DOMAIN" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$ ]] || die "\"$DOMAIN\" is not a valid domain name"
    fi
    echo "    Mizito login: paste your token (see the guide), or just press Enter to use username + password."
    ask_secret MIZITO_TOKEN "Mizito token"
    if [ -z "${MIZITO_TOKEN:-}" ]; then
        ask MIZITO_USERNAME "Mizito username (mobile number or email)"
        ask_secret MIZITO_PASSWORD "Mizito password"
        if [ -z "${MIZITO_USERNAME:-}" ] || [ -z "${MIZITO_PASSWORD:-}" ]; then
            die "Give a token, or a username and password"
        fi
    fi
fi

# ---------------------------------------------------------------------------------------------------
say "2/7  Checking this server"
curl -sS -o /dev/null --max-time 20 https://app.mizito.ir 2>/dev/null \
    || die "This server cannot reach app.mizito.ir. Use a server that can open Mizito (for example one in Iran)."
ok "Mizito is reachable"
if [ "$SKIP_TLS" != 1 ] && [ -n "$DOMAIN" ]; then
    if getent ahosts "$DOMAIN" >/dev/null 2>&1; then
        ok "$DOMAIN resolves to $(getent ahostsv4 "$DOMAIN" | awk 'NR==1 {print $1}')"
    else
        die "$DOMAIN does not resolve yet. Create an A record for it with this server's IP, wait a few minutes, then run again."
    fi
fi

# ---------------------------------------------------------------------------------------------------
say "3/7  System packages"
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_SUSPEND=1  # no service-restart prompts from apt
apt-get update -qq
PACKAGES=(python3 python3-venv curl ca-certificates)
[ "$SKIP_TLS" = 1 ] || PACKAGES+=(nginx certbot)
apt-get install -y -qq "${PACKAGES[@]}" >/dev/null
PY="$(pick_python)" || { apt-get install -y -qq python3.11 python3.11-venv >/dev/null 2>&1 && PY=python3.11; } \
    || die "Python 3.11 or newer is needed (use Ubuntu 24.04 or Debian 12)"
"$PY" -c 'import venv, ensurepip' 2>/dev/null || apt-get install -y -qq "$(basename "$PY")-venv" >/dev/null 2>&1 || true
ok "$($PY --version)"

# ---------------------------------------------------------------------------------------------------
say "4/7  Installing the connector into $APP_DIR"
id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home-dir "$APP_DIR" --no-create-home --shell /usr/sbin/nologin "$APP_USER"
install -d -o root -g "$APP_USER" -m 750 "$APP_DIR" "$APP_DIR/mizito"
if [ -f "$APP_DIR/server.py" ]; then  # keep the previous version to roll back to
    BACKUP="$APP_DIR/backup/$(date +%Y%m%d-%H%M%S)"
    install -d -m 700 "$BACKUP"
    cp -a "$APP_DIR/server.py" "$APP_DIR/mizito_client.py" "$APP_DIR/mizito" "$BACKUP/" 2>/dev/null || true
    rm -f "$APP_DIR"/mizito/*.py
    ok "Previous version saved in $BACKUP"
fi
install -o root -g "$APP_USER" -m 640 "$REPO_DIR/server.py" "$REPO_DIR/mizito_client.py" "$REPO_DIR/pyproject.toml" "$APP_DIR/"
install -o root -g "$APP_USER" -m 640 "$REPO_DIR"/mizito/*.py "$APP_DIR/mizito/"
install -o root -g "$APP_USER" -m 640 "$REPO_DIR/deploy/requirements.txt" "$APP_DIR/requirements.txt"
[ -x "$APP_DIR/.venv/bin/python" ] || "$PY" -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install -q --disable-pip-version-check --require-hashes -r "$APP_DIR/requirements.txt" \
    || die "Installing Python packages failed. If pypi.org is blocked here, run again with a mirror:
       sudo PIP_INDEX_URL=https://<mirror>/simple bash deploy/install.sh"
chown -R root:"$APP_USER" "$APP_DIR/.venv"
chmod -R o-rwx "$APP_DIR"
ok "Code and Python packages installed"

# ---------------------------------------------------------------------------------------------------
say "5/7  Service"
if [ "$NEW_ENV" = 1 ]; then  # written by Python so any character in a password is stored safely
    export MIZITO_TOKEN="${MIZITO_TOKEN:-}" MIZITO_USERNAME="${MIZITO_USERNAME:-}" MIZITO_PASSWORD="${MIZITO_PASSWORD:-}"
    export MIZITO_LOGIN_CODE="${MIZITO_LOGIN_CODE:-}" DOMAIN PORT SERVICE ENV_FILE
    (umask 077 && "$PY" - <<'PYEOF'
import os
import secrets

def quoted(value: str) -> str:  # single-quoted the way python-dotenv reads it back
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"

env = os.environ
lines = [
    f"# Written by deploy/install.sh. After editing: sudo systemctl restart {env['SERVICE']}",
    f"MIZITO_TOKEN={quoted(env['MIZITO_TOKEN'])}",
    f"MIZITO_USERNAME={quoted(env['MIZITO_USERNAME'])}",
    f"MIZITO_PASSWORD={quoted(env['MIZITO_PASSWORD'])}",
    f"MIZITO_LOGIN_CODE={quoted(env['MIZITO_LOGIN_CODE'])}",
    f"MIZITO_ENABLE_WRITE={env.get('MIZITO_ENABLE_WRITE', '1')}",
    f"MIZITO_ENABLE_CRM={env.get('MIZITO_ENABLE_CRM', '0')}",
    f"MIZITO_ENABLE_ADMIN={env.get('MIZITO_ENABLE_ADMIN', '0')}",
    "MCP_TRANSPORT=streamable-http",
    "MCP_HOST=127.0.0.1",
    f"MCP_PORT={env['PORT']}",
    f"MCP_HTTP_PATH=/mcp-{secrets.token_urlsafe(32)}",
    f"MCP_PUBLIC_HOST={env['DOMAIN']}",
]
with open(env["ENV_FILE"], "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
PYEOF
    )
fi
chown "$APP_USER:$APP_USER" "$ENV_FILE"
chmod 600 "$ENV_FILE"
PORT="$(env_get MCP_PORT)"
PORT="${PORT:-8765}"
sed -e "s#/opt/mizito-mcp#$APP_DIR#g" -e "s#^User=.*#User=$APP_USER#" -e "s#^Group=.*#Group=$APP_USER#" \
    "$REPO_DIR/deploy/mizito-mcp.service" >"/etc/systemd/system/$SERVICE.service"
systemctl daemon-reload
systemctl enable "$SERVICE" >/dev/null 2>&1
systemctl restart "$SERVICE"
for _ in $(seq 1 30); do
    mcp_call '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' >/dev/null 2>&1 && break
    sleep 1
done
systemctl is-active --quiet "$SERVICE" || { journalctl -u "$SERVICE" -n 25 --no-pager; die "The service did not start"; }
CHECK="$(mcp_call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mizito_whoami","arguments":{}}}' || true)"
RESULT="$(printf '%s' "$CHECK" | "$PY" -c '
import json, sys
try:
    r = json.load(sys.stdin)["result"]
except Exception:
    print("ERROR no answer from the service"); sys.exit()
text = " ".join(c.get("text", "") for c in r.get("content", []))
if r.get("isError"):
    print("ERROR " + text[:300])
else:
    data = r.get("structuredContent") or json.loads(text)
    print("OK " + str(data.get("user_name")) + " / workspace " + str(data.get("workspaces", [{}])[0].get("title")))
')"
case "$RESULT" in
    OK*) ok "Connected to Mizito as ${RESULT#OK }" ;;
    *) warn "${RESULT#ERROR }"
       die "The service runs, but Mizito refused the login. Put a fresh token in $ENV_FILE and run:  sudo systemctl restart $SERVICE" ;;
esac
TOOLS="$(mcp_call '{"jsonrpc":"2.0","id":3,"method":"tools/list"}' | "$PY" -c 'import json,sys; print(len(json.load(sys.stdin)["result"]["tools"]))' 2>/dev/null || echo "?")"
ok "$TOOLS tools available"

# ---------------------------------------------------------------------------------------------------
if [ "$SKIP_TLS" = 1 ]; then
    say "6/7  HTTPS skipped (MIZITO_SKIP_TLS=1)"
    say "7/7  nginx skipped"
else
    say "6/7  HTTPS certificate for $DOMAIN"
    install -d "$WEBROOT"
    IPV6=1
    [ -f /proc/net/if_inet6 ] || IPV6=0
    CERT_DIR="/etc/letsencrypt/live/$DOMAIN"
    systemctl enable --now nginx >/dev/null 2>&1 || true
    if command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep -q "Status: active"; then
        ufw allow 80/tcp >/dev/null && ufw allow 443/tcp >/dev/null && ok "Opened ports 80 and 443 in the ufw firewall"
    fi
    if [ ! -f "$CERT_DIR/fullchain.pem" ]; then
        cat >"$SITE" <<EOF
server {
    listen 80;
$([ "$IPV6" = 1 ] && echo "    listen [::]:80;")
    server_name $DOMAIN;
    location /.well-known/acme-challenge/ { root $WEBROOT; }
    location / { return 404; }
}
EOF
        ln -sf "$SITE" "/etc/nginx/sites-enabled/$NGINX_SITE"
        nginx -t -q && systemctl reload nginx
        echo "    Requesting a free Let's Encrypt certificate (you accept their terms: https://letsencrypt.org/repository/)"
        CERTBOT=(certonly --webroot -w "$WEBROOT" -d "$DOMAIN" --non-interactive --agree-tos
                 --deploy-hook "systemctl reload nginx")
        if [ -n "${LETSENCRYPT_EMAIL:-}" ]; then CERTBOT+=(--email "$LETSENCRYPT_EMAIL"); else CERTBOT+=(--register-unsafely-without-email); fi
        certbot "${CERTBOT[@]}" || die "No certificate. Check that $DOMAIN points to this server and that port 80 is open to the internet
       (some Iranian servers cannot reach Let's Encrypt: see Troubleshooting in SETUP.md)."
        ok "Certificate issued; it renews automatically"
    else
        ok "Certificate already present"
    fi

    say "7/7  nginx (HTTPS)"
    sed -e "s#mcp.example.com#$DOMAIN#g" -e "s#127.0.0.1:8765#127.0.0.1:$PORT#g" \
        -e "s#/var/www/letsencrypt#$WEBROOT#g" "$REPO_DIR/deploy/nginx.conf.example" >"$SITE"
    [ "$IPV6" = 1 ] || sed -i '/listen \[::\]/d' "$SITE"
    ln -sf "$SITE" "/etc/nginx/sites-enabled/$NGINX_SITE"
    nginx -t -q || die "nginx rejected the configuration in $SITE"
    systemctl reload nginx
    if mcp_call '{"jsonrpc":"2.0","id":4,"method":"tools/list"}' "https://$DOMAIN" 2>/dev/null | grep -q '"tools"'; then
        ok "https://$DOMAIN answers"
    else
        warn "https://$DOMAIN did not answer from this server itself; check the firewall (ports 80 and 443) if it also fails from outside"
    fi
fi

# ---------------------------------------------------------------------------------------------------
cat <<EOF

  Done. Your connector address (keep it secret: it works like a password):

      $(connector_url)

  Claude.ai: Settings > Connectors > Add custom connector > paste the address (no OAuth).
  ChatGPT:   Settings > Apps & Connectors > Advanced > Developer mode on > Create > paste the address,
             Authentication: No authentication.
  Update later:  git pull && sudo bash deploy/install.sh   (then Refresh the connector in ChatGPT)
  Show the address again:  sudo bash deploy/install.sh url

EOF
