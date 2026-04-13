---
tags: [kb, design, radix, components, react]
area: knowledge-base
updated: 2026-04-14
---

# Design systems & component patterns

---

## Radix UI (headless)

| Benefit | Detail |
|---------|--------|
| **A11y** | Focus trap, keyboard, ARIA for dialogs/menus |
| **Composition** | `asChild` merges props onto child (e.g. `Slot`) |

**Tailwind styling:** target `data-[state=open]`, `data-[disabled]` for visual states.

---

## Compound components

```tsx
// Pattern: static properties on namespace
Card.Root, Card.Header, Card.Body
```

- **Pros:** Flexible layout, single import surface
- **Cons:** Need clear docs — agents grep for `Card.`

---

## Controlled vs uncontrolled

| Use controlled when | Use uncontrolled when |
|---------------------|----------------------|
| URL state, multi-step wizards | Simple local forms |
| Sync with server / React Query | Leaf inputs with `defaultValue` |

---

## Slots pattern

- **`asChild`:** one child receives merged props — avoid wrapper divs
- Ensure **single** React element child

---

## Styling boundaries

| Layer | Responsibility |
|-------|----------------|
| **Primitives** | Button, Input — tokens only |
| **Features** | Compose primitives + domain logic |

Avoid **prop explosion** (`variant` enums) without design need; prefer composition.

---

## See also

- [[Component Composition Patterns]] · [[Accessibility on Mobile (WCAG)]] · [[Social App UI Patterns]]
- Project: [[App Architecture]] (shell / providers)
- Repos: [shadcn-ui/ui](https://github.com/shadcn-ui/ui) · [radix-ui/primitives](https://github.com/radix-ui/primitives) · [tailwindlabs/headlessui](https://github.com/tailwindlabs/headlessui) — [[Curated GitHub Repositories]]
- **shadcn in Cursor:** registry MCP — [[Cursor Tips & Power Features]] · [ui.shadcn.com/docs/mcp](https://ui.shadcn.com/docs/mcp)
