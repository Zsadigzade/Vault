#!/usr/bin/env bash
# sync.sh — Vault git sync for the DO server
#
# Usage:
#   bash scripts/sync.sh           # Pull → run learning → commit → push
#   bash scripts/sync.sh --pull-only     # Only pull, no learning run
#   bash scripts/sync.sh --push-only     # Only commit + push pending changes
#   bash scripts/sync.sh --dry-run       # Show what would happen, no writes
#
# Set VAULT_ROOT env var or run from vault root directory.

set -euo pipefail

VAULT_ROOT="${VAULT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
LOG_FILE="$VAULT_ROOT/07-Learning/sync.log"
DRY_RUN=false
PULL_ONLY=false
PUSH_ONLY=false

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dry-run)   DRY_RUN=true ;;
    --pull-only) PULL_ONLY=true ;;
    --push-only) PUSH_ONLY=true ;;
  esac
done

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Vault sync start ==="
log "VAULT_ROOT: $VAULT_ROOT"
log "DRY_RUN: $DRY_RUN | PULL_ONLY: $PULL_ONLY | PUSH_ONLY: $PUSH_ONLY"

cd "$VAULT_ROOT"

# ── Pull ───────────────────────────────────────────────────────────────────

if [ "$PUSH_ONLY" = false ]; then
  log "Pulling from remote..."
  if [ "$DRY_RUN" = true ]; then
    log "[DRY-RUN] Would run: git pull --rebase origin main"
  else
    git pull --rebase origin main 2>&1 | tee -a "$LOG_FILE" || {
      log "ERROR: git pull failed. Check remote and SSH key."
      exit 1
    }
  fi
fi

if [ "$PULL_ONLY" = true ]; then
  log "Pull-only mode. Done."
  exit 0
fi

# ── Run learning agent ─────────────────────────────────────────────────────

if [ "$PUSH_ONLY" = false ]; then
  log "Running knowledge update..."
  if [ "$DRY_RUN" = true ]; then
    log "[DRY-RUN] Would run: python scripts/knowledge_update.py --max-per-run 10"
  else
    python3 scripts/knowledge_update.py --max-per-run 10 2>&1 | tee -a "$LOG_FILE" || {
      log "WARNING: knowledge_update.py failed (non-fatal)"
    }
  fi
else
  log "Push-only mode — skipping knowledge update."
fi

# ── Commit new inbox items ─────────────────────────────────────────────────

PENDING_COUNT=$(find "$VAULT_ROOT/06-Inbox/pending" -name "*.md" ! -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')
LEARNING_CHANGED=$(git diff --name-only HEAD -- 07-Learning/ 2>/dev/null | wc -l | tr -d ' ')

if [ "$PENDING_COUNT" -gt 0 ] || [ "$LEARNING_CHANGED" -gt 0 ]; then
  COMMIT_MSG="chore(vault): autonomous update $(date '+%Y-%m-%d')

- inbox proposals: $PENDING_COUNT new items
- learning log updated"

  log "Staging and committing ($PENDING_COUNT inbox items, $LEARNING_CHANGED learning changes)..."
  if [ "$DRY_RUN" = true ]; then
    log "[DRY-RUN] Would commit: $COMMIT_MSG"
  else
    git add "06-Inbox/pending/" "07-Learning/" 2>&1 | tee -a "$LOG_FILE"
    git diff --cached --quiet || git commit -m "$COMMIT_MSG" 2>&1 | tee -a "$LOG_FILE"
  fi
else
  log "Nothing new to commit."
fi

# ── Push ──────────────────────────────────────────────────────────────────

log "Pushing to remote..."
if [ "$DRY_RUN" = true ]; then
  log "[DRY-RUN] Would run: git push origin main"
else
  git push origin main 2>&1 | tee -a "$LOG_FILE" || {
    log "ERROR: git push failed."
    exit 1
  }
fi

log "=== Vault sync complete ==="
