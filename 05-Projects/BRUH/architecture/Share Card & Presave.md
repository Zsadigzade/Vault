---
tags: [architecture, share, canvas, performance, create]
area: architecture
updated: 2026-04-03
---

# Share Card & Presave

> [!note] Fast path for **posting card** share: background presave + synchronous encode. Confirmed pattern from `memory/share_latency_fix.md` / OTA ~1.0.32.

---

## Key files

| File | Role |
|------|------|
| `src/lib/storyCardGenerator.ts` | `presavePostingCard`, `encodeCanvas`, `sharePostingCard` |
| `src/components/screens/CreateScreen.tsx` | Debounce, `presavePromiseRef`, piggyback on tap |

---

## Encode (critical)

> [!warning] Use **`canvas.toDataURL("image/jpeg", quality)`** (synchronous). **Do not** rely on **`toBlob`** for the hot path on native — Android WebView release can delay the callback **100–500ms+**.

`encodeCanvas` builds `{ blob, base64 }` from the data URL in one shot (no extra `FileReader`).

---

## Presave flow

1. `prewarmTemplateCache()` on mount (`posting.png`).  
2. **100ms** debounced `useEffect` on post text → `presavePostingCard(trimmed)`.  
3. `presavePromiseRef` + `pregeneratedCardRef` store in-flight / last result.  
4. Tap **fast path:** if `presavedUri` ready → `Share.share({ url })` immediately.  
5. Tap during presave → **await** existing promise (piggyback).  
6. Tap before debounce → generate fresh (rare).

---

## Order of operations

> [!important] **`await createPost(...)`** before `sharePostingCard(...)`.  
> If post creation fails (limits, validation), **no** canvas work and **no** share sheet.

---

## Canvas resolution

| Platform | Size |
|----------|------|
| Native | 540×960 (fewer pixels → faster encode) |
| Web | 1080×1920 |

---

## Debugging release Android

`console.log` **does not** appear in logcat on release WebView — use toasts or `error_logs` / Sentry.

---

## Capgo / version

- **`__APP_VERSION__`** from `package.json` at build — keep Capgo bundle version aligned.  
- Use **`capgo-push`** flow; agents: **no** git push unless user asks.

---

## See also

- [[Coding Patterns & Preferences]]
- [[Decision Log]]
- [[Capgo OTA]]
- [[🏠 Home]]
