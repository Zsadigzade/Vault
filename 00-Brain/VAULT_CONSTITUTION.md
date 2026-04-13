---
tags: [meta, constitution, vault-wide, agents, agent:immutable]
area: meta
status: stable
updated: 2026-04-13
tldr: "Vault-wide laws: write tiers, inbox, low-risk auto-merge, no secrets in vault."
---

# Vault constitution (read-only for agents)

> [!warning] **Agents:** Treat as **immutable** unless the human edits. If task conflicts, stop and ask. **BRUH product laws** live in `05-Projects/BRUH/reference/CONSTITUTION.md` — load when work is under `05-Projects/BRUH/`.

## Write tiers

| Tier | Paths | Agent writes | Gate |
|------|--------|--------------|------|
| 1 | `06-Inbox/pending/` | Allowed (new notes, append) | None |
| 2 | `04-Knowledge/`, `05-Projects/` (except reference constitutions) | **Propose** via inbox or PR-style note; human batch weekly | Human |
| 3 | `00-Brain/` (except documented exceptions), `01-Agents/roles/` | **No** direct edits | Human only |

## Low-risk auto-merge (optional automation)

Notes may be auto-merged **only if all** hold:

- Frontmatter `low_risk: true`
- Target path is on **allowlist**: `07-Learning/VAULT_HEALTH.md` (append metrics section only), `07-Learning/LEARNING_LOG.md` (append-only), `07-Learning/OUTCOMES_LEDGER.md` (append-only), `06-Inbox/approved/` (move from pending)
- **Never** auto-merge into: `00-Brain/VAULT_CONSTITUTION.md`, `01-Agents/roles/`, `05-Projects/BRUH/reference/CONSTITUTION.md`, any `**/reference/CONSTITUTION.md`

Human runs `approve_inbox.py --dry-run` before enabling real auto-merge.

## Security

- **No secrets** in vault (no API keys, tokens, private keys). Document *names* of env vars only.
- Cite external URLs; do not paste credentials from tooling into notes.

## Citations and web capture

- New synthesized claims from the web → **capture in `06-Inbox/pending/` first** with `source_url`, `retrieved_at`, proposed KB path.
- Promotion to `04-Knowledge/` after weekly batch or allowlist rules.

## Session and roles

- Universal entry: `00-Brain/HOME.md` → `01-Agents/DISPATCHER.md` as needed.
- Respect per-role `reads_on_activation` and token budgets in `00-Brain/AGENT_READ_ORDER.md`.

## Weekly batch obligation

- Human (or delegate) reviews `06-Inbox/pending/` → files or merges into Tier 2; archives rejects to `06-Inbox/archive/`.
