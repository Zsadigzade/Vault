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

## UI/UX Trends 2025/2026 — 2026-04-13

- **Liquid Glass (iOS 26 / WWDC 2025)** — Apple introduced across iOS 26, macOS Tahoe; translucent layered surfaces replacing flat cards
- **Bento layouts** — iOS 17 widgets + Fluent UI set the stage; grid-based modular information display
- **Expressive typography** — large headlines, custom fonts, striking text layouts as primary design element
- **AI-driven personalization** — dynamic UI adapting to user behavior; companies without this falling behind
- Source: [Chop Dawg 2025](https://www.chopdawg.com/ui-ux-design-trends-in-mobile-apps-for-2025/), [DEV.to complete guide](https://dev.to/krlz/mobile-app-trends-2025-the-complete-developer-guide-to-uiux-ai-and-beyond-5265)
