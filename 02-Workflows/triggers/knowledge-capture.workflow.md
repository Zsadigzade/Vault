---
workflow_id: wf-knowledge-capture
trigger:
  type: event
compatible_with: [n8n, make, python]
roles: [CoS]
context_budget:
  max_tokens_total: 4000
  priority_files:
    - "04-Knowledge/SOURCE_REGISTRY.md"
    - "06-Inbox/INBOX_PROTOCOL.md"
steps:
  - id: step-01
    agent: CoS
    action: fetch_url_or_feed
    params: { url: "{{source_url}}" }
    output_var: raw_capture
  - id: step-02
    agent: CoS
    action: write_inbox_note
    params:
      path: "06-Inbox/pending/"
      template: "_Sources/CITATION_BLOCK"
      body: "{{raw_capture}}"
execution:
  status: idle
  last_run: null
---

# Knowledge capture

Research → **inbox first** with citation block ([[SOURCE_REGISTRY]] for trusted tiers).
