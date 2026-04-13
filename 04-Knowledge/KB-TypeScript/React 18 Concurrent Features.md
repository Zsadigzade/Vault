---
tags: [kb, react, concurrent, react-18]
area: knowledge-base
updated: 2026-04-04
---

# React 18 concurrent features

---

## `useTransition`

- Mark **non-urgent** state updates (e.g. filtering a large list) as transitions
- Keeps UI responsive for urgent input

```tsx
const [isPending, startTransition] = useTransition();
startTransition(() => setFilter(q));
```

---

## `useDeferredValue`

- **Defer** re-rendering expensive child with stale value briefly
- Good for search-as-you-type with heavy results

---

## Suspense for data (ecosystem)

- React Query + Suspense boundaries — coordinate with **fallback** UX ([[Loading & Skeleton States]])
- Error still needs **ErrorBoundary** — [[Error Boundaries & Recovery]]

---

## Batching

- React 18 **automatic batching** in more async contexts — fewer manual `flushSync` needs

---

## Pitfalls

- Don’t hide **critical** errors behind transitions
- **INP** — long synchronous work still hurts; split tasks ([[Core Web Vitals]])

---

## See also

- [[React Rendering Optimization]] · [[React Query Advanced Patterns]]
