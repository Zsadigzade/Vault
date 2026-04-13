---
tags: [agents, orchestration, multi-agent]
area: agents
updated: 2026-04-13
tldr: "Handoff YAML, parallel vs sequential, CoS synthesis caps tokens."
---

# Multi-agent orchestration protocol

## Handoff object (YAML)

```yaml
handoff:
  from_role: CTO
  to_role: CISO
  task_id: "task-2026-04-13-001"
  summary: "One paragraph max."
  decisions_made: ["bullet"]
  open_questions: ["bullet"]
  context_tokens_used: 1200
```

## Rules

1. **CoS** (or human) owns merge order and conflict resolution.
2. **Parallel:** each role stays within `output_format.max_tokens` in its role file.
3. **Sequential:** downstream role receives only `handoff` + links to prior artifacts (not full logs).
4. **Vault writes:** proposals go to `06-Inbox/pending/` unless [[VAULT_CONSTITUTION]] low-risk allowlist applies.

## Ollama / cloud

- Per-role `endpoint:` in frontmatter: `http://localhost:11434` (laptop) or `https://ollama.yourdomain/v1` (VPS behind TLS + auth).
- Fallback model in `model_fallback:` when local model missing.

## Synthesis template (CoS)

- **Summary** (3 bullets)
- **Agreed decisions**
- **Dissent / risks**
- **Next actions** (owner + due if known)
