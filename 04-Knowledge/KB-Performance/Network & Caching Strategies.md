---
tags: [kb, performance, network, react-query]
area: knowledge-base
updated: 2026-04-04
---

# Network & caching strategies

---

## React Query (TanStack Query)

| Knob | Use |
|------|-----|
| **`staleTime`** | Data fresh enough — avoid refetch spam |
| **`gcTime` (cacheTime)** | How long inactive data stays in memory |
| **`placeholderData` / `initialData`** | Instant UI from cache |
| **`prefetchQuery`** | Hover / route anticipate |

Detail: [[React Query Advanced Patterns]] · project [[Data Layer]].

---

## HTTP caching (static assets)

- **Immutable** hashed assets + `Cache-Control: max-age=31536000, immutable`
- **HTML** short TTL or revalidate — ensures new JS picked up

---

## Supabase / API

- **Pagination** (cursor/keyset) over huge offsets — see [[Query Patterns & Anti-Patterns]]
- **Debounce** search; **abort** in-flight `fetch` on query change (`AbortSignal`)

---

## Offline / flaky mobile

- **Optimistic updates** with rollback on error
- **Queue** writes carefully — idempotency on server

---

## See also

- [[Capacitor Native Performance]] · [[Core Web Vitals]]
