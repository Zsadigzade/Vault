---
tags: [kb, performance, memory, debugging]
area: knowledge-base
updated: 2026-04-04
---

# Memory leaks & profiling

---

## Common React leaks

| Cause | Fix |
|-------|-----|
| **Subscriptions** not cleaned | `useEffect` return cleanup (`unsubscribe`, `clearInterval`) |
| **Global caches** growing | Cap `Map` size or use LRU |
| **Closures** holding large objects | Narrow deps; avoid capturing whole store |
| **Detached DOM** (charts, maps) | Destroy instance on unmount |

---

## DevTools (Chrome / Safari Web Inspector)

- **Heap snapshot** — compare before/after navigation
- **Performance** — record interaction, spot long tasks

---

## React DevTools

- **Profiler** — commit count, why re-render
- **⚠️** “Why did this render?” for `memo` mismatches

---

## Listeners in Capacitor

- Remove **App**/`Keyboard` listeners on unmount

---

## See also

- [[Agent Debugging Strategies]] · [[React Rendering Optimization]] · [[Sentry]] (OOM less visible — watch breadcrumbs)
