---
tags: [kb, ai, debugging]
area: knowledge-base
updated: 2026-04-04
---

# Agent debugging strategies

---

## Reproduce first

| Step | Action |
|------|--------|
| 1 | Minimal repro path (platform, build, user state) |
| 2 | Capture **logs** / **HAR** / **Sentry** event |
| 3 | Bisect **git** if regression |

Project: [[Incident Response & Debugging]] · [[Sentry]].

---

## With an agent

- Provide **expected vs actual** + **one** failing test output
- Ask for **hypothesis list** ranked by likelihood — then verify top item **manually**

---

## Log analysis

- **Trim** noise; anchor on **first** error, not cascading failures
- **Correlate** client + Edge Function + Postgres logs (timestamp)

---

## Performance

- **Profile** before asking for micro-optimizations — [[Memory Leaks & Profiling]]

---

## When agents struggle

- **Narrow** file scope; paste **signature** of functions involved
- Switch to **Plan mode** for architectural uncertainty

---

## See also

- [[Cursor Tips & Power Features]] · [[Context Window Management]] · [[Testing Strategies & Patterns]]
