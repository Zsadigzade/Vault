---
tags: [kb, design, typography, readability]
area: knowledge-base
updated: 2026-04-04
---

# Typography & readability

---

## Type scale (mobile)

| Role | Typical range | Notes |
|------|----------------|-------|
| **Display / hero** | 28–34px | Short lines only |
| **Title** | 20–24px | Post titles, sheet headers |
| **Body** | 16–18px | **Avoid &lt;16px** for long reading on phones |
| **Caption / meta** | 12–14px | Secondary only; maintain contrast (see [[Color & Contrast Accessibility]]) |

Use **rem**-based tokens in Tailwind config so zoom / accessibility settings behave well.

---

## Line length & height

- **Line length:** ~45–75 characters comfortable for reading (wider OK for feed **snippets**)
- **Line height:** Body `leading-relaxed` (~1.5); tight headings `leading-tight`

---

## Font loading (web / Capacitor)

| Practice | Detail |
|----------|--------|
| **`font-display: swap`** | Reduces invisible text flash |
| **Subset weights** | Load only used weights (variable fonts = fewer files) |
| **Preload** critical display face in `index.html` if LCP is text-heavy |

BRUH: Plus Jakarta + Bricolage Grotesque — keep subsetting in mind for bundle.

---

## Hierarchy without shouting

1. **Size** + **weight** before color
2. One **primary** action per view hierarchy level
3. **Truncate** with `line-clamp-*` + full text on detail screen

---

## Dynamic type / accessibility

- Respect user zoom (`maximum-scale` not locked to 1 on BRUH)
- Test **200% zoom** layouts — flex + wrap, not fixed pixel heights for text blocks

See [[Accessibility on Mobile (WCAG)]].

---

## See also

- [[Mobile Design Principles]] · [[Social App UI Patterns]]
