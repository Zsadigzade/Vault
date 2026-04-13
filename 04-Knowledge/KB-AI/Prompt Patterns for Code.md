---
tags: [kb, ai, prompting]
area: knowledge-base
updated: 2026-04-04
---

# Prompt patterns for code

---

## Structure

1. **Goal** — one sentence outcome  
2. **Constraints** — performance, a11y, “must not break X”  
3. **Context** — files, stack, environment  
4. **Acceptance** — tests to run, UX to verify  

---

## Few-shot

- Provide **one** minimal good example + **one** anti-pattern *don’t do this*

---

## Constraints that work

| Good | Vague |
|------|-------|
| “Use `useQuery`, keys from `queryKeys.ts`” | “Use best practices” |
| “Run `npx vitest run path` only” | “Add tests” |
| “No `git commit`” | “Be careful” |

---

## Chain-of-thought (light)

- Ask for **plan** first on risky changes — aligns with Cursor Plan mode

---

## Security prompts

- “**Threat model** this RPC” / “List **trust boundaries**” — see [[AI-Assisted Code Review]]

---

## See also

- [[AI-Assisted Code Review]] · [[Agent Debugging Strategies]]
