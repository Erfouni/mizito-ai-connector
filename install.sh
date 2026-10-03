#!/usr/bin/env bash
# Mizito AI Connector: install, update and manage it on an Ubuntu / Debian server.
#
# Install or update with one command (as root, or as a user who may use sudo):
#
#   curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | bash
#
# It asks for the domain that points to this server and for your Mizito username and password, and
# does everything else: Python, a background service, a free HTTPS certificate, nginx and a secret
# connector address. Running it again updates the code and keeps your settings.
#
# Afterwards the `mizito-connector` command manages it:
#   mizito-connector url       show the connector address again
#   mizito-connector status    check that everything works
#   mizito-connector login     log in to Mizito again (new password, or the login expired)
#   mizito-connector update    update to the latest version
#   mizito-connector logs      follow the service log
#
# In a downloaded copy of the repository, `sudo bash install.sh` installs that copy.
#
# Answers can also come from environment variables (then nothing is asked):
#   MIZITO_DOMAIN, and MIZITO_USERNAME + MIZITO_PASSWORD or MIZITO_TOKEN
# Optional: HTTPS_PROXY (if this server cannot reach Let's Encrypt), PIP_INDEX_URL (a PyPI mirror),
#   LETSENCRYPT_EMAIL, MIZITO_ENABLE_WRITE=0 (read-only), MIZITO_ENABLE_CRM=1, MIZITO_ENABLE_ADMIN=1,
#   MIZITO_SKIP_TLS=1 (no nginx/HTTPS, e.g. behind your own web server), MIZITO_SKIP_DNS_CHECK=1,
#   MIZITO_REF (branch or tag to download; default main).
set -euo pipefail

REPO="Erfouni/mizito-ai-connector"
INSTALL_CMD="curl -fsSL https://raw.githubusercontent.com/$REPO/main/install.sh | bash"
APP_DIR="${APP_DIR:-/opt/mizito-mcp}"
APP_USER="${APP_USER:-mizito-mcp}"
SERVICE="${SERVICE:-mizito-mcp}"
NGINX_SITE="${NGINX_SITE:-mizito}"
CLI="${MIZITO_CLI:-/usr/local/bin/mizito-connector}"
CLI_NAME="$(basename "$CLI")"
SKIP_TLS="${MIZITO_SKIP_TLS:-0}"
PORT="${MCP_PORT:-8765}"
ENV_FILE="$APP_DIR/.env"
VPY="$APP_DIR/.venv/bin/python"
SITE="/etc/nginx/sites-available/$NGINX_SITE"
WEBROOT="/var/www/letsencrypt"
LOG="/var/log/mizito-connector.log"
# Settings passed on when the script runs itself again through sudo.
SETTINGS=(APP_DIR APP_USER SERVICE NGINX_SITE MIZITO_CLI MIZITO_SKIP_TLS MCP_PORT MIZITO_DOMAIN MIZITO_USERNAME
          MIZITO_PASSWORD MIZITO_TOKEN HTTPS_PROXY https_proxy PIP_INDEX_URL LETSENCRYPT_EMAIL MIZITO_ENABLE_WRITE
          MIZITO_ENABLE_CRM MIZITO_ENABLE_ADMIN MIZITO_SKIP_DNS_CHECK MIZITO_REF)
