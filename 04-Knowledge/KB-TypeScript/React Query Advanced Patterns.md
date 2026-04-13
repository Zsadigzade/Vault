---
tags: [kb, react-query, tanstack, data-fetching]
area: knowledge-base
updated: 2026-04-04
---

# React Query advanced patterns

> [!tip] BRUH: keys live in `queryKeys.ts` — [[Data Layer]] · [[09 - Critical Gotchas]].

---

## Query factories

- Centralize **key + queryFn** for reuse across hooks/components

---

## Dependent queries

```ts
useQuery({ queryKey: ["post", id], enabled: !!id, queryFn: ... })
```

---

## Infinite queries

- `useInfiniteQuery` + **cursor** from server
- UX patterns: [[Feed & Infinite Scroll Patterns]]

---

## Optimistic updates

- `onMutate` snapshot → `onError` rollback → `onSettled` invalidate
- Keep rollback **cheap** for memes/media posts

---

## Prefetch

- `queryClient.prefetchQuery` on hover / route guard

---

## Stale vs fetching

- **`isPending`** first load vs **`isFetching`** background refresh — different skeleton UX ([[Loading & Skeleton States]])

---

## See also

- [[Network & Caching Strategies]] · [[Error Boundaries & Recovery]]
