---
tags: [kb, ux, feeds, infinite-scroll]
area: knowledge-base
updated: 2026-04-04
---

# Feed & infinite scroll patterns

---

## Pagination UX

| Pattern | Pros | Cons |
|---------|------|------|
| **Infinite scroll** | Seamless browsing | Hard to reach footer |
| **Load more** | User control | Extra tap |
| **Tabs + cursor** | Fast switching | State per tab |

---

## Scroll position restore

- On **back** from detail: restore prior scroll — store offset or first visible id
- With **virtualization** — library support required ([[List Virtualization]])

---

## “New posts” indicator

- **Non-blocking** chip at top — tap to jump to newest
- Avoid **auto-jump** while user is reading (jarring)

---

## Pull to refresh

- **Standard** on mobile feeds; show **subtle** progress
- Combine with React Query `refetch` — [[React Query Advanced Patterns]]

---

## End of feed

- **You’re all caught up** message — satisfying closure

---

## Performance

- **Prefetch** next page near bottom — [[Network & Caching Strategies]]

---

## See also

- [[Social App UI Patterns]] · [[Loading & Skeleton States]] · [[Social App Engagement Patterns]]