# Tried in this order when pypi.org does not work; pip still checks every file against its hash.
PIP_MIRRORS=(https://mirror-pypi.runflare.com/simple https://package-mirror.liara.ir/repository/pypi/simple
             https://repo.hmirror.ir/python/simple)
# https://www.cloudflare.com/ips-v4
CLOUDFLARE_NETS="173.245.48.0/20 103.21.244.0/22 103.22.200.0/22 103.31.4.0/22 141.101.64.0/18 108.162.192.0/18
190.93.240.0/20 188.114.96.0/20 197.234.240.0/22 198.41.128.0/17 162.158.0.0/15 104.16.0.0/13 104.24.0.0/14
172.64.0.0/13 131.0.72.0/22"

# This file, and the code next to it when it is part of a downloaded repository. Both are empty when
# the script comes from `curl | bash`; CODE_DIR is empty for the installed mizito-connector copy too.
SELF="${BASH_SOURCE[0]:-}"
CODE_DIR=""
if [ -n "$SELF" ] && [ -f "$SELF" ]; then
    SELF="$(cd "$(dirname "$SELF")" && pwd)/$(basename "$SELF")"
    _dir="$(dirname "$SELF")"
    if [ -f "$_dir/server.py" ] && [ -d "$_dir/mizito" ] && [ -f "$_dir/deploy/mizito-mcp.service" ]; then
        CODE_DIR="$_dir"
    fi
else
    SELF=""
fi

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
ok()   { printf '    \033[32m%s\033[0m\n' "$*"; }
warn() { printf '    \033[33m%s\033[0m\n' "$*"; }
die()  { printf '\n\033[1;31mERROR: %s\033[0m\n\n' "$*" >&2; exit 1; }
quiet() { "$@" >>"$LOG" 2>&1; }                                     # output only to the log file
log_tail() { tail -n "${1:-12}" "$LOG" | sed 's/^/    | /' >&2; }  # show the end of the log file
has_tty() { { : </dev/tty; } 2>/dev/null; }                         # can questions be asked?

ask() {  # ask VAR "question" ["default"]   (skipped when VAR is already set, e.g. from the environment)
    local var="$1" question="$2" default="${3:-}" reply
    [ -n "${!var:-}" ] && return 0
    has_tty || die "$var is not set and there is no terminal to ask for it"
    if [ -n "$default" ]; then question="$question [$default]"; fi
    read -r -p "    $question: " reply </dev/tty
    printf -v "$var" '%s' "${reply:-$default}"
}

as_root() {  # as_root COMMAND...: run it as root (through sudo if needed) in place of this script
    if [ "$(id -u)" -eq 0 ]; then exec "$@"; fi
    command -v sudo >/dev/null 2>&1 || die "Run this as root."
    local keep=() name
    for name in "${SETTINGS[@]}"; do
        if [ -n "${!name:-}" ]; then keep+=("$name"); fi
    done
    if [ "${#keep[@]}" -gt 0 ]; then exec sudo "--preserve-env=$(IFS=,; echo "${keep[*]}")" "$@"; fi
    exec sudo "$@"
}

need_root() {  # need_root ARGS...: this script again as root, with the same arguments
    [ "$(id -u)" -eq 0 ] && return 0
    [ -n "$SELF" ] || die "Run this as root."
    as_root bash "$SELF" "$@"
}

download() {  # the code from GitHub into a new temporary directory -> CODE_DIR
    local ref="${MIZITO_REF:-main}"
    CODE_DIR="$(mktemp -d /tmp/mizito-connector.XXXXXX)"
    echo "    Downloading the connector from github.com/$REPO ($ref) ..."
    if ! curl -fsSL --retry 2 --connect-timeout 20 --max-time 300 "https://github.com/$REPO/archive/$ref.tar.gz" \
            | tar -xz -C "$CODE_DIR" --strip-components=1; then
        rm -rf "$CODE_DIR"
        die "Could not download the code from GitHub. Check this server's internet access, then run the command again."
    fi
    [ -f "$CODE_DIR/install.sh" ] || die "The download from GitHub was incomplete. Run the command again."
}

env_get() {  # value of KEY in the .env file, without quotes
    [ -f "$ENV_FILE" ] || return 0
    sed -n "s/^$1=//p" "$ENV_FILE" | tail -n 1 | sed -e "s/^'\(.*\)'\$/\1/" -e 's/^"\(.*\)"$/\1/'
}

env_set() {  # env_set KEY VALUE, for plain values (a domain, a number)
    if grep -q "^$1=" "$ENV_FILE"; then sed -i "s#^$1=.*#$1=$2#" "$ENV_FILE"; else echo "$1=$2" >>"$ENV_FILE"; fi
}

connector_url() {
    local domain path
    domain="$(env_get MCP_PUBLIC_HOST)"
    path="$(env_get MCP_HTTP_PATH)"
    if [ -n "$domain" ]; then echo "https://$domain$path"; else echo "http://127.0.0.1:$(env_get MCP_PORT)$path"; fi
}

mcp_call() {  # mcp_call '<json-rpc body>' [base url]  -> response body
    curl -sS --max-time 90 -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
        -d "$1" "${2:-http://127.0.0.1:$PORT}$(env_get MCP_HTTP_PATH)"
}

answers_publicly() {  # does https://DOMAIN answer MCP requests (checked from this server)?
    mcp_call '{"jsonrpc":"2.0","id":4,"method":"tools/list"}' "https://$1" 2>/dev/null | grep '"tools"' >/dev/null
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

port_owner() {  # the program listening on TCP port $1, if any
    { ss -Hltnp "sport = :$1" 2>/dev/null | sed -n 's/.*users:(("\([^"]*\)".*/\1/p' | head -n 1; } || true
}

public_ip() {  # this server's public IPv4 address (empty if it cannot be found)
    local url ip
    # Its own address first: outgoing traffic may leave through another IP (seen on Iranian servers).
    ip="$(ip -4 -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 \
        | grep -vE '^(10|127|169\.254|192\.168|172\.(1[6-9]|2[0-9]|3[01])|100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7]))\.' \
        | head -n 1 || true)"
    if [ -n "$ip" ]; then echo "$ip"; return 0; fi
    for url in https://api.ipify.org https://icanhazip.com; do  # behind NAT: ask what the internet sees
        ip="$(curl -4 -fsS --max-time 6 "$url" 2>/dev/null | tr -d '[:space:]' || true)"
        if [[ "$ip" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then echo "$ip"; return 0; fi
    done
}

local_ip() {  # is $1 one of this server's own addresses?
    ip -o addr show 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -xF "$1" >/dev/null
}

is_cloudflare() {  # is the IPv4 address $1 one of Cloudflare's proxies?
    "$VPY" -c 'import ipaddress, sys
ip = ipaddress.ip_address(sys.argv[1])
sys.exit(0 if any(ip in ipaddress.ip_network(net) for net in sys.argv[2].split()) else 1)' "$1" "$CLOUDFLARE_NETS"
}

pip_install() {  # the pinned Python packages; when pypi.org is blocked, from a mirror (still hash-checked)
    local pip=("$VPY" -m pip install -q --disable-pip-version-check --require-hashes -r "$APP_DIR/requirements.txt")
    local mirror
    if [ -n "${PIP_INDEX_URL:-}" ]; then
        quiet "${pip[@]}" && return 0
        log_tail
        die "Installing the Python packages from $PIP_INDEX_URL failed (see above)."
    fi
    quiet "${pip[@]}" --timeout 30 --retries 2 && return 0
    for mirror in "${PIP_MIRRORS[@]}"; do
        warn "pypi.org did not work; trying the mirror $(echo "$mirror" | cut -d/ -f3)"
        quiet "${pip[@]}" --timeout 30 --retries 1 --index-url "$mirror" && return 0
    done
    log_tail
    die "Installing the Python packages failed. With a PyPI mirror that works on this server, run:
       sudo PIP_INDEX_URL=https://<mirror>/simple $CLI_NAME update"
}

install_cli() {  # the mizito-connector command: a copy of this script that knows this installation
    install -o root -g root -m 700 "$CODE_DIR/install.sh" "$APP_DIR/install.sh"
    cat >"$CLI" <<EOF
#!/usr/bin/env bash
# Manage the Mizito AI Connector: $CLI_NAME help
[ "\$(id -u)" -eq 0 ] || exec sudo "\$0" "\$@"
export APP_DIR="$APP_DIR" APP_USER="$APP_USER" SERVICE="$SERVICE" NGINX_SITE="$NGINX_SITE" MIZITO_CLI="$CLI" MIZITO_SKIP_TLS="$SKIP_TLS"
exec bash "$APP_DIR/install.sh" "\${@:-help}"
EOF
    chmod 755 "$CLI"
}

choose_domain() {  # ask for the domain (a previous answer is the default) -> DOMAIN, SERVER_IP
    local previous="$1"
    SERVER_IP="$(public_ip)"
    DOMAIN="${MIZITO_DOMAIN:-}"
    if [ -z "$DOMAIN" ]; then
        echo "    The connector needs a domain or subdomain (e.g. mcp.example.com) with a DNS record"
        echo "    of type A pointing to this server's IP address: ${SERVER_IP:-(unknown)}"
        ask DOMAIN "Domain" "$previous"
    fi
    DOMAIN="$(printf '%s' "$DOMAIN" | tr '[:upper:]' '[:lower:]' | sed -e 's#^[a-z]*://##' -e 's#/.*$##' | tr -cd 'a-z0-9.-')"
    DOMAIN="${DOMAIN%.}"
    [[ "$DOMAIN" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$ ]] \
        || die "\"$DOMAIN\" is not a valid domain name (example: mcp.example.com)"
}

check_dns() {  # before asking Let's Encrypt for a certificate, the domain must point to this server
    local resolved v6 ip="${SERVER_IP:-the IP address of this server}"
    [ "${MIZITO_SKIP_DNS_CHECK:-0}" = 1 ] && return 0
    resolved="$(getent ahostsv4 "$DOMAIN" 2>/dev/null | awk 'NR==1 {print $1}' || true)"
    [ -n "$resolved" ] || die "$DOMAIN has no DNS record yet.
       At your domain provider, add a record of type A for $DOMAIN with the value $ip.
       Wait a few minutes, then run the same command again."
    if is_cloudflare "$resolved"; then
        die "$DOMAIN points to Cloudflare's proxy ($resolved), not to this server.
       In Cloudflare > DNS, click the orange cloud of this record so it turns grey (DNS only).
       Wait a minute, then run the same command again."
    fi
    if [ -n "${SERVER_IP:-}" ] && [ "$resolved" != "$SERVER_IP" ] && ! local_ip "$resolved"; then
        warn "$DOMAIN points to $resolved, but this server's IP address seems to be $SERVER_IP."
        warn "If the certificate step fails, change the A record of $DOMAIN to $SERVER_IP."
    else
        ok "$DOMAIN points to this server ($resolved)"
    fi
    v6="$(getent ahostsv6 "$DOMAIN" 2>/dev/null | awk '$1 !~ /^::ffff:/ {print $1; exit}' || true)"
    if [ -n "$v6" ] && ! local_ip "$v6"; then
        warn "$DOMAIN also has an IPv6 (AAAA) record, $v6, which is not this server. Delete it if the certificate step fails."
    fi
}

write_settings() {  # a new .env with the server settings; check_login.py adds the Mizito login
    local secret
    secret="$("$VPY" -c 'import secrets; print(secrets.token_urlsafe(32))')"
    (umask 077 && cat >"$ENV_FILE" <<EOF
# Written by install.sh. Change the Mizito login with: $CLI_NAME login
# After editing this file by hand: systemctl restart $SERVICE
MIZITO_ENABLE_WRITE=${MIZITO_ENABLE_WRITE:-1}
MIZITO_ENABLE_CRM=${MIZITO_ENABLE_CRM:-0}
MIZITO_ENABLE_ADMIN=${MIZITO_ENABLE_ADMIN:-0}
MCP_TRANSPORT=streamable-http
MCP_HOST=127.0.0.1
MCP_PORT=$PORT
MCP_HTTP_PATH=/mcp-$secret
MCP_PUBLIC_HOST=$DOMAIN
EOF
    )
}

fix_env_perms() { chown "$APP_USER:$APP_USER" "$ENV_FILE"; chmod 600 "$ENV_FILE"; }

mizito_login() {  # ask for the Mizito login, check it and save it in .env
    local run=("$VPY" -B "$APP_DIR/check_login.py" --save "$ENV_FILE")
    echo
    if has_tty; then
        "${run[@]}" </dev/tty || die "No working Mizito login yet. Run the same command again to try once more."
    else
        "${run[@]}" </dev/null || die "Mizito did not accept MIZITO_USERNAME + MIZITO_PASSWORD (or MIZITO_TOKEN)."
    fi
    fix_env_perms
}

restart_service() {  # restart and wait until it answers
    local _
    PORT="$(env_get MCP_PORT)"
    PORT="${PORT:-8765}"
    systemctl restart "$SERVICE"
    for _ in $(seq 1 30); do
        mcp_call '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' >/dev/null 2>&1 && return 0
        sleep 1
    done
    journalctl -u "$SERVICE" -n 25 --no-pager >&2 || true
    die "The service did not start (see the log above)."
}

mizito_check() {  # ask the running service who we are in Mizito
    local answer result
    answer="$(mcp_call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mizito_whoami","arguments":{}}}' 2>/dev/null || true)"
    result="$(printf '%s' "$answer" | "$VPY" -c '
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
    print("OK " + str(data.get("user_name")) + " (workspace: " + str(data.get("workspaces", [{}])[0].get("title")) + ")")
')"
    case "$result" in
        OK*) ok "Connected to Mizito as ${result#OK }"; return 0 ;;
        *) warn "${result#ERROR }"; return 1 ;;
    esac
}

