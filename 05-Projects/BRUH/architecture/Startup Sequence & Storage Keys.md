---
tags: [architecture, startup, storage, init, native]
area: architecture
updated: 2026-04-03
---

# Startup Sequence & Storage Keys

## Full Provider Tree (outermost → innermost)

```
ErrorBoundary(App)
  QueryClientProvider       ← queryClient is module-level in App.tsx (~line 60)
    TooltipProvider
      LanguageProvider      ← i18n; persists "bruh_language"; infers from device locale + cached region on first launch
        [Toaster + Sonner toasts]
        SplashScreen          ← shown until hideSplash() called
        OnboardingFlow        ← shown if !showSplash && showOnboarding
        RealtimeProvider      ← mounted after splash + onboarding clear
          TourProvider
            BrowserRouter
              DeepLinkHandler     ← Capacitor appUrlOpen → handleOAuthCallback
              PushHandler         ← initPushNotifications + setPushNavigationHandler
              TourOverlay
              Suspense(shimmer)
                ErrorBoundary(Routes)
                  BanGuard        ← wraps ALL routes; queryKey:["ban-status"], refetchInterval:5min
                    Routes
```

---

## QueryClient Config (module-level in App.tsx)

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      retryDelay: 1000,
      staleTime: 60_000,      // 1 minute default
      gcTime: 10 * 60_000,    // 10 minutes garbage collection
    }
  }
})
```

---

## Startup `useEffect` Sequence (App.tsx, once on mount)

```
1. await initNativeStorage()          → hydrate Capacitor Preferences → memCache + localStorage
2. setShowOnboarding(!getItem("bruh_onboarded"))
3. validateUserSession().then(valid =>
     { if (valid) queryClient.invalidateQueries(MY_POSTS_QUERY_KEY) }).catch(console.error)
   → fire-and-forget (intentional — does NOT block splash)
4. migrateLocalBlocksToServer()       → fire-and-forget
5. initRevenueCat(getUserId())
     .then(() => {
       if (getUserId()) isPremiumUser().catch(() => {})
     })
   → RC must init BEFORE premium check on native
   → chains premium cache warmup so isPremiumUserCached() is correct before CreateScreen renders
   → prevents buy-button flash for premium users
