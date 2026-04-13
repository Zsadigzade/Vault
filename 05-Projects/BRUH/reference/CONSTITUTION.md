---
tags: [meta, constitution, immutable, agents, agent:immutable]
area: meta
status: stable
updated: 2026-04-04
---

# BRUH — Constitution (immutable laws)

> [!warning] **Agents:** This file is **read-only**. Do not edit, rename, or delete. If a task conflicts with these laws, stop and ask the human. Expanded detail lives in [[Critical Gotchas]], [[Coding Patterns & Preferences]], and repo `CLAUDE.md`.

---

## Identity & auth

| Law | Detail |
|-----|--------|
| **App user id** | Use `getUserId()` (sync). Never `supabase.auth.getUser()` for app identity. |
| **Native storage** | Use `getItem` / `setItem` from `nativeStorage.ts`. Never read `bruh_user_id` from `localStorage` directly on native. |
| **Server-side identity** | SECURITY DEFINER RPCs derive user via `get_my_user_id()`. Never trust client-supplied UUID as the authenticated user for privileged ops. |

---

## Database & Supabase

| Law | Detail |
|-----|--------|
| **Reply / aggregate counts** | Never PostgREST resource embedding like `replies(count)` — use SECURITY DEFINER RPCs. |
| **Promise shape** | `PostgrestFilterBuilder` is not a full `Promise` — no `.catch()`; use `.then(({ error }) => …)`. |
| **Migrations & webhooks** | Push and sensitive triggers: migrations + Vault secrets — not Supabase Dashboard Database Webhooks UI (secret truncation). |

---

## UI, keyboard & layout

| Law | Detail |
|-----|--------|
| **Capacitor Keyboard** | `Keyboard.resize: 'none'`. Never `'body'`. |
| **Android** | `windowSoftInputMode="adjustNothing"`. Never `adjustPan` / `adjustResize` for this app’s layout model. |
| **Insets** | Keyboard height via `--kbd-h` / `useKeyboardHeight()`; outer column gets padding, not inner scroller. |

---

## React, data & tests

| Law | Detail |
|-----|--------|
| **Server/async data** | `useQuery` — not `useState` + `useEffect` for fetching. |
| **Query keys** | From `src/lib/queryKeys.ts` — not ad-hoc strings (except documented i18n-in-component exceptions). |
| **Handlers** | `await` async work in handlers; check `result?.error` before success UX. |
| **React import** | No `import React from 'react'` — type-only imports from `'react'` where needed. |
| **Component tests** | `renderWithProviders` from `src/test/testUtils.tsx`. |
| **Replies UX** | `MemeReplyPicker` stays native-only (Capacitor guard). Do not remove for web. |

---

## Native-only & monetization

| Law | Detail |
|-----|--------|
| **Ads** | Guard with `Capacitor.isNativePlatform()`; respect premium / ad-free caches. |
| **Premium on startup** | Native: `isPremiumUser()` after `initRevenueCat()` — not before. |

---

## Tooling, deploy & git

| Law | Detail |
|-----|--------|
| **Windows CLIs** | Always `npx supabase` and `npx netlify` (global EPERM). |
| **Android package** | Package name in `android/app/build.gradle` — not as the source of truth in `capacitor.config` for Android. |
| **`.bat` files** | Do not commit runnable `.bat` (gitignored); use `.bat.example` templates. |
| **Git** | No `git commit` / `git push` unless the user explicitly asks in that message. |

---

## Security

| Law | Detail |
|-----|--------|
| **Secrets** | Never paste secrets into chat, vault, or commits. |
| **HMAC / secrets compare** | Use `timingSafeEqual()` — not `===` on raw secret strings. |
| **Redirects** | Use validated same-origin patterns (`safeRedirect`); never assign `window.location` from untrusted URLs. |
| **Deep links** | `DeepLinkHandler` allowlist is a security boundary — only `/u/` and `/post/` unless product explicitly expands it. |

---

## Vault maintenance (agents)

| Law | Detail |
|-----|--------|
| **This file** | Do not modify `CONSTITUTION.md`. |
| **Handoff** | Update [[SESSION_HANDOFF]] at end of substantive sessions. |
| **Dead ideas** | Before suggesting removed libraries or flows, check [[13 - Tombstones & Anti-Patterns]]. |

---

## See also

- [[🏠 Home]] · [[Agent Quick Reference]] · [[Critical Gotchas]]
- [[INVARIANTS]] · [[13 - Tombstones & Anti-Patterns]]
