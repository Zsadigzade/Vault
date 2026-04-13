---
tags: [kb, ai, review, security]
area: knowledge-base
updated: 2026-04-04
---

# AI-assisted code review

---

## Review prompt skeleton

```
You are reviewing a PR for a React + Supabase app.
Focus: security (RLS, auth), performance, a11y, error handling.
List: (1) blockers (2) suggestions (3) nits.
Cite files and line ranges. Assume client is untrusted.
```

---

## Security-focused questions

- “Where is **authorization** enforced beyond the UI?”
- “Can a user **forge** `user_id` in body?”
- “Any **secret** in client bundle?”

Cross-check: [[OWASP Mobile Top 10]] · [[Supabase Security Hardening]].

---

## Refactor prompts

- “**Preserve behavior** — list public API changes”
- “**Extract** hook; keep tests green”

---

## Limitations

- Models **hallucinate** — verify claims against code
- Run **tests** and **linters** — AI is additive, not replacement

---

## See also

- [[Prompt Patterns for Code]] · [[Testing Strategies & Patterns]]
