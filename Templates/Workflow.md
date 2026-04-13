---
workflow_id: wf-example-001
trigger:
  type: manual
compatible_with: [python, claude-code]
roles: [CoS]
context_budget:
  max_tokens_total: 4000
  priority_files: []
steps:
  - id: step-01
    agent: CoS
    action: describe
    params: {}
    output_var: out
execution:
  status: idle
  last_run: null
---

# Workflow title

Describe human-readable flow here.
