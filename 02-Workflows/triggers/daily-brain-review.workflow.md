---
workflow_id: wf-daily-brain-review
trigger:
  type: schedule
  schedule: "0 7 * * *"
compatible_with: [n8n, make, python, claude-code]
roles: [CoS]
context_budget:
  max_tokens_total: 4000
  priority_files:
    - "00-Brain/HOME.md"
    - "01-Agents/SESSION_HANDOFF.md"
steps:
  - id: step-01
    agent: CoS
    action: read_file
    params: { path: "01-Agents/SESSION_HANDOFF.md" }
    output_var: handoff_snapshot
  - id: step-02
    agent: CoS
    action: suggest_session_update
    params: { snapshot: "{{handoff_snapshot}}" }
    output_var: draft_delta
  - id: step-03
    agent: CoS
    action: write_inbox_note
    params:
      path: "06-Inbox/pending/"
      prefix: "daily-brain-review"
      low_risk: true
execution:
  status: idle
  last_run: null
---

# Daily brain review

Refresh [[SESSION_HANDOFF]] pointers; list orphan notes (if health data available). Output → `06-Inbox/pending/` draft for human merge.
