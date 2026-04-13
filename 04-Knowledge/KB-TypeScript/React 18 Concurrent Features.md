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

## React 18/19 Patterns — 2026-04-13

- **Automatic batching** — state updates in async callbacks/timeouts now batched by default (React 18)
- **Transitions** (`useTransition`) — mark updates as non-urgent; keeps UI responsive during heavy renders
- **Suspense** — declarative loading states; pairs with `React.lazy()` for code splitting
- **React Server Components** — server-side rendering with zero client JS for static subtrees
- **React 19** — `use()` hook for promises/context; Actions API for form mutations
- Source: [Vercel R18 perf post](https://vercel.com/blog/how-react-18-improves-application-performance), [React 18→19 guide](https://medium.com/@mjshaikh1175/react-18-to-react-19-major-features-and-updates-you-need-to-know-b907cb3f312a)
