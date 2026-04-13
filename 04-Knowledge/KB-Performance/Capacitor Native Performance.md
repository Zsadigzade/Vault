---
tags: [kb, performance, capacitor, webview]
area: knowledge-base
updated: 2026-04-04
---

# Capacitor native performance

---

## Bridge overhead

| Issue | Mitigation |
|-------|------------|
| **Chatty** native calls | Batch reads/writes; avoid per-frame bridge traffic |
| **Large JSON** | Serialize once; prefer file URLs for big blobs |

---

## WebView

- **iOS WKWebView** — warm start vs cold; avoid huge synchronous JS on startup
- **Android** — System WebView updates matter; test low-end devices

---

## Splash & perceived perf

- **Native splash** until first paint ready — align with app shell
- Don’t block UI on **non-critical** SDK init (defer analytics)

Project: [[Startup Sequence & Storage Keys]].

---

## Keyboard & layout

- Project uses **`adjustNothing`** + CSS `--kbd-h` — wrong resize mode tanks UX perf ([[Keyboard & Layout]]).

---

## Plugins

- Load **heavy** plugins lazily on feature entry

---

## See also

- [[Core Web Vitals]] · [[Memory Leaks & Profiling]] · [[Bundle Size & Code Splitting]]
