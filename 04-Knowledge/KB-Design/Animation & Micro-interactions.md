---
tags: [kb, design, animation, motion]
area: knowledge-base
updated: 2026-04-04
---

# Animation & micro-interactions

---

## Motion budget

| Guideline | Detail |
|-----------|--------|
| **Purpose** | Motion explains **relationship** (where did that come from?) not decoration |
| **Duration** | Short on mobile: ~150–300ms for UI; avoid long easing on every tap |
| **Reduce motion** | Respect `prefers-reduced-motion: reduce` — offer non-animated fallback |

```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

Tailwind: `motion-reduce:transition-none` where applicable.

---

## What to animate

| Good | Risky |
|------|--------|
| Opacity, transform (`translate`, `scale`) | `height: auto` (layout thrash) |
| `transform-gpu` / `will-change` sparingly | Large blurs on huge areas (GPU cost) |

**Lists:** prefer **CSS** or **layout animation libs** that FLIP; for long lists see [[List Virtualization]].

---

## React patterns

- **Mount/unmount:** Radix + `tailwindcss-animate` / `data-[state=open]:`
- **Route transitions:** keep subtle in Capacitor — native already has transition expectations

---

## Haptics vs animation

Pair subtle **visual** feedback with optional **haptic** on success — see [[Haptic & Native Feedback]].

---

## See also

- [[Mobile Design Principles]] · [[Social App UI Patterns]] · [[Performance & Debugging Tools]] (FPS profiling)
- Repos: [motiondivision/motion](https://github.com/motiondivision/motion) · [pmndrs/use-gesture](https://github.com/pmndrs/use-gesture) — [[Curated GitHub Repositories]]
