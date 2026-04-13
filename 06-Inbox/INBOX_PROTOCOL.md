---
tags: [inbox, agents, governance]
area: meta
updated: 2026-04-13
tldr: "Tier-1 writes here; frontmatter required; weekly batch to KB/projects."
---

# Inbox protocol

## Folders

- `pending/` — new captures, agent proposals.
- `approved/` — human OK’d; ready to file into `04-Knowledge/` or `05-Projects/`.
- `archive/` — rejected or already merged (keep short reason in note).

## Required frontmatter (proposals)

```yaml
---
inbox_id: inbox-2026-04-13-001
status: pending
proposed_location: "04-Knowledge/KB-Business/Strategy-Frameworks.md"
confidence: 0.85
source_agent: CTO
source_url: "https://example.com/article"
retrieved_at: "2026-04-13"
low_risk: false
human_gate: required
rationale: "One line."
---
```

## Rules

- No secrets. **Cite URLs** — use `_Sources/CITATION_BLOCK` pattern; trusted feeds in [[SOURCE_REGISTRY]].
- See [[VAULT_CONSTITUTION]] for promotion tiers and low-risk rules.
- Batch review: `vault-automation/scripts/approve_inbox.py` (default dry-run; `--move-low-risk-to-approved` stages to `approved/`).
