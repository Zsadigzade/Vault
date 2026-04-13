---
tags: [workflows, overrides]
area: meta
updated: 2026-04-13
tldr: "Pause flags for automations."
---

# Workflow overrides (human-controlled)

Edit this file to pause jobs without deleting workflow definitions.

```yaml
pauses:
  ingest_rss:
    paused_until: null   # ISO date or null
  weekly_health:
    paused_until: null
```

When `paused_until` is a future date, `run_workflow.py` skips that workflow.
