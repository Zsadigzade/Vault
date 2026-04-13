---
tags: [kb, design, inspiration, webgl, react, motion, agent:topic]
area: knowledge-base
topic: design-inspiration
updated: 2026-04-13
---

# Developer design inspiration & motion tools

> **BRUH** is mobile-first; these sites help **web** polish, **marketing** landings, and **component** ideas. **Browsing** needs **no API keys**. **Accounts** may be required for **save / export / community upload** on 3D tools — check each product’s terms.

## Picks (your list)

| Site | URL | What it is | Keys / signup |
|------|-----|------------|----------------|
| **Godly** | [godly.website](https://godly.website/) | Curated **high-quality web** design references | Browse free; newsletter optional |
| **Unicorn Studio** | [unicorn.studio](https://www.unicorn.studio/) | **No-code WebGL** / interactive scenes | Product account likely for projects/hosting — verify pricing |
| **Spline Community** | [community.spline.design](https://community.spline.design/) | **3D** scenes, templates, remix | **Login** for community features |
| **React Bits** | [reactbits.dev](https://reactbits.dev/) | **Animated React** UI patterns / snippets | Dev usage; check **license** per snippet before ship |

## Similar (no API for inspiration)

| Site | URL | Notes |
|------|-----|--------|
| **Mobbin** | [mobbin.com](https://mobbin.com/) | Mobile UI patterns — paid tiers |
| **Dribbble** | [dribbble.com](https://dribbble.com/) | Visual exploration — accounts for interaction |
| **Awwwards** | [awwwards.com](https://awwwards.com/) | Award sites — trend reference |
| **Landingfolio** | [landingfolio.com](https://landingfolio.com/) | Landing page examples |

## Implementation tips (BRUH context)

- **Godly / Dribbble / Awwwards:** steal **layout rhythm**, typography pairing, **CTA** hierarchy — translate to **Tailwind** + Radix; test **contrast** ([[Color & Contrast Accessibility]]).
- **React Bits:** copy patterns into **`src/components/`**; prefer **tree-shaken** code; watch bundle size ([[Bundle Size & Code Splitting]]).
- **Spline / Unicorn:** export assets or embed only if **perf + privacy** OK; **Capacitor WebView** limits heavy WebGL on low-end devices — prefer **static** or **Lottie** for critical paths ([[Capacitor Native Performance]]).

## See also

- [[Component & motion libraries — compact]] · [[Social App UI Patterns]] · [[Animation & Micro-interactions]] · [[Mobile Design Principles]]
- [[📚 Knowledge Base]] · [[🏠 Home]]
