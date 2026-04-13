---
tags: [kb, react, composition, radix]
area: knowledge-base
updated: 2026-04-04
---

# Component composition patterns

---

## Compound components

- `Tabs`, `Tabs.List`, `Tabs.Trigger` — shared implicit state via context

---

## `asChild` / `Slot` (Radix)

- Merge props onto single child — avoids extra DOM

---

## Render props vs hooks

| Hooks | Render props |
|-------|--------------|
| Preferred in modern React | Legacy libraries, fine when needed |
| Easier composition | Explicit injection |

---

## Controlled wrappers

- **Controlled** + **uncontrolled** modes — document default values

---

## List items

- Pass **`renderItem`** or **children function** for flexible row rendering in virtualized lists ([[List Virtualization]])

---

## See also

- [[Design Systems & Component Patterns]] · [[Custom Hook Patterns]]
