Run a vault automation workflow.

## Usage
`/run-workflow [workflow-id]`

Examples:
- `/run-workflow inbox-triage` — process pending inbox items
- `/run-workflow vault-health` — generate vault health report
- `/run-workflow daily-review` — daily brain review
- `/run-workflow new-project` — bootstrap a new project namespace

## What this does
1. Read the workflow file from `02-Workflows/triggers/` matching the ID
2. Parse the YAML frontmatter to get steps, roles, and context budget
3. Execute each step in order, invoking the specified role for each
4. Log the run to `07-Learning/OUTCOMES_LEDGER.md`
5. Propose any vault changes to `06-Inbox/pending/`

## Available workflows

Read `02-Workflows/WORKFLOW_REGISTRY.md` for the full list. Core workflows:

| Short name | Workflow ID | Trigger |
|-----------|-------------|---------|
| `inbox-triage` | wf-inbox-triage-001 | 8:30am daily |
| `vault-health` | wf-vault-health-001 | Monday 9am |
| `daily-review` | wf-daily-brain-review-001 | Daily |
| `knowledge-capture` | wf-knowledge-capture-001 | Manual |
| `new-project` | wf-new-project-bootstrap-001 | Manual |

## Alternative: Python script
```bash
python scripts/run_workflow.py --id [workflow-id]
python scripts/run_workflow.py --list
python scripts/run_workflow.py --id [workflow-id] --dry-run
```

---

Now execute: **$ARGUMENTS**

Read `02-Workflows/WORKFLOW_REGISTRY.md` first. Find the workflow that matches the argument (by short name or ID). Then execute its steps following the [[ORCHESTRATION_PROTOCOL]].
