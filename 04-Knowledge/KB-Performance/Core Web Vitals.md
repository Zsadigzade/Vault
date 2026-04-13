---
tags: [kb, performance, cwv, web-vitals]
area: knowledge-base
updated: 2026-04-04
---

# Core Web Vitals

---

## Metrics (web)

| Metric | Meaning |
|--------|---------|
| **LCP** | Largest Contentful Paint — loading performance |
| **INP** | Interaction to Next Paint (replaces FID focus) — responsiveness |
| **CLS** | Cumulative Layout Shift — visual stability |

---

## Capacitor / hybrid nuance

- **Lighthouse** on **deployed** URL still useful for PWA shell
- Native shell: **first meaningful paint** in WebView + **time-to-interactive** for bridge-heavy flows

---

## Improve LCP

- Optimize hero image ([[Image & Media Optimization]])
- Preload critical font
- Reduce blocking JS — [[Bundle Size & Code Splitting]]

---

## Improve INP

- Break up long tasks (`scheduler.postTask`, `startTransition`)
- Avoid **main-thread** work on tap — debounce heavy work

See [[React 18 Concurrent Features]].

---

## Improve CLS

- Reserve space for images/skeletons
- Avoid inserting banners above content without layout shift

---

## See also

- [[Performance & Debugging Tools]] · [[React Rendering Optimization]]
