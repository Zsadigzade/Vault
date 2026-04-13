---
workflow_id: wf-inbox-triage-001
trigger:
  type: schedule
  schedule: "30 8 * * *"
compatible_with: [n8n, make, python, claude-code]
roles: [CoS]
context_budget:
  max_tokens_total: 8000
  priority_files:
    - "00-Brain/HOME.md"
    - "01-Agents/DISPATCHER.md"
    - "06-Inbox/INBOX_PROTOCOL.md"
steps:
  - id: step-01
    agent: CoS
    action: list_directory
    params: { path: "06-Inbox/pending/" }
    output_var: inbox_items
  - id: step-02
    agent: CoS
    action: classify
    params: { items: "{{inbox_items}}" }
    output_var: routing
execution:
  status: idle
  last_run: null
---

# Inbox triage

Classify `06-Inbox/pending/` items → proposed `04-Knowledge/` or `05-Projects/` paths; human batch approves via `approve_inbox.py`.