setup_https() {  # a Let's Encrypt certificate for DOMAIN, and nginx in front of the service
    local cert="/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ipv6=1 request
    [ -f /proc/net/if_inet6 ] || ipv6=0
    install -d "$WEBROOT"
    systemctl enable --now nginx >/dev/null 2>&1 || true
    if command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep "Status: active" >/dev/null; then
        ufw allow 80/tcp >/dev/null && ufw allow 443/tcp >/dev/null && ok "Opened ports 80 and 443 in the ufw firewall"
    fi
    if [ ! -f "$cert" ]; then
        curl -sS -o /dev/null --max-time 20 https://acme-v02.api.letsencrypt.org/directory 2>/dev/null \
            || die "This server cannot reach Let's Encrypt, which issues the free HTTPS certificate
       (international access from this server may be restricted). With an HTTP proxy, run:
         sudo HTTPS_PROXY=http://<proxy-ip>:<port> $CLI_NAME update"
        cat >"$SITE" <<EOF
server {
    listen 80;
$([ "$ipv6" = 1 ] && echo "    listen [::]:80;")
    server_name $DOMAIN;
    location /.well-known/acme-challenge/ { root $WEBROOT; }
    location / { return 404; }
}
EOF
        ln -sf "$SITE" "/etc/nginx/sites-enabled/$NGINX_SITE"
        if ! quiet nginx -t; then log_tail; die "nginx rejected the configuration in $SITE"; fi
        systemctl reload nginx
        echo "    Asking Let's Encrypt for a free certificate (you accept their terms: https://letsencrypt.org/repository/)"
        request=(certbot certonly --webroot -w "$WEBROOT" -d "$DOMAIN" --non-interactive --agree-tos
                 --deploy-hook "systemctl reload nginx")
        if [ -n "${LETSENCRYPT_EMAIL:-}" ]; then request+=(--email "$LETSENCRYPT_EMAIL"); else request+=(--register-unsafely-without-email); fi
        if ! quiet "${request[@]}"; then
            log_tail 15
            die "Let's Encrypt could not check $DOMAIN. Make sure that:
         - the A record of $DOMAIN points to this server (${SERVER_IP:-its IP address}),
         - port 80 is open to the internet (also in your server provider's firewall),
       then run the same command again."
        fi
        ok "Certificate issued; it renews by itself"
    else
        ok "Certificate already present"
    fi
    sed -e "s#mcp.example.com#$DOMAIN#g" -e "s#127.0.0.1:8765#127.0.0.1:$PORT#g" \
        -e "s#/var/www/letsencrypt#$WEBROOT#g" "$CODE_DIR/deploy/nginx.conf.example" >"$SITE"
    [ "$ipv6" = 1 ] || sed -i '/listen \[::\]/d' "$SITE"
    ln -sf "$SITE" "/etc/nginx/sites-enabled/$NGINX_SITE"
    if ! quiet nginx -t; then log_tail; die "nginx rejected the configuration in $SITE"; fi
    systemctl reload nginx
    if answers_publicly "$DOMAIN"; then
        ok "https://$DOMAIN answers"
    else
        warn "https://$DOMAIN did not answer from this server itself. If ChatGPT or Claude cannot connect"
        warn "either, open ports 80 and 443 in your server provider's firewall."
    fi
}

# ---------------------------------------------------------------------------------------------------
cmd_install() {
    if [ -z "$CODE_DIR" ]; then download; fi
    if [ "$(id -u)" -ne 0 ] || [ "$SELF" != "$CODE_DIR/install.sh" ]; then
        as_root bash "$CODE_DIR/install.sh" install  # the downloaded copy, as root
    fi
    case "$CODE_DIR" in /tmp/mizito-connector.*) trap 'rm -rf "$CODE_DIR"' EXIT ;; esac
    : >>"$LOG" && chmod 600 "$LOG"
    printf '\n===== %s install from %s\n' "$(date '+%F %T')" "$CODE_DIR" >>"$LOG"
    local py port owner previous
    cat <<'EOF'

  Mizito AI Connector installer
  Connects your Mizito account to ChatGPT and Claude through this server.
EOF

    say "1/6  Checking this server"
    command -v apt-get >/dev/null 2>&1 || die "This installer needs Ubuntu or Debian (apt-get)."
    export DEBIAN_FRONTEND=noninteractive NEEDRESTART_SUSPEND=1  # no questions from apt
    local apt=(apt-get -y -q -o DPkg::Lock::Timeout=600)
    if ! command -v curl >/dev/null 2>&1; then
        quiet "${apt[@]}" update || true
        quiet "${apt[@]}" install curl ca-certificates || { log_tail; die "Installing curl failed (see above)."; }
    fi
    curl -sS -o /dev/null --max-time 20 https://app.mizito.ir 2>/dev/null \
        || die "This server cannot reach app.mizito.ir. Use a server that can open Mizito (for example one in Iran)."
    ok "Mizito is reachable"
    if [ "$SKIP_TLS" != 1 ]; then
        for port in 80 443; do
            owner="$(port_owner "$port")"
            if [ -n "$owner" ] && [ "$owner" != nginx ]; then
                die "Port $port is already used by \"$owner\", but the connector needs nginx on ports 80 and 443.
       Stop that program, or put the connector behind your own web server with MIZITO_SKIP_TLS=1 (see the guide)."
            fi
        done
        ok "Ports 80 and 443 are free for nginx"
    fi

    say "2/6  Installing (this takes a minute or two)"
    quiet "${apt[@]}" update || warn "apt-get update reported problems; trying to install anyway"
    local packages=(python3 python3-venv curl ca-certificates)
    [ "$SKIP_TLS" = 1 ] || packages+=(nginx certbot)
    if ! quiet "${apt[@]}" install "${packages[@]}"; then log_tail; die "Installing the system packages failed (see above)."; fi
    py="$(pick_python)" || { quiet "${apt[@]}" install python3.11 python3.11-venv && py=python3.11; } \
        || die "Python 3.11 or newer is needed: use Ubuntu 24.04 or 22.04, or Debian 12."
    "$py" -c 'import venv, ensurepip' 2>/dev/null || quiet "${apt[@]}" install "$(basename "$py")-venv" || true
    ok "System packages ($("$py" --version))"
    id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home-dir "$APP_DIR" --no-create-home --shell /usr/sbin/nologin "$APP_USER"
    install -d -o root -g "$APP_USER" -m 750 "$APP_DIR" "$APP_DIR/mizito"
    if [ -f "$APP_DIR/server.py" ]; then  # keep the previous version to roll back to (the last 5)
        local backup
        backup="$APP_DIR/backup/$(date +%Y%m%d-%H%M%S)"
        install -d -m 700 "$backup"
        cp -a "$APP_DIR/server.py" "$APP_DIR/mizito_client.py" "$APP_DIR/mizito" "$backup/" 2>/dev/null || true
        find "$APP_DIR/backup" -mindepth 1 -maxdepth 1 -type d | sort | head -n -5 | xargs -r rm -rf
        rm -f "$APP_DIR"/mizito/*.py
    fi
    install -o root -g "$APP_USER" -m 640 "$CODE_DIR/server.py" "$CODE_DIR/mizito_client.py" "$CODE_DIR/check_login.py" \
        "$CODE_DIR/pyproject.toml" "$APP_DIR/"
    install -o root -g "$APP_USER" -m 640 "$CODE_DIR"/mizito/*.py "$APP_DIR/mizito/"
    install -o root -g "$APP_USER" -m 640 "$CODE_DIR/deploy/requirements.txt" "$APP_DIR/requirements.txt"
    install_cli
    if [ ! -x "$VPY" ] && ! quiet "$py" -m venv "$APP_DIR/.venv"; then log_tail; die "Creating the Python environment failed."; fi
    pip_install
    chown -R root:"$APP_USER" "$APP_DIR/.venv"
    chmod -R o-rwx "$APP_DIR"
    ok "Connector installed in $APP_DIR"

    say "3/6  Your domain"
    previous="$(env_get MCP_PUBLIC_HOST)"
    DOMAIN="$previous"
    if [ "$SKIP_TLS" = 1 ]; then
        DOMAIN="${MIZITO_DOMAIN:-$previous}"
        ok "No HTTPS setup (MIZITO_SKIP_TLS=1)"
    elif [ -n "$previous" ] && [ -f "/etc/letsencrypt/live/$previous/fullchain.pem" ]; then
        ok "$previous (already set up)"
    else
        choose_domain "$previous"
        check_dns
    fi

    say "4/6  Your Mizito login"
    [ -f "$ENV_FILE" ] || write_settings
    [ "$DOMAIN" = "$(env_get MCP_PUBLIC_HOST)" ] || env_set MCP_PUBLIC_HOST "$DOMAIN"
    if [ -n "$(env_get MIZITO_TOKEN)$(env_get MIZITO_PASSWORD)" ]; then
        ok "Keeping the saved login (to change it later: $CLI_NAME login)"
    else
        mizito_login
    fi
    fix_env_perms

    say "5/6  Starting the service"
    sed -e "s#/opt/mizito-mcp#$APP_DIR#g" -e "s#^User=.*#User=$APP_USER#" -e "s#^Group=.*#Group=$APP_USER#" \
        "$CODE_DIR/deploy/mizito-mcp.service" >"/etc/systemd/system/$SERVICE.service"
    systemctl daemon-reload
    systemctl enable "$SERVICE" >/dev/null 2>&1
    restart_service
    if ! mizito_check; then
        has_tty || die "The service runs, but Mizito refused the saved login. Log in again with:  $CLI_NAME login"
        warn "Mizito refused the saved login. Please log in again."
        mizito_login
        restart_service
        mizito_check || die "The service runs, but it cannot work with Mizito (see the message above)."
    fi
    ok "$(mcp_call '{"jsonrpc":"2.0","id":3,"method":"tools/list"}' | "$VPY" -c 'import json,sys; print(len(json.load(sys.stdin)["result"]["tools"]))' 2>/dev/null || echo "?") tools available"

    if [ "$SKIP_TLS" = 1 ]; then
        say "6/6  HTTPS skipped (MIZITO_SKIP_TLS=1): point your web server to 127.0.0.1:$PORT"
    else
        say "6/6  HTTPS for $DOMAIN"
        setup_https
    fi

    cat <<EOF

  ==========================================================================================
   Done. Your connector address (keep it secret: it works like a password):

     $(connector_url)

  ==========================================================================================
   Now add it in ChatGPT or Claude:
     Claude:   Settings > Connectors > Add custom connector > paste the address (no OAuth)
     ChatGPT:  Settings > Apps & Connectors > Advanced > turn on Developer mode, then
               Create > paste the address > Authentication: No authentication

   Later:  $CLI_NAME url       show the address again
           $CLI_NAME status    check that everything works
           $CLI_NAME login     log in to Mizito again
           $CLI_NAME update    update to the latest version

EOF
}

cmd_update() {  # always the latest code from GitHub
    download
    as_root bash "$CODE_DIR/install.sh" install
}

need_installed() { [ -f "$ENV_FILE" ] || die "The connector is not installed yet. Install it with:  $INSTALL_CMD"; }

cmd_url() { need_installed; connector_url; }

cmd_status() {
    local domain
    need_installed
    PORT="$(env_get MCP_PORT)"
    if systemctl is-active --quiet "$SERVICE"; then ok "The service is running"; else warn "The service is not running (see: $CLI_NAME logs)"; fi
    mizito_check || warn "To log in again:  $CLI_NAME login"
    domain="$(env_get MCP_PUBLIC_HOST)"
    if [ -n "$domain" ]; then
        if answers_publicly "$domain"; then ok "https://$domain answers"; else warn "https://$domain does not answer from this server"; fi
    fi
    echo "    Connector address: $(connector_url)"
}

cmd_login() {
    need_installed
    mizito_login
    restart_service
    mizito_check || die "Mizito still does not accept the login."
}

cmd_logs() { need_installed; exec journalctl -u "$SERVICE" -n 50 -f; }

cmd_help() {
    cat <<EOF
Mizito AI Connector

  $CLI_NAME url       show the connector address
  $CLI_NAME status    check that everything works
  $CLI_NAME login     log in to Mizito again (new password, or the login expired)
  $CLI_NAME update    update to the latest version (settings are kept)
  $CLI_NAME logs      follow the service log (Ctrl+C to stop)

First installation:  $INSTALL_CMD
EOF
}

main() {
    case "${1:-install}" in
        install) cmd_install ;;
        update) cmd_update ;;
        url | status | login | logs) need_root "$@"; "cmd_$1" ;;
        help | -h | --help) cmd_help ;;
        *) cmd_help; exit 1 ;;
    esac
}

main "$@"
