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
