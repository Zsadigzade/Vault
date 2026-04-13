---
tags: [kb, ux, errors, empty-states]
area: knowledge-base
updated: 2026-04-04
---

# Error state design

---

## Principles

| Principle | Implementation |
|-----------|----------------|
| **Human language** | “Couldn’t load posts” not `500` |
| **Recovery** | Primary **Retry** button |
| **Context** | Offline vs server vs auth expired |

---

## Empty vs error

| State | UX |
|-------|-----|
| **Empty** (no data yet) | Illustration + CTA (“Create first post”) |
| **Error** | Explain + retry; link to support if persistent |

---

## Toasts vs inline

| Toasts | Inline |
|--------|--------|
| Non-blocking confirmation | Form field errors |
| Background sync failed | Whole page failed load |

---

## Auth errors

- **Session expired** — clear CTA to re-login; preserve return path

Project: [[Authentication]].

---

## Logging

- Client message ≠ Sentry payload — [[Sentry]] gets stack + tags

---

## See also

- [[Mobile UX Heuristics]] · [[Form Design & Validation]] · [[Incident Response & Debugging]]
