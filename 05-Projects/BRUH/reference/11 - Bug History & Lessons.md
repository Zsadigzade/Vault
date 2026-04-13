---
tags: [history, bugs, decisions, lessons, non-obvious]
area: reference
updated: 2026-04-05
---

# Bug History & Lessons

> [!note] Non-obvious decisions, root-caused bugs, and institutional knowledge. Read before attempting similar changes.

---

## Auth & Splash Race (2026-04-02) — App Review Blocker

**Symptom**: Reviewers saw only a white screen. Users false-redirected to `/welcome` after splash.

**Root cause 1 — White WKWebView**:
Production `index.html` had empty `#root` and no inline background → white until JS/CSS.
LaunchScreen used `systemBackgroundColor` (white in light mode).

**Fix**: `vite.config.ts` `native-first-paint` plugin injects critical CSS + boot HTML in `#root`.
`LaunchScreen.storyboard` changed to dark `#0c0a0f`.

**Root cause 2 — Storage race**:
`Index` ran `getUserId()` before `initNativeStorage()` finished → `null` → `navigate("/welcome")`.
The `[navigate]`-only effect never re-ran when storage hydrated.

**Fix**: `App.tsx` gates splash on `nativeStorageReady`. `BRUH_NATIVE_STORAGE_READY_EVENT` + listeners in `Index.tsx` / `WelcomePage.tsx` re-run auth gate when Preferences hydrate.

See [[Startup Sequence & Storage Keys]] (full init + event wiring) and [[Authentication]] (session + `getUserId()`).

---

## Push Notifications Completely Broken (2026-03-22)

**Symptom**: Reply system returned HTTP 400. All 4 push triggers failed.

**Root cause**: Supabase dashboard "Database Webhooks" UI truncated the `WEBHOOK_SECRET` in the JSON trigger argument (`"Bearer f080'` — missing closing `"` and `}`). `supabase_functions.http_request()` threw `22P02 invalid input syntax for type json`, rolling back the entire INSERT transaction.

**Fix**: Dropped all dashboard-created triggers. Replaced with PL/pgSQL SECURITY DEFINER functions reading `WEBHOOK_SECRET` from `vault.decrypted_secrets` via `net.http_post()` in migrations `20260322000008-10`.

**Lesson**: Never recreate push triggers via the Supabase dashboard UI. Write a migration. See [[Critical Gotchas]].

---

## Premium Button Flash on Startup

**Symptom**: Premium users briefly saw the "Buy Premium" button on cold start before it disappeared.

**Root cause**: `isPremiumUserCached()` reads a 15-min localStorage cache. On cold start or after TTL expiry, it returns `false`. The buy button renders before RC finishes initializing.

**Fix**: `App.tsx` startup chains `isPremiumUser()` after `initRevenueCat()` resolves (RC must be ready first on native). The in-app splash (~700ms) covers the async check on typical devices.

**Rule**: Never move the premium check before `initRevenueCat()` — the native entitlement check will fail.

---

## Queries Paused After Reconnect (2026-03-29)

**Symptom**: OfflineBanner disappeared correctly but React Query queries remained paused — no data refreshed when internet returned.

**Root cause**: `useOnlineStatus` had a Google-ping polling probe but never called `onlineManager.setOnline(true)` from `@tanstack/react-query`. Capacitor WebViews don't reliably fire `window "online"`.

**Fix**: Both the polling probe and `goOnline`/`goOffline` fast-path handlers now sync `onlineManager` from `@tanstack/react-query` alongside local `isOnline` state.

---

## Admin UUID Enumeration (2026-03-28)

**Symptom**: Any authenticated client could probe whether a UUID belonged to an admin.

**Root cause**: `is_admin(p_auth_id UUID)` — the parameter allowed arbitrary UUID lookup.

**Fix**: Removed the parameter entirely. `is_admin()` is now no-arg, hardcoded to `auth.uid()`. Also: `admin_users` SELECT was `qual: true` (public) — now restricted to `is_admin()`.

---

## NativeAd Plugin Detection (2026-03-28)

**Symptom**: `Capacitor.isPluginAvailable("NativeAd")` always returned `true` on Android.

**Root cause**: `registerPlugin` is global — `isPluginAvailable` checks registration, not platform availability.

**Fix**: Changed to `Capacitor.getPlatform() === "ios"` (or `=== "android"`).

---

## RevenueCat V2 API Incompatible (PAYMENT_FIXES)

**Fix**: Reverted RC webhook hybrid verify from V2 API URL back to V1. V2 endpoint was incompatible with the secret key format used.

---

## Payment Webhook HMAC Timing Attack

**Original**: `if (hmac === expected)` — `===` is timing-sensitive (fails early on first mismatch → timing oracle).

**Fix**: XOR `timingSafeEqual()` loop that always runs full comparison regardless of mismatch position.

