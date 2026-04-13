#!/usr/bin/env bash
# setup_server.sh — One-command DigitalOcean server setup for vault automation
#
# Run as root on a fresh Ubuntu 22.04 / 24.04 droplet:
#   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_VAULT_REPO/main/scripts/setup_server.sh | bash
#
# Or copy to server and run:
#   scp scripts/setup_server.sh root@YOUR_DO_IP:/tmp/
#   ssh root@YOUR_DO_IP bash /tmp/setup_server.sh

set -euo pipefail

VAULT_USER="vaultbot"
VAULT_DIR="/srv/vault"
PYTHON_MIN="3.11"

log()  { echo -e "\033[32m[SETUP]\033[0m $*"; }
warn() { echo -e "\033[33m[WARN]\033[0m  $*"; }
err()  { echo -e "\033[31m[ERROR]\033[0m $*"; exit 1; }

log "=== Vault server setup ==="
[ "$(id -u)" = "0" ] || err "Run as root (sudo su -)"

# ── System packages ────────────────────────────────────────────────────────

log "Updating system packages..."
apt-get update -qq
apt-get install -y -qq \
  python3 python3-pip python3-venv \
  git curl wget \
  docker.io docker-compose \
  ufw fail2ban \
  jq

# ── Vault user ─────────────────────────────────────────────────────────────

if ! id "$VAULT_USER" &>/dev/null; then
  log "Creating user: $VAULT_USER"
  useradd -m -s /bin/bash "$VAULT_USER"
  mkdir -p /home/$VAULT_USER/.ssh
  chmod 700 /home/$VAULT_USER/.ssh
fi

# ── SSH key for git ────────────────────────────────────────────────────────

SSH_KEY="/home/$VAULT_USER/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
  log "Generating SSH key for git access..."
  su - "$VAULT_USER" -c "ssh-keygen -t ed25519 -C 'vault@$(hostname)' -f $SSH_KEY -N ''"
  log "Add this public key to your GitHub repo (Settings → Deploy Keys → Add):"
  echo ""
  cat "${SSH_KEY}.pub"
  echo ""
  warn "Add the key above to GitHub before continuing."
  read -p "Press Enter once the deploy key is added..."
fi

# ── Ollama ─────────────────────────────────────────────────────────────────

if ! command -v ollama &>/dev/null; then
  log "Installing Ollama..."
  curl -fsSL https://ollama.com/install.sh | sh
  systemctl enable ollama
  systemctl start ollama
  sleep 3
  log "Pulling default models (this takes a while)..."
  ollama pull llama3.3      || warn "Failed to pull llama3.3"
  ollama pull qwen2.5-coder || warn "Failed to pull qwen2.5-coder"
else
  log "Ollama already installed."
fi

# ── SearxNG via Docker ─────────────────────────────────────────────────────

SEARXNG_DIR="/srv/searxng"
if [ ! -d "$SEARXNG_DIR" ]; then
  log "Setting up SearxNG..."
  mkdir -p "$SEARXNG_DIR/searxng"

  # SearxNG settings
  cat > "$SEARXNG_DIR/searxng/settings.yml" << 'SEARXNG_EOF'
use_default_settings: true
server:
  secret_key: "CHANGE_ME_RANDOM_SECRET"
  limiter: false
  image_proxy: false
search:
  safe_search: 0
  autocomplete: ""
  default_lang: "en"
  formats:
    - html
    - json
engines:
  - name: google
    engine: google
    language: en
    region: en-US
    disabled: false
  - name: bing
    engine: bing
    disabled: false
  - name: duckduckgo
    engine: duckduckgo
    disabled: false
  - name: wikipedia
    engine: wikipedia
    disabled: false
SEARXNG_EOF

  # Docker compose
  cat > "$SEARXNG_DIR/docker-compose.yml" << 'DOCKER_EOF'
version: "3.7"
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    restart: unless-stopped
    ports:
      - "127.0.0.1:8888:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
DOCKER_EOF

  cd "$SEARXNG_DIR" && docker-compose up -d
  log "SearxNG running at http://localhost:8888"
else
  log "SearxNG already configured."
fi

# ── Clone vault ────────────────────────────────────────────────────────────

if [ ! -d "$VAULT_DIR/.git" ]; then
  log "Enter your vault GitHub repo SSH URL (e.g. git@github.com:username/vault.git):"
  read -p "Repo URL: " VAULT_REPO_URL
  su - "$VAULT_USER" -c "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone $VAULT_REPO_URL $VAULT_DIR"
  log "Vault cloned to $VAULT_DIR"
else
  log "Vault already cloned at $VAULT_DIR."
