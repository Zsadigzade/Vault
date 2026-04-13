---
role: ROLE_KEY
role_name: "Full Name"
agent_id: agent-rolekey
model: ollama/llama3.3
model_fallback: claude-sonnet-4-6
endpoint: http://localhost:11434
temperature: 0.35
owns_domains: [domain1, domain2]
reads_on_activation:
  - "00-Brain/HOME.md"
  - "00-Brain/VAULT_CONSTITUTION.md"
  - "01-Agents/SESSION_HANDOFF.md"
decision_scope:
  owns: []
  defers_to: {}
output_format:
  structure: brief-name
  max_tokens: 700
  required_sections: [Summary, Next Actions]
can_propose_inbox: true
can_write_core: false
status: draft
---

# Role: {{title}}

## TL;DR

-
