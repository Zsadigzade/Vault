---
tags: [architecture, invariants, critical, agents]
area: architecture
status: stable
updated: 2026-04-04
---

# Architecture invariants

> [!warning] **Do not change** the ordering or contracts below without explicit human approval and a full regression pass (auth, splash, keyboard, OTA, payments, push). Detail: [[Authentication]], [[Startup Sequence & Storage Keys]], [[Keyboard & Layout]], [[Capgo OTA]], [[Share Card & Presave]], [[Push Notifications]].

---

## Auth & identity

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| App identity is `getUserId()` / `bruh_user_id` cache — not `supabase.auth.getUser()` for “who is the user” | `src/lib/user/`, consumers | Two auth paths; wrong API → subtle IDOR or wrong RLS assumptions. |
| Password-auth path uses anon session + SECURITY DEFINER RPCs + `get_my_user_id()` | DB + client | Breaking this leaks or blocks access across RLS. |

---

## Startup, splash & storage

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| Native storage must be initialized before auth gates read `bruh_user_id` | `App.tsx`, `nativeStorage.ts`, `Index.tsx`, `BRUH_NATIVE_STORAGE_READY_EVENT` | Race → false `/welcome` redirect or white screen (see [[Bug History & Lessons]]). |
| Splash / first paint: native-first-paint + dark launch screen alignment | `vite.config.ts` plugin, iOS `LaunchScreen` | Reviewers saw white WKWebView when this drifted. |
| Failsafe timer arms **before** heavy `main.tsx` import chain | `splash-failsafe.ts` | Prevents stuck splash if bundle hangs. |

---

## Keyboard & layout

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| `Keyboard.resize: 'none'` and Android `adjustNothing` | Capacitor config, `AndroidManifest` | `'body'` or `adjustResize` reflows shell — breaks keyboard architecture. |
| Bottom inset uses `--kbd-h` / `useKeyboardHeight()` on **outer** column | Multiple screens | Padding on inner scroller breaks scroll + sheets. |

---

## Premium & monetization

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| On native, premium entitlement check runs **after** `initRevenueCat()` | `App.tsx` startup | Reordering causes buy-button flash for subscribers. |

---

## Share card & canvas

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| Posting card encoding uses synchronous `canvas.toDataURL` path — not `toBlob` for the critical encode | `storyCardGenerator.ts` / related | Android WebView release: `toBlob` latency killed UX. |

---

## Capgo OTA

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| `notifyAppReady()` errors handled; `appReadyTimeout` sufficient for slow devices | `capacitor.config`, updater init | Prevents rollback loops / stuck splash. |

---

## Push notifications

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| Triggers implemented via migrations + `vault.decrypted_secrets` — not Dashboard “Database Webhooks” UI for secrets | `supabase/migrations`, functions under `supabase/functions/send-push-notification` | Dashboard JSON truncation broke inserts (see [[Bug History & Lessons]]). |

---

## Deep links

| Invariant | Where | Why fragile |
|-----------|-------|-------------|
| `DeepLinkHandler` allowlist stays minimal (`/u/`, `/post/`) unless product expands deliberately | `App.tsx` / handler module | Allowlist is a security boundary. |

---

## See also

- [[Critical Gotchas]] · [[CONSTITUTION]] · [[13 - Tombstones & Anti-Patterns]]
- [[🏠 Home]] · [[Agent Quick Reference]]