---

## EXPIRATION Events Not Setting Grace Period

**Symptom**: Users lost premium immediately on expiration instead of getting 48h grace.

**Root cause**: EXPIRATION webhook events set `newStatus = null` instead of `"expired"`. The grace period logic only activates on status = `"expired"`.

**Fix**: EXPIRATION path now sets `newStatus = "expired"` before the 48h grace period RPC.

---

## `replies(count)` PostgREST Embedding — 15-20s Delay

**Symptom**: Inbox took 15-20 seconds to load.

**Root cause**: `supabase.from('posts').select('*, replies(count)')` triggers per-row RLS evaluation for every post. With many posts, this becomes catastrophically slow.

**Fix**: SECURITY DEFINER RPC that bypasses per-row RLS for aggregate counts.

**Rule**: Never use PostgREST resource embedding for reply counts. See [[Critical Gotchas]].

---

## Keyboard Layout Broken (2026-03-28)

**Symptom**: Screens scrolled/shifted when keyboard opened. Layout reflowed.

**Root cause**: `Keyboard.resize: 'body'` was set. This shrinks the `<body>` element height, reflowing the entire layout.

**Fix**: Changed to `resize: 'none'`. The `--kbd-h` CSS var + `useKeyboardHeight()` hook handle layout shifts manually. `windowSoftInputMode="adjustNothing"` on Android.

---

## Fire-and-Forget Handler False Success (2026-03-27)

**Symptom**: `ForgotPasswordScreen` — OTP wrong but user saw "Password reset!" and was navigated away.

**Root cause**: `handleResetPassword` fired `resetPasswordWithCode()` without `await`. Failure was silently ignored.

**Fix**: Handler made `async`. Call awaited. Result checked with `result?.error`.

---

## Capgo Splash Stuck (2026-03-31)

**Symptom**: App stuck on splash after Capgo OTA update on slow devices.

**Root causes**:
1. Failsafe timer lived in `main.tsx` after all static imports — never armed if bundle hung
2. Capgo `appReadyTimeout` default (10s) exceeded by slow device + large JS bundle → rollback loop
3. `notifyAppReady()` rejection not caught

**Fix**: 
1. Failsafe in `splash-failsafe.ts` (separate minimal entry) armed before `main.tsx` loads
2. `appReadyTimeout: 45000` in capacitor.config
3. `void CapacitorUpdater.notifyAppReady().catch(...)`

---

## Admin Capgo refresh: empty channel / no pinned version (2026-04)

**Symptom**: Admin **Refresh Capgo** showed no version or “no bundle pinned” despite Capgo dashboard having data; **Force OTA** was unusable.

**Root causes**: (1) **`capgo-proxy`** parsed only `body.data` while the live API returns a **top-level channel object** or **array** for `GET /channel/`, and a **top-level array** for `GET /bundle/` — see [[Capgo OTA]] (response shapes). (2) Earlier: wrong API path vs [Cap-go/capgo](https://github.com/Cap-go/capgo) source. (3) **GitHub Actions** Vercel deploy used `working-directory: admin-web` while the Vercel project **Root Directory** is already `admin-web` → path **`admin-web/admin-web`** does not exist.

**Fix**: Normalize channel/bundle JSON in **`capgo-proxy`**; redeploy the edge function. Admin UI: pinned vs latest bundles + Force OTA dropdown. Workflow: run Vercel CLI from **repo root** only.

---

## TypedArray `.at()` on Android 11

**Symptom**: Crash on Android 11 (Chrome WebView 90).

**Root cause**: `TypedArray.prototype.at` doesn't exist on WebView 90.

**Fix**: Polyfill in `main.tsx` covers all 9 typed array types.

---

## GCP Service Account Key in Git

**Status**: Scrubbed from tracking (2026-04-05). File gitignored (`bruh-*.json`).

> [!warning] The key (`bruh-489016-000f34885fcf.json`) must be rotated in Google Cloud Console. Optional: git history scrub.

---

## Root Directory Junk Cleaned (2026-03-29)

Deleted unreferenced files: `stitch_executive_overview/`, `icons/` (7 .webp), 5× `IMG-20260322-WA*.jpg`, `LOGO_Colored.jpg`, `image.png`, `notif_Icon_no_background.png`, `generate_icons.py`, `generate_notification_icon.py`.

**Sensitive files that remain in root** (do not delete; most gitignored):
- `.p8` keys, `.p12`/`.cer`/`.der` certs, `BRUH_App_Store.mobileprovision`
- `bruh-489016-000f34885fcf.json` — GCP key (rotate + history scrub pending)
- `google-services.json` — Firebase config for Android FCM (referenced by Android build)

---

## See also

- [[Critical Gotchas]]
- [[Decision Log]]
- [[Security Reference]]
- [[🏠 Home]]