6. initAdMob()                        → init ads (native only, no-op on web)
```

RevenueCat / premium warmup details: [[Monetization]].

**Additional hooks in App.tsx:**
- Keyboard height tracking (native only): sets `--kbd-h` CSS var on `<html>` + dispatches `"kbd-change"` CustomEvent — see [[Keyboard & Layout]]
- Premium cache invalidation (all platforms): invalidates on app resume / window focus
- Periodic premium re-check: 30-minute `setInterval` → `isPremiumUser()` + invalidate `["settings-meta"]` — see [[Monetization]]

---

## Splash Dismiss Logic (`commitSplashDismiss`)

Splash dismisses ONLY when **both** conditions are met:
1. `nativeStorageReady === true` (Preferences hydrated)
2. `splashMinTimeDone === true` (~700ms from `SplashScreen.tsx`)

Race timeout: **5s** (whichever fires first for nativeStorageReady).
Absolute failsafe: **12s** in App.tsx forces dismiss regardless.

On dismiss:
- Sets `sessionStorage["bruh_active_tab"] = "1"` when `pathname === "/" ` (cold start → Create tab)
- Calls native `CapSplashScreen.hide()`

---

## `BRUH_NATIVE_STORAGE_READY_EVENT` (`"bruh-native-storage-ready"`)

Dispatched from `initNativeStorage().finally()` (native) and after web no-op init.

Listeners:
- `App.tsx` → sets `nativeStorageReady = true` → triggers `commitSplashDismiss`
- `Index.tsx` → re-runs `applyAuthGate()` (prevents false `/welcome` redirect from early `getUserId() === null`)
- `WelcomePage.tsx` → if `getUserId()` appears → `navigate("/", { replace: true })`

**Why**: On native, `getUserId()` called before `initNativeStorage()` finishes returns `null`. Without this event, the app permanently redirects to `/welcome` with no way back.

---

## Auth Guard (`applyAuthGate` in Index.tsx)

Runs on:
- Component mount
- `BRUH_NATIVE_STORAGE_READY_EVENT`

Logic:
```
No userId            → navigate("/welcome")
bruh_stay_logged_in  → stamp sessionStorage.bruh_welcome_seen + continue
bruh_last_username set but no bruh_welcome_seen → navigate("/login")
```

---

## Tab Initial State

`getInitialTab()` in Index.tsx:
1. `/inbox` route → tab 0
2. `sessionStorage["bruh_active_tab"]` → use stored tab
3. Default: **1** (Create)

---

## Native Storage Keys

### Capacitor Preferences (survive WebView data clears)

| Key | Value | Purpose |
|-----|-------|---------|
| `bruh_user_id` | UUID | Primary user ID |
| `bruh_username` | string | Current username |
| `bruh_stay_logged_in` | `"1"` | Stay logged in flag |
| `bruh_onboarded` | `"1"` | Onboarding complete |
| `bruh_last_username` | string | Login screen pre-fill |
| `bruh_recovery_token` | string | Account recovery — **native: Preferences + memCache ONLY** — NOT mirrored to WebView localStorage |
| `bruh_language` | `"en"/"az"/"ru"/"tr"` | Selected language |

> [!warning] `bruh_recovery_token` on native is Preferences + memCache only — NOT in WebView localStorage. `initNativeStorage` clears any legacy LS key. This is intentional hardware-isolation.

### localStorage Only (not in Preferences)

| Key | Purpose |
|-----|---------|
| `bruh_subscribed` / `bruh_subscribed_at` / `bruh_subscribed_checksum` | Premium cache (15min, djb2 tamper-proof) |
| `bruh_rated` | App store rating shown |
| `bruh_rate_dismissed` | Rate popup dismissed (7-day cooldown) |
| `bruh_app_opens` | Launch counter (incremented when tour complete); capped wrap at 100 |
| `bruh_broadcast_reads` | JSON array of read broadcast IDs |
| `bruh_broadcast_dismissed` | JSON array of dismissed broadcast IDs |
| `bruh_hidden_memes_<uid>` | User-scoped hidden meme list (or `_guest`) |
| `bruh_blocked_users` | Locally cached block list |
| `bruh_adfree_until` | Timestamp: 1 hour ad-free after rewarded ad |
| `bruh_login_rl` | Login rate limit timestamps (10/5min) |
| `bruh_reset_rl` | Password reset rate limit timestamps (3/5min) |

### sessionStorage

| Key | Purpose |
|-----|---------|
| `bruh_welcome_seen` | Per-session: skip welcome screen |
| `bruh_active_tab` | Active tab index for returning from nested routes |

---

## First Paint Architecture

```
index.html
  ↓ loads only src/splash-failsafe.ts (minimal)
    splash-failsafe.ts
      ↓ registers 8s SplashScreen.hide timer (BEFORE large bundle loads)
      ↓ dynamic import("./main.tsx")
        main.tsx
          ↓ void CapacitorUpdater.notifyAppReady().catch(...)
          ↓ renders <App />
```

**Why minimal entry**: The 8s failsafe timer must arm BEFORE the large bundle finishes downloading/parsing. If it was in `main.tsx` directly, a slow/hung bundle would never arm the failsafe.

**`capacitor.config.ts`**: `CapacitorUpdater.appReadyTimeout: 45000` (45s — prevents Capgo rollback on slow devices). OTA flow: [[Capgo OTA]].

---

## Screen Helper

```tsx
function Screen({ name, children }: { name: string; children: ReactNode }) {
  return (
    <MobileFrame>
      <ErrorBoundary componentName={name} fallback={<GoBackButton />}>
        {children}
      </ErrorBoundary>
    </MobileFrame>
  );
}
// Used for every route EXCEPT /admin and /auth/callback
```

---

## See also

- [[App Architecture]]
- [[Authentication]]
- [[Keyboard & Layout]]
- [[Monetization]]
- [[Capgo OTA]]
- [[🏠 Home]]
