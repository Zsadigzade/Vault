---
tags: [meta, server, automation, do]
area: meta
updated: 2026-04-13
tldr: "DigitalOcean server connects to vault via git. Runs Ollama + SearxNG + cron learning agent."
---

# Server Setup (DigitalOcean)

## TL;DR

- Server syncs vault via **GitHub private repo** (pull → learn → commit → push)
- Runs **Ollama** (always-on LLM inference) + **SearxNG** (self-hosted search)
- Autonomous learning: `knowledge_update.py` searches web, proposes to `06-Inbox/pending/`
- You review on PC: `git pull` → `/approve-inbox` → `git push`

---

## Architecture

```
Your PC                      GitHub (private)           DO Server
─────────                    ────────────────           ─────────
Obsidian vault  ←── pull ──  vault repo  ←── push ──  vaultbot cron
                             (origin)                  ├─ Ollama (llama3.3, qwen2.5-coder)
                                                       ├─ SearxNG (localhost:8888)
                                                       ├─ knowledge_update.py
                                                       ├─ vault_health.py
                                                       └─ sync.sh
```

---

## Step 1 — Create GitHub private repo

1. Go to github.com → New repository → **Private**
2. Name: `vault` (or any name)
3. Do NOT initialize with README (vault already has git)

---

## Step 2 — Push vault to GitHub (your PC)

```bash
cd "C:\Users\zsadi\Desktop\vault\First Vault"
git remote add origin git@github.com:YOUR_USERNAME/vault.git
git branch -M main
git add .
git commit -m "chore: initial vault push"
git push -u origin main
```

If you use HTTPS instead of SSH:
```bash
git remote add origin https://github.com/YOUR_USERNAME/vault.git
```

---

## Step 3 — Provision DigitalOcean droplet

**Recommended specs:**
- OS: Ubuntu 24.04 LTS
- Size: Basic, 4GB RAM / 2 vCPU ($24/month) minimum — 8GB recommended for Ollama models
- Region: pick closest to you
- Authentication: SSH key

**Connect:**
```bash
ssh root@YOUR_DO_IP
```

---

## Step 4 — Run setup script

```bash
# Copy script to server
scp "scripts/setup_server.sh" root@YOUR_DO_IP:/tmp/

# Run it
ssh root@YOUR_DO_IP bash /tmp/setup_server.sh
```

Or one-liner after repo is public/accessible:
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/vault/main/scripts/setup_server.sh | bash
```

The script installs: Python 3, git, Docker, Ollama, SearxNG, UFW firewall, cron jobs.

---

## Step 5 — Add API keys to server

```bash
ssh vaultbot@YOUR_DO_IP
nano ~/.vault_env
```

Add:
```bash
export BRAVE_SEARCH_API_KEY="your_key"    # get at brave.com/search/api
export PERPLEXITY_API_KEY="your_key"      # get at perplexity.ai/settings/api
export ANTHROPIC_API_KEY="your_key"       # optional — for fallback roles
```

Get API keys:
- **Brave Search:** https://brave.com/search/api — 2,000 free queries/month
- **Perplexity:** https://www.perplexity.ai/settings/api — $5 credit free on signup

---

## Step 6 — Test the pipeline

```bash
# SSH as vaultbot
ssh vaultbot@YOUR_DO_IP

# Dry run — no writes
source ~/.vault_env
python3 $VAULT_ROOT/scripts/knowledge_update.py --dry-run

# Test search only
python3 $VAULT_ROOT/scripts/knowledge_update.py --topic ai_tooling --dry-run --max-per-run 2

# Test sync
bash $VAULT_ROOT/scripts/sync.sh --dry-run
```

---

## Step 7 — Your daily workflow

**Morning (server has already run):**
```bash
# On your PC
cd "C:\Users\zsadi\Desktop\vault\First Vault"
git pull origin main
```

Then in Claude Code (vault directory):
```
/approve-inbox
```

Or run directly:
```bash
python scripts/approve_inbox.py --move
```

**After approving:**
```bash
git add .
git commit -m "chore: approve inbox batch $(date +%Y-%m-%d)"
git push origin main
```

---

## Cron schedule (server)

| Time | Job |
|------|-----|
| 6:00am | `git pull` — get any changes you pushed |
| 8:00am | `vault_health.py` — health check → inbox |
| 9:00am (Mon–Fri) | `knowledge_update.py` — 10 topics → inbox |
| 10:00am | `sync.sh --push-only` — commit + push results |
| 11:00am (Sun) | Deep scan of ai_tooling topics |

---

## Ollama endpoints

After setup, roles use:
- **Server:** `http://localhost:11434` (from server scripts)
- **Your PC (local):** `http://localhost:11434` (unchanged)
- **Role fallback:** `claude-sonnet-4-6` via `model_fallback:` in role frontmatter

To expose Ollama to your PC over SSH tunnel (optional):
```bash
# On your PC — forward server's Ollama to local port 11435
ssh -L 11435:localhost:11434 vaultbot@YOUR_DO_IP -N
```
Then in role files, change `endpoint: http://localhost:11435` to use server's models locally.

---

## Security checklist

- [ ] UFW active (only SSH, 80, 443 public — Ollama + SearxNG are localhost-only)
- [ ] `fail2ban` installed (blocks brute force SSH)
- [ ] API keys in `~/.vault_env` with `chmod 600`
- [ ] No secrets in vault files (only env var names)
- [ ] Vault repo is **private** on GitHub
- [ ] Deploy key on GitHub is read/write but scoped to one repo

---

## Troubleshooting

| Problem | Check |
|---------|-------|
| `git push` fails | `ssh -T git@github.com` — key added to GitHub? |
| Ollama not responding | `systemctl status ollama` and `ollama list` |
| SearxNG error | `docker ps` — is container running? `docker logs searxng` |
| No inbox proposals | `cat /var/log/vault-learn.log` — API keys set? |
| Merge conflicts | Human edited + server edited same file → resolve manually on PC |

---

## See also

→ [[GIT_REMOTE_SETUP]] · [[GIT_IMPORT_PROTOCOL]] · [[WATCH_TOPICS]] · [[INBOX_PROTOCOL]]
