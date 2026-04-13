---
inbox_id: inbox-{{date}}-{{sequence}}
status: pending
proposed_location: "04-Knowledge/{{KB-folder}}/{{filename}}.md"
confidence: 0.80
source_agent: {{role or "human"}}
source_url: ""
retrieved_at: "{{date}}"
low_risk: false
human_gate: required
rationale: "{{One sentence: why this is worth keeping}}"
related_notes:
  - "{{path/to/related.md}}"
tags: [inbox, {{domain}}]
area: inbox
created: {{date}}
---

# {{Title of proposed note}}

> **Proposed location:** `{{proposed_location}}`
> **Rationale:** {{rationale}}

---

## Content

{{The actual content being proposed for the knowledge base}}

---

## Review checklist (human)

- [ ] Content is accurate and not outdated
- [ ] Source is credible (URL/book checked)
- [ ] No secrets or credentials in content
- [ ] Proposed location is correct
- [ ] Tags are appropriate

**Approve:** move to `approved/` and then to proposed location
**Reject:** move to `archive/` with note: `rejection_reason: "{{why}}"`
