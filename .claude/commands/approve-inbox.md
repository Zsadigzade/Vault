Review and approve pending inbox items.

## What this does
1. List all files in `06-Inbox/pending/` (excluding `.gitkeep`)
2. For each file, show: inbox_id, source_agent, confidence, proposed_location, rationale
3. Present a preview of the content
4. Ask for approval: approve / reject / skip
5. On approve: mark status as "approved" and confirm the proposed_location
6. On reject: ask for rejection_reason, mark as "rejected"
7. After review: summarize what was approved / rejected / skipped

## Governance rules (from VAULT_CONSTITUTION.md)
- **Tier 2 paths** (`04-Knowledge/`, `05-Projects/`): require human approval (this command)
- **Tier 3 paths** (`00-Brain/`, `01-Agents/roles/`): BLOCKED — these require direct human edit
- **Low-risk items** (low_risk: true): can be merged without deep review, but still confirm

## Commands
- `/approve-inbox` — review all pending items
- `/approve-inbox --auto-low-risk` — auto-approve low_risk: true items, review the rest

## Alternative: Python script
```bash
python scripts/approve_inbox.py              # Interactive, dry-run
python scripts/approve_inbox.py --move       # Actually move files
python scripts/approve_inbox.py --auto-low-risk --move
```

---

## Execute

Read `06-Inbox/pending/` now. List all `.md` files. For each:

1. Show the frontmatter fields: `inbox_id`, `source_agent`, `confidence`, `proposed_location`, `rationale`, `low_risk`
2. Show first 300 chars of body
3. Ask: **[A]pprove / [R]eject / [S]kip?**
4. If approve: confirm the `proposed_location` is not a Tier 3 path. If Tier 3, block and explain.
5. After all items: show summary and remind human to run `python scripts/approve_inbox.py --move` to physically move files.

**Arguments:** $ARGUMENTS
