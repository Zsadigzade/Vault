---
tags: [kb, ux, loading, skeleton]
area: knowledge-base
updated: 2026-04-04
---

# Loading & skeleton states

---

## Skeleton vs spinner

| Skeleton | Spinner |
|----------|---------|
| Known layout (feed cards) | Indeterminate tiny action |
| Reduces perceived wait | OK for &lt;300ms if unavoidable |

---

## React patterns

- **`Suspense`** boundaries around lazy routes / async components
- **React Query** `isPending` / `isFetching` — distinguish **initial** vs **background** refresh (show subtle bar, not full skeleton)

See [[React Query Advanced Patterns]] · [[Data Layer]].

---

## Optimistic UI

- **Like**, **follow**: update UI immediately; rollback on error + toast

---

## Stale-while-revalidate

- Show **cached** data instantly; refresh quietly — [[Network & Caching Strategies]]

---

## Timeouts

- If >10s: offer **cancel** / **retry** — don’t infinite spinner

---

## See also

- [[Error State Design]] · [[Core Web Vitals]] (LCP perception)
