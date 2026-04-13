---
workflow_id: wf-weekly-health-check
trigger:
  type: schedule
  schedule: "0 8 * * 1"
compatible_with: [n8n, make, python, claude-code]
roles: [CoS, CTO]
context_budget:
  max_tokens_total: 8000
  priority_files:
    - "00-Brain/SITEMAP.md"
    - "07-Learning/VAULT_HEALTH.md"
steps:
  - id: step-01
    agent: CoS
    action: run_script
    params: { script: "vault_health.py", args: ["--output-inbox"] }
    output_var: health_report_path
  - id: step-02
    agent: CoS
    action: append_learning_log
    params: { note: "Weekly health run complete" }
execution:
  status: idle
  last_run: null
---

# Weekly health check

Runs `vault_health.py`; appends metrics to inbox and suggests [[VAULT_HEALTH]] updates.
