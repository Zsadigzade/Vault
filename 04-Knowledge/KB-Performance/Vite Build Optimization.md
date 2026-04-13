---
tags: [kb, performance, vite, build]
area: knowledge-base
updated: 2026-04-04
---

# Vite build optimization

---

## Chunk strategy

| Goal | Approach |
|------|----------|
| **Stable vendor chunk** | `manualChunks` in `build.rollupOptions.output` for large deps |
| **Avoid one giant vendor** | Split `react`, `react-dom`, heavy analytics separately |

---

## Dependency pre-bundling

- Vite **pre-bundles** deps — rare ESM/CJS issues: `optimizeDeps.include` / `exclude`

---

## Analyze bundle

- `vite-bundle-visualizer` or Rollup plugin after `npm run build`
- Find **unexpected** large strings or locales

---

## Source maps

- **Production:** hidden source maps for Sentry only — don’t ship public full maps

Project: [[Sentry]].

---

## Environment

- **Drop debug** code with `import.meta.env.PROD` guards

---

## See also

- [[Bundle Size & Code Splitting]] · [[Performance & Debugging Tools]]

## Vite 6 Optimization — 2026-04-13

- **Code splitting + tree shaking** — reduces build time 70% (Vite 6 guide); lazy-load routes keeps main bundle lean
- **esbuild parallelism** — enable for heavy plugins/transformations; already multi-threaded by default
- **Manual chunks** — split large deps (e.g. `lucide-react`) into separate vendor chunks to improve cache hit rate
- **Rollup under the hood** — configure `build.rollupOptions.output.manualChunks` for fine-grained splitting
- Source: [Vite 6 guide](https://markaicode.com/vite-6-build-optimization-guide/), [React Vite Jan 2026](https://medium.com/@salvinodsa/optimizing-react-builds-with-vite-practical-techniques-for-faster-apps-063d4952e67d)
