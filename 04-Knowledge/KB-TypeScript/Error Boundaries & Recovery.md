---
tags: [kb, react, errors, sentry]
area: knowledge-base
updated: 2026-04-04
---

# Error boundaries & recovery

---

## Class boundary (React)

- Still required for **render** errors; hooks can’t catch child render throws

```tsx
class ErrorBoundary extends Component<{ fallback: ReactNode }, { err?: Error }> { ... }
```

---

## Placement

| Level | Use |
|-------|-----|
| **Route** | Full-page fallback + “Try again” |
| **Feature** | Isolate feed vs composer |
| **Leaf** | Rare — prefer inline error UI |

---

## Integration (Sentry)

- `Sentry.captureException` in `componentDidCatch`
- Provide **reset keys** to remount subtree after navigation

Project: [[Sentry]].

---

## What boundaries **don’t** catch

- **Event handlers** — use `try/catch`
- **Async** errors — handle in promise chain
- **SSR** streaming quirks — framework-specific

---

## UX

- **Don’t** wipe whole app for minor widget failure — [[Error State Design]]

---

## See also

- [[Agent Debugging Strategies]] · [[React 18 Concurrent Features]]
