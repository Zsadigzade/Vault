---
tags: [workflows, automation, spec]
area: meta
updated: 2026-04-13
tldr: "YAML frontmatter + markdown steps; n8n/Make/Python/Cursor compatible."
---

# Workflow file spec

## Frontmatter keys

- `workflow_id` — stable id, e.g. `wf-inbox-triage-001`
- `trigger` — `type: schedule | event | manual | webhook | file-watch` + params (`schedule` cron, etc.)
- `compatible_with` — e.g. `[n8n, make, python, claude-code]`
- `roles` — C-suite roles involved
- `context_budget` — `max_tokens_total`, `priority_files`
- `steps` — list of `{ id, agent, action, params, output_var }`
- `execution` — `status`, `last_run` (updated by runner)

## Body

Human-readable description + step detail + failure handling.

## Location

Store under `02-Workflows/triggers/*.workflow.md`.

## Runner

`vault-automation/run_workflow.py --id <workflow_id>` parses YAML between first `---` pair.
