---
tags: [kb, performance, lists, react]
area: knowledge-base
updated: 2026-04-04
---

# List virtualization

---

## When to virtualize

| Signal | Action |
|--------|--------|
| **100+** similar rows | Strong candidate |
| **Jank** on scroll | Profile; check expensive row components |
| **Images/video** in rows | Virtualize + lazy media |

---

## Libraries

| Library | Notes |
|---------|-------|
| **TanStack Virtual** | Headless — works with any markup |
| **react-window** | Mature, fixed/variable size |
| **react-virtuoso** | Good for chat/infinite scroll ergonomics |

---

## Infinite scroll + virtual

- **Append** pages to flat list; **stable keys**
- **Overscan** a few rows for smooth scroll
- **Scroll restore** on back navigation — see [[Feed & Infinite Scroll Patterns]]

---

## Measuring row height

- **Fixed height** simplest
- **Dynamic height** — measure/cache; avoid layout thrash ([[React Rendering Optimization]])

---

## See also

- [[Network & Caching Strategies]] (infinite queries) · [[Social App UI Patterns]]
