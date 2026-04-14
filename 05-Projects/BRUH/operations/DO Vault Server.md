---
tags: [operations, server, digitalocean, automation, vault]
area: operations
updated: 2026-04-13
---

# DO Vault Server

Autonomous knowledge-learning server running 24/7.

---

## Specs

| Key | Value |
|-----|-------|
| Provider | DigitalOcean, FRA1 |
| IP | `46.101.161.176` |
| Spec | 2 vCPU · 4 GB RAM · 80 GB SSD |
| OS | Ubuntu 24.04 LTS |
| User | `vaultbot` (operations) · `root` (admin) |
| Vault path | `/srv/vault` |
| Vault repo | `github.com/Zsadigzade/Vault` (private, deploy key) |

---

## SSH access

```bash
ssh root@46.101.161.176
```

Local key: `~/.ssh/id_ed25519` (passphrase-protected — must enter passphrase interactively).

> [!warning] Always operate git as `vaultbot`, not root. Root commits break `.git` ownership.
> ```bash
> sudo -u vaultbot git pull origin main
> sudo -u vaultbot git push origin main
> ```

---

## Stack

| Component | Details |
|-----------|---------|
| **Ollama** | `qwen2.5-coder:1.5b` (986 MB — fits in 4 GB RAM). Systemd service + warmup service on boot. |
| **SearxNG** | Docker, `localhost:8888`. Brave API key + SearxNG = dual search backends. |
| **Python venv** | `/srv/vault/.venv` — scripts: `scripts/knowledge_update.py`, `scripts/vault_health.py`, `scripts/alert_on_failure.py`, `scripts/sync.sh` |
| **Alerts** | `alert_on_failure.py` → Resend API → `zsadigzade@gmail.com`. User-Agent: `curl/8.5.0` (Cloudflare bypass). |

---

## Cron schedule (vaultbot)

| Time | Job |
|------|-----|
| 06:00 daily | `sync.sh --pull-only` → git pull vault |
| 08:00 daily | `vault_health.py` → health report to inbox |
| 09:00 Mon–Fri | `knowledge_update.py --max-per-run 10` → research + proposals |
| 10:00 daily | `sync.sh --push-only` → git push vault |
| 11:00 Sunday | `knowledge_update.py --topic ai_tooling --force` → deep AI scan |

Logs: `/var/log/vault-learn.log`, `/var/log/vault-push.log`, `/var/log/vault-pull.log`, `/var/log/vault-health.log` (owned by vaultbot).

---

## Pipeline flow

```
9am cron → knowledge_update.py
  → Brave API + SearxNG search
  → Ollama qwen2.5-coder:1.5b summarization (+0.4 confidence boost)
  → confidence ≥ 0.35 → write to 06-Inbox/pending/
10am cron → git push pending files to GitHub
Manual → /approve-inbox (Claude Code skill) → review, append to KB, commit, push
```

---

## Confidence thresholds

| Score | Action |
|-------|--------|
| ≥ 0.80 | Ollama summary present — high quality |
| 0.35–0.79 | Accepted, queued for review |
| < 0.35 | Dropped (logged to LEARNING_LOG) |

Max without Ollama: ~0.40. With Ollama: up to 0.80.

---

## Models — size guide

| Model | Size | Status |
|-------|------|--------|
| `qwen2.5-coder:1.5b` | 986 MB | **Active** — fits RAM |
| `qwen2.5-coder:7b` | 4.7 GB | Removed — CPU swap, 25s/token |
| `llama3.3` | 42 GB | Removed — needs 40 GB RAM |

> [!warning] Never pull `llama3.3` or `qwen2.5-coder:7b` again — they don't fit in 4 GB RAM and will fill the disk.

---

## Disk

After cleanup (2026-04-13): **23% used** (18 GB / 77 GB). Monitor — if > 70%, check for stale Ollama models.

```bash
df -h /
ollama list
```

---

## Manual pipeline commands (qwen auto-learning)

### SSH in
```bash
ssh root@46.101.161.176
# enter id_ed25519 passphrase when prompted
```

### Helper — load vaultbot env + cd (run this first every session)
```bash
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && exec bash'
# now you're vaultbot with correct env and in /srv/vault
```

Or prefix every command individually (see below).

### Sync vault (pull / push)
```bash
# Pull latest from GitHub → local /srv/vault
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && bash scripts/sync.sh --pull-only'

# Push local /srv/vault → GitHub
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && bash scripts/sync.sh --push-only'
```

### Run knowledge update (qwen research + proposals)
```bash
# Standard run — up to 10 proposals written to 06-Inbox/pending/
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && /srv/vault/.venv/bin/python scripts/knowledge_update.py --max-per-run 10'

# Force deep AI tooling scan (Sunday special)
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && /srv/vault/.venv/bin/python scripts/knowledge_update.py --topic ai_tooling --force'
```

### Run vault health check
```bash
sudo -u vaultbot bash -c 'source /home/vaultbot/.vault_env && cd "$VAULT_ROOT" && /srv/vault/.venv/bin/python scripts/vault_health.py'
```

### Check logs
```bash
tail -50 /var/log/vault-learn.log    # knowledge_update.py output
tail -50 /var/log/vault-push.log     # sync --push-only output
tail -50 /var/log/vault-pull.log     # sync --pull-only output
tail -50 /var/log/vault-health.log   # vault_health.py output
```

### Check pending proposals
```bash
ls /srv/vault/06-Inbox/pending/
```

### Approve proposals (Claude Code — run locally, not on server)
```
/approve-inbox
```
Reads `06-Inbox/pending/`, reviews each with Claude, moves approved to their target path, commits + pushes.

> [!warning] Always `sudo -u vaultbot` — root breaks `.git` ownership. Scripts live in `scripts/`, not vault root. Env vars (`$VAULT_ROOT` etc.) live in `/home/vaultbot/.vault_env` — must be sourced before any script.

---

## Known gotchas

- **Git as root** breaks `.git` ownership → `sudo -u vaultbot git` always
- **`/var/log/vault-*.log`** must be pre-created and owned by vaultbot (root owns `/var/log/`)
- **Brave API** returns gzip — `Accept-Encoding: gzip` header removed; manual `gzip.decompress()` in script
- **Resend API** blocked by Cloudflare without `User-Agent: curl/8.5.0`
- **git safe.directory** needed for root: `git config --global --add safe.directory /srv/vault`
- **SSH from Claude Code** doesn't work — key is passphrase-protected, non-interactive shell can't sign

---

## See also

- [[WATCH_TOPICS]] — research query registry
- [[Agent MCP — live verification]]
- `/approve-inbox` Claude Code skill (`~/.claude/skills/approve-inbox/`)
