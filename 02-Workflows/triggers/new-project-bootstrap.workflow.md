---
workflow_id: wf-new-project-bootstrap
trigger:
  type: manual
compatible_with: [python, claude-code]
roles: [CoS, CTO, CPO]
context_budget:
  max_tokens_total: 6000
  priority_files:
    - "00-Brain/VAULT_CONSTITUTION.md"
    - "Templates/Project Bootstrap.md"
steps:
  - id: step-01
    agent: CoS
    action: scaffold_folder
    params: { base: "05-Projects/", name: "{{project_slug}}" }
    output_var: project_path
  - id: step-02
    agent: CPO
    action: draft_home_md
    params: { project_path: "{{project_path}}" }
execution:
  status: idle
  last_run: null
---

# New project bootstrap

Creates `05-Projects/<slug>/` with `HOME.md`, `reference/`, empty feature folders — fill from [[Templates/Project Bootstrap]].
