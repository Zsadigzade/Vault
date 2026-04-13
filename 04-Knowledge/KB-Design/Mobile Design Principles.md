---
tags: [kb, design, mobile, touch]
area: knowledge-base
updated: 2026-04-04
---

# Mobile design principles

> [!note] Stack tie-in: **Capacitor WebView** + **Tailwind** + **React**. Apply these in `className` and layout shells (e.g. safe areas).

---

## Touch targets

| Guideline | Detail |
|-----------|--------|
| **Minimum** | ~44×44 pt (Apple HIG) / 48×48 dp (Material) for tappable controls |
| **Spacing** | Adequate gap between adjacent targets to prevent mis-taps |
| **Hit slugs** | Small icons can use invisible padding (`min-h-11 min-w-11`, `p-2` on wrapper) |

**Tailwind example:** `min-h-11 min-w-11 flex items-center justify-center` on icon buttons.

---

## Thumb zones (one-handed use)

- **Easy:** Bottom third + center of screen (natural thumb arc)
- **Hard:** Top corners — avoid primary actions only there; use reachability or bottom sheets

**React pattern:** Sticky bottom nav / FAB for primary actions; destructive or rare actions in menus.

---

## Safe areas & notches

| Concern | Approach |
|---------|----------|
| **iOS home indicator** | `env(safe-area-inset-bottom)` — Tailwind: `pb-[env(safe-area-inset-bottom)]` or plugin |
| **Notch / Dynamic Island** | `padding-top: env(safe-area-inset-top)` on headers |
| **Landscape** | Re-test; side insets matter |

Capacitor: often set `viewport-fit=cover` in `index.html` and pad shell components.

---

## Density vs readability

- **Social feeds:** Prefer **scannable** rows — clear avatar, title, meta line
- **Avoid** cramming secondary actions into every row; use overflow menu

---

## Platform conventions

| Pattern | iOS | Android |
|---------|-----|---------|
| **Back** | Swipe from edge, top-left chevron | System back, sometimes bottom nav |
| **Actions** | Often top-right | FAB / bottom bar |
| **Sheets** | `UISheet` mental model | Bottom sheets common |

Hybrid apps: pick **one** primary pattern per flow; don’t mix paradigms in one screen without reason.

---

## See also

- [[Typography & Readability]] · [[Social App UI Patterns]] · [[Animation & Micro-interactions]] · [[Accessibility on Mobile (WCAG)]]
- [[Design Systems & Component Patterns]] · [[Curated GitHub Repositories]] § Design system components
- Project: [[User Preferences & Style]] · [[Keyboard & Layout]]
