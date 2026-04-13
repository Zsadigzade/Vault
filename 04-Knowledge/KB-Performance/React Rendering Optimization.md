---
tags: [kb, performance, react]
area: knowledge-base
updated: 2026-04-04
---

# React rendering optimization

---

## When **not** to optimize

> [!tip] Premature `memo`/`useCallback` adds noise and bugs. Profile first ([[Memory Leaks & Profiling]]).

- Small leaf components
- Lists already virtualized ([[List Virtualization]])
- State colocated so parent doesn’t re-render unnecessarily

---

## `React.memo`

| Use | Skip |
|-----|------|
| Pure list rows receiving stable props | Component re-renders cheaply |

```tsx
export const Row = memo(function Row(props: RowProps) { ... });
```

---

## `useMemo` / `useCallback`

| `useMemo` | `useCallback` |
|-----------|----------------|
| Expensive derived data | Stable function ref for `memo` children / effect deps |

**Rule:** If dependency array is huge or always changing, memoization **fails** — fix architecture.

---

## Context performance

- **Split context** — don’t put fast-changing state next to slow in one context
- Prefer **React Query** for server state ([[React Query Advanced Patterns]]) over prop-drilling global state

---

## Key stability

- **Never** use array index as key for **reorderable** lists
- Stable IDs from server

---

## Concurrent-friendly updates

See [[React 18 Concurrent Features]] — `startTransition` for non-urgent updates.

---

## See also

- [[Bundle Size & Code Splitting]] · [[List Virtualization]] · [[Network & Caching Strategies]]
