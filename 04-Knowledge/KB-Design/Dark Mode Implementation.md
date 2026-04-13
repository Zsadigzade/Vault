---
tags: [kb, design, dark-mode, tailwind]
area: knowledge-base
updated: 2026-04-04
---

# Dark mode implementation

---

## Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| **`media`** (`prefers-color-scheme`) | Zero state; matches OS | No in-app override |
| **`class` on `html`** | User toggle + persistence | Must sync on load (flash risk) |
| **Hybrid** | Default `media`, optional override → `class` | More logic |

**Tailwind v3+:** `darkMode: 'class'` or `'media'` in `tailwind.config`.

---

## Avoid flash of wrong theme

1. **Inline script** in `index.html` before paint: read `localStorage` / system pref → set `class="dark"` early
2. **CSS variables** for surfaces: swap token values per theme instead of duplicating every utility

---

## Semantic tokens

Prefer **`bg-surface`**, **`text-primary`** (mapped in CSS) over raw `bg-gray-900` everywhere — easier to tune dark palette.

---

## Images & video

- **Icons:** currentColor or SVG variants per theme
- **Photos:** optional slight **brightness** reduction in dark mode (careful with banding)

---

## Testing

- OLED black vs dark gray (#000 vs #121212) — banding, smear, readability
- **Contrast:** [[Color & Contrast Accessibility]]

---

## See also

- [[Tailwind CSS Advanced Patterns]] · [[Color & Contrast Accessibility]]
