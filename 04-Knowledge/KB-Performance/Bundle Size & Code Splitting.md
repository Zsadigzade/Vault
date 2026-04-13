---
tags: [kb, performance, bundle, vite]
area: knowledge-base
updated: 2026-04-04
---

# Bundle size & code splitting

---

## Route-level splitting

```tsx
const Admin = lazy(() => import("./pages/Admin"));
```

Wrap with `<Suspense fallback={...}>`.

---

## Library splitting

| Strategy | Detail |
|----------|--------|
| **Dynamic import** heavy editors, charts | Load on first use |
| **Tree-shakeable ESM** | Prefer `lodash-es` / per-fn imports vs whole lodash |
| **Analyze** | `rollup-plugin-visualizer` / Vite bundle report — see [[Vite Build Optimization]] |

---

## Duplication

- Watch for **multiple versions** of same lib in lockfile (`npm why pkg`)

---

## Capacitor

- Smaller JS = faster **OTA** ([[OTA Update Strategies]]) and cold start

---

## See also

- [[Vite Build Optimization]] · [[Image & Media Optimization]]