fi

# ── Python env ────────────────────────────────────────────────────────────

VENV_DIR="$VAULT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
  log "Creating Python virtual environment..."
  su - "$VAULT_USER" -c "python3 -m venv $VENV_DIR && $VENV_DIR/bin/pip install --quiet pyyaml requests"
fi

# ── Environment file ──────────────────────────────────────────────────────

ENV_FILE="/home/$VAULT_USER/.vault_env"
if [ ! -f "$ENV_FILE" ]; then
  log "Creating environment file: $ENV_FILE"
  cat > "$ENV_FILE" << ENV_EOF
# Vault automation environment
export VAULT_ROOT="$VAULT_DIR/First Vault"
export SEARXNG_URL="http://localhost:8888"

# Add your API keys below:
# export BRAVE_SEARCH_API_KEY="your_key_here"
# export PERPLEXITY_API_KEY="your_key_here"
# export ANTHROPIC_API_KEY="your_key_here"

# Ollama endpoint (local on this server)
export OLLAMA_ENDPOINT="http://localhost:11434"
ENV_EOF
  chown "$VAULT_USER:$VAULT_USER" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
  log "Edit $ENV_FILE and add your API keys."
fi

# ── Cron jobs ─────────────────────────────────────────────────────────────

log "Installing cron jobs for $VAULT_USER..."
CRON_FILE="/tmp/vaultbot_cron"
cat > "$CRON_FILE" << CRON_EOF
# Vault automation cron jobs
# Pull vault from GitHub
0 6 * * * source /home/$VAULT_USER/.vault_env && cd "\$VAULT_ROOT" && bash scripts/sync.sh --pull-only >> /var/log/vault-pull.log 2>&1

# Daily health check at 8am
0 8 * * * source /home/$VAULT_USER/.vault_env && cd "\$VAULT_ROOT" && $VENV_DIR/bin/python scripts/vault_health.py >> /var/log/vault-health.log 2>&1

# Knowledge update at 9am (weekdays)
0 9 * * 1-5 source /home/$VAULT_USER/.vault_env && cd "\$VAULT_ROOT" && $VENV_DIR/bin/python scripts/knowledge_update.py --max-per-run 10 >> /var/log/vault-learn.log 2>&1

# Push results at 10am
0 10 * * * source /home/$VAULT_USER/.vault_env && cd "\$VAULT_ROOT" && bash scripts/sync.sh --push-only >> /var/log/vault-push.log 2>&1

# Full AI tooling deep scan on Sundays
0 11 * * 0 source /home/$VAULT_USER/.vault_env && cd "\$VAULT_ROOT" && $VENV_DIR/bin/python scripts/knowledge_update.py --topic ai_tooling --force >> /var/log/vault-learn.log 2>&1
CRON_EOF

crontab -u "$VAULT_USER" "$CRON_FILE"
rm "$CRON_FILE"
log "Cron jobs installed."

# ── Firewall ───────────────────────────────────────────────────────────────

log "Configuring UFW firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp   # optional: nginx for Ollama proxy
ufw allow 443/tcp  # optional: TLS
# SearxNG and Ollama are localhost-only — NOT exposed publicly
ufw --force enable
log "UFW enabled. Ollama (11434) and SearxNG (8888) are localhost-only."

# ── Log rotation ───────────────────────────────────────────────────────────

cat > /etc/logrotate.d/vault << 'LOGROTATE_EOF'
/var/log/vault-*.log {
  daily
  rotate 14
  compress
  missingok
  notifempty
}
LOGROTATE_EOF

# ── Summary ───────────────────────────────────────────────────────────────

log ""
log "=== Setup complete ==="
log ""
log "Services running:"
log "  Ollama:  http://localhost:11434"
log "  SearxNG: http://localhost:8888"
log ""
log "Next steps:"
log "  1. Edit /home/$VAULT_USER/.vault_env — add API keys (Brave, Perplexity)"
log "  2. Test: su - $VAULT_USER -c 'source ~/.vault_env && python3 \$VAULT_ROOT/scripts/knowledge_update.py --dry-run'"
log "  3. Test sync: su - $VAULT_USER -c 'source ~/.vault_env && bash \$VAULT_ROOT/scripts/sync.sh --dry-run'"
log "  4. On your PC: git remote add origin git@github.com:USERNAME/vault.git && git push -u origin main"
log ""
log "Cron schedule:"
log "  6am   — Pull from GitHub"
log "  8am   — Vault health check"
log "  9am   — Knowledge update (weekdays)"
log "  10am  — Push results to GitHub"
log "  Sun   — Deep AI tooling scan"
