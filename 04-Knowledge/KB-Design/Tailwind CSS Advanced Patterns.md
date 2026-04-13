---
tags: [kb, design, tailwind, css]
area: knowledge-base
updated: 2026-04-04
---

# Tailwind CSS advanced patterns

> [!tip] BRUH uses **Tailwind** + **React**. Prefer utilities in JSX; use `@apply` sparingly in CSS layers.

---

## Composition over custom CSS

| Approach | When |
|----------|------|
| **Utilities in `className`** | Default — colocated with component |
| **`clsx` / `cn()` helper** | Conditional variants, merged classes |
| **`@apply` in `@layer components`** | Repeated **identical** clusters (e.g. one “card” primitive) |

> [!warning] Heavy `@apply` stacks duplicate breakpoint/dark variants poorly — harder to grep than JSX.

---

## Responsive & container queries

- **Mobile-first:** unprefixed = small; `sm:`, `md:`, `lg:` scale up
- **Touch:** `active:` states for press feedback on mobile WebView
- **Container queries** (v4 / plugin): useful for **reusable** cards inside variable-width parents

```tsx
// Example: cn pattern
<div className={cn("flex gap-2", isActive && "bg-white/10")} />
```

---

## Arbitrary values

- Use `min-h-[env(safe-area-inset-bottom)]` when plugins don’t expose env()
- Prefer **design tokens** (`spacing` in config) over magic numbers repeated 20×

---

## Dark mode (overview)

- **`class` strategy:** `dark:` variants; toggle `class` on `<html>`
- **`media` strategy:** respects OS only

Detail: [[Dark Mode Implementation]].

---

## Performance

| Tip | Why |
|-----|-----|
| **JIT** | Unused utilities stripped in build |
| **Avoid huge dynamic strings** | Some patterns defeat purge — prefer safelist or static branches |
| **SVG / icons** | Sprite or icon components vs thousands of inline paths |

---

## Radix + Tailwind

- Style **slots** via `className` on `Slot`/`asChild` patterns
- Use **data attributes** Radix sets (`data-state=open`) for animations: `data-[state=open]:animate-in`

See [[Design Systems & Component Patterns]].

---

## See also

- [[Color & Contrast Accessibility]] · [[Animation & Micro-interactions]]
- Project: [[User Preferences & Style]] (`--ig-*`, gradients)
