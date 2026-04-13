---
tags: [features, revenue, revenuecat, admob, ads, payments, premium]
area: features
updated: 2026-04-08 (UI/Ads pass)
---

# Monetization

> [!tip] Webhook / hybrid-verify / fraud / idempotency details: [[Payment Webhook Security]]. Admin subscription audit: [[Dashboards]] (Fraud / Audit tabs).

## Two Revenue Streams

| Stream | Platform | Gate |
|--------|---------|------|
| **RevenueCat** (subscriptions) | iOS + Android + Web | `isPremiumUser()` / `isPremiumUserCached()` |
| **AdMob** (ads) | Native-only | `Capacitor.isNativePlatform()` + **`hasAnyPremiumAccess()`** (subscriber cache **or** temp premium) |
| **Fortune wheel** (temp premium + rewarded) | Native Profile | Edge **`fortune-spin`**; DB **`users.temp_premium_until`** + spin counters; client **`grantTemporaryPremium`** / **`isTemporaryPremiumActive`**; losers must complete rewarded ad before next spin |

> [!note] **`hasAnyPremiumAccess()`** = **`isPremiumUserCached() || isTemporaryPremiumActive()`** — used for ad suppression and premium-gated UI (GIF/sticker flows, native ads, etc.). Real paid status for paywall copy may still use async **`isPremiumUser()`**.

---

## RevenueCat (Subscriptions)

### Product
| Field | Value |
|-------|-------|
| Entitlement | `"BRUH Pro"` |
| Store product id (ASC) | `bruh_pro_weekly` |
| RevenueCat package | `$rc_weekly` — auto-renewable |
| Price display | `$0.99 / week · Cancel anytime` |
| i18n key | `premium.price` (same across all 4 languages) |
| ASC App ID | `6761007303` |
| Vendor Number | `94136885` |

> [!note] Google Play / App Store sandbox billing uses 5-minute cycles. This is expected test behavior — NOT real charges. `Subscription.tsx` strips the sandbox billing period from `priceString` and always appends `/week`.

### RC API Keys (client-side, in `src/lib/purchases.ts`)
```ts
const RC_API_KEY = Capacitor.getPlatform() === "ios"
  ? "appl_DKsEBqMctyUZRnepwkwDnQncIHz"
  : "goog_yQvntVwYSPhkeAlAVnnxkXEsjji";
```
ASC API key linked in RC dashboard: Key ID `JJRJ8CXM7A` (same as Codemagic + APNs — dual-purpose, see [[iOS & Android]]).

### Premium Check Functions

| Function | Type | Cache | Used for |
|----------|------|-------|---------|
| `isPremiumUser()` | async | None (fresh) | Before showing premium content; before premium interstitial |
| `isPremiumUserCached()` | sync | **15 min** localStorage + djb2 tamper check | Before showing/hiding ads (must be fast); skip in render path |
| `invalidatePremiumCache()` | sync | Clears cache | Called on realtime `users.UPDATE` subscription change |

```ts
// Async — use before gating features
const isPremium = await isPremiumUser();

// Sync cached — use in render paths (ad suppression, UI show/hide)
const isPremium = isPremiumUserCached();
```

**Web fallback**: `isPremiumUser()` checks DB + 48h grace period if RevenueCat returns false (enables admin-granted premium).
**Native fallback**: Also falls back to DB check after RC returns false.

**Chat:** **Sending** chat messages is enforced in Postgres (`send_chat_message` + premium/grace RPC); free users are read-only in UI. → [[Chat System]]

### Grace Period
**48 hours** on subscription expiration events (enables `"expired"` status which triggers grace logic). Prevents accidental premium loss during payment processing.

> [!warning] EXPIRATION webhook events MUST set `newStatus = "expired"` (not `null`). The grace period only activates on status = `"expired"`. This was a fixed bug.

### Premium Cache Storage Keys
```
bruh_subscribed          ← "1" if premium
bruh_subscribed_at       ← timestamp of last check
bruh_subscribed_checksum ← djb2 hash for tamper detection
```

### Webhook (summary)

Full table: [[Payment Webhook Security]]. In short: timing-safe Authorization, optional HMAC, non-UUID skip **200**, hybrid verify fail-closed without secret key, `webhook_events` idempotency, rate limits, Zod.

### Required Secrets
| Secret | Required? | Purpose |
|--------|-----------|---------|
| `REVENUECAT_WEBHOOK_SECRET` | **Yes** | Authorization header match (RC → Supabase) |
| `REVENUECAT_SECRET_KEY` | **Yes** | Hybrid REST verify — **fail-closed without this** |
| `REVENUECAT_WEBHOOK_VERIFICATION_SECRET` | No | Optional HMAC layer |

---

## AdMob (Ads)

### Critical Rule

> [!warning] ALL ad calls guarded with `Capacitor.isNativePlatform()` — ads are native-only. Already done in `src/lib/admob.ts`. Never call AdMob functions without this check.

### Ad Unit IDs (Live Production)

AdMob account: `ca-app-pub-1146372347903589`

| Type | Unit ID | Status |
|------|---------|--------|
| App ID (Android + iOS) | `ca-app-pub-1146372347903589~5276121484` | Active in AndroidManifest.xml + Info.plist |
| Banner | `ca-app-pub-1146372347903589/5949107154` | Defined in `admob.ts` — **intentionally not shown** (no layout slot alongside BottomNav) |
| Interstitial | `ca-app-pub-1146372347903589/8394723931` | **LIVE** |
| Rewarded | `ca-app-pub-1146372347903589/4754861828` | **LIVE** |
| Native Advanced | `ca-app-pub-1146372347903589/3378784134` | **LIVE via NativeAdPlugin** |

### Pre-publish: Google test ad units (repo)

> [!tip] Real units often **do not fill** until the app is live / units approved. For on-device verification use test IDs.

- **`src/lib/admob.ts`**: production IDs when **not** in test mode; **`import.meta.env.DEV`** (Vite dev) switches to Google **sample** banner / interstitial / rewarded IDs.
- **Release-style native builds** (`npm run build` → Capacitor): `DEV` is false — set **`VITE_ADMOB_USE_TEST_IDS=true`** in env before build to force test units on internal APKs / Play internal testing.
- Optional: **`VITE_ADMOB_TESTING_DEVICE_IDS`** (comma-separated) passed into `AdMob.initialize({ initializeForTesting: true, testingDevices })` when test mode is on.
- **`useTestAdMobIds()`** exported for debugging. Repo: `CLAUDE.md` Ads section, `src/vite-env.d.ts`.

### Premium + Ad-Free Gates

```ts
if (isPremiumUserCached()) return;  // paying subscriber — permanent no ads
if (isAdFreeActive()) return;       // 1 hour ad-free after watching rewarded ad
```

**Ad-free storage key**: `bruh_adfree_until` (localStorage timestamp)
**Duration**: **1 hour** (NOT 24h)

### AdMob interstitial frequency cap
`src/lib/admob.ts`: minimum **2 minutes** between **AdMob** interstitial shows (`INTERSTITIAL_MIN_INTERVAL_MS = 120_000`) — policy / UX spacing. **Not** the in-app **premium upsell** modal (see **Premium Interstitial (App Shell)** below).

### Ad Placement Table

| Ad Type | Location | Frequency / Trigger |
|---------|----------|-------------------|
| **Interstitial** | CreateScreen | Every 3rd post creation |
| **Interstitial** | MemeReplyPicker | 800ms after reply sent |
| **Interstitial** | `HiddenInterstitialAdGif` tap (GIF grids) | On user tap of a hidden ad tile |
| **Rewarded** | SubscriptionPage | "Watch an ad" button |
| **Rewarded** | Fortune Wheel | Mandatory after losing spin (before next spin) |
| **InlineWideAd** | RepliesInbox feed | Every 5th post |
| **InlineWideAd** | GifBrowserSheet stickers (category list) | Every 4th sticker category (gated `!premium && !isAdFreeActive()`, not after last category) |
| **InlineWideAd** | MemeReplyPicker sticker categories | Every 4th category |
| **HiddenInterstitialAdGif** | MemeReplyPicker GIF trending + search grids | ~13% random `pickAdSlots` — looks like a normal GIF tile, fires interstitial on tap |
| **HiddenInterstitialAdGif** | GifBrowserSheet GIF trending + search grids | ~13% random `pickAdSlots` — same pattern |
| **InlineSquareAd** | GifBrowserSheet sticker **search** (vertical `StickerScrollGrid`) | ~13% via `showAds` when gated |
| **InlineSquareAd** | PostDetail grid view | Every 6th cell |
| **SponsoredReplyCard** | PostDetail swipe view | Every 5th reply |

> [!note] **`HiddenInterstitialAdGif`** (`src/components/AdSlot.tsx`) — renders a real trending GIF thumbnail with no "Ad" label; indistinguishable from regular grid items. Tap fires `showInterstitialAd()` (AdMob skippable interstitial) and returns user to grid without selecting the GIF. Non-premium + non-ad-free users only.

### Ad Slot Mix (InlineSquareAd / NativeAdSlot)
- **3/4 slots** = real AdMob ads (NativeAdSlot on native)
- **1/4 slots** = house ads (premium upsell variants: premium/hint/create/brand)
- Rotation: `adIndex % 4 !== 0` → real ad; `adIndex % 4 === 0` → house ad

### Random Slot Selection
`pickAdSlots(count)` — ~13% density, min gap 3, stable per result set via `useMemo` keyed on `[items[0]?.id, items.length]`. Randomness is per-device (independent `Math.random()` state); different users and different result sets produce different slot positions. Slots regenerate when the result set changes (new search, load more), stay stable within a scroll session.

### Native Ad Plugin

Custom Capacitor plugin (`NativeAdPlugin`) wrapping Google Mobile Ads Native Advanced:
- JS bridge: `src/lib/nativeAd.ts` — `loadAd`, `showAd`, `hideAd`, `removeAd`, `removeAllAds`
- React: `src/components/NativeAdSlot.tsx` — transparent placeholder div, positions native view overlay via `getBoundingClientRect()`, scroll/resize repositioning, IntersectionObserver
- **React layer loads native overlay on iOS only** (`getPlatform() === "ios"`). **Android** has `NativeAdPlugin.java` but TS uses **Klipy thumbnail + interstitial-on-tap** (or house ad) fallbacks from `AdSlot.tsx`.
- iOS: `ios/App/App/NativeAdPlugin.swift`
- Android: `android/app/src/main/java/com/bruh/app/NativeAdPlugin.java`
- `removeAllAds()` called automatically when app goes to background (in `App.tsx`)
- Guard: `Capacitor.isPluginAvailable("NativeAd")` — but use `Capacitor.getPlatform()` check NOT `isPluginAvailable` (isPluginAvailable always returns true after registerPlugin)

### PostHog Ad Tracking
- `native_ad_impression` — on successful load (includes `layout`)
- `native_ad_failed` — on load failure (includes `layout` + `error`)

### GIF & Sticker Sources
| Content | Primary | Fallback |
|---------|---------|---------|
| GIFs (search + trending) | GIPHY | Klipy |
| Stickers | Klipy | GIPHY |

### Pending
- Configure UMP consent form for EU/GDPR (AdMob console) before EU launch
- Add mediation networks (Meta Audience Network, AppLovin) for better fill rates
- `landing/app-ads.txt` live at `https://bruhsocial.app/app-ads.txt` (306 entries)

---

## Premium Interstitial (App Shell)

Separate from AdMob — the subscription upsell modal:
- Shown on **every** `Index` remount for non-premium users (after `tourAllDone`)
- Timing: **1.5s** delay normally; **4.5s** when `bruh_app_opens >= 8` (rate-us fires at 1s, stagger avoids overlap)
- `isPremiumUserCached()` → skip immediately if premium
- Then `isPremiumUser()` async re-check before `setShowPremiumInterstitial(true)`
- Effect uses `cancelled` flag on unmount (prevents stale async results)
- Render: `showPremiumInterstitial && !isPremiumUserCached()`

### Rate-App Popup (separate from premium modal)
- Shows at ≥8 app opens (incremented in `Index.tsx` when `tourAllDone`)
- 1s delay
- Cooldown: 7 days after dismiss
- `tourAllDone` required — never interrupts new users mid-tutorial

---

## Periodic premium refresh

- `App.tsx`: ~**30 min** interval `isPremiumUser()` + invalidate `["settings-meta"]`  
- App resume / focus: re-fetch premium (subscription cancellations without restart)

---

## Cancel subscription UX

- `SubscriptionSettings`: toast before opening store manager; invalidate settings query on return — see `ux_fixes` / repo.

---

## See also

- [[Payment Webhook Security]]
- [[Security Reference]]
- [[Edge Functions]]
- [[Dashboards]]
- [[Personal Media & GIFs]] (premium gates)
- [[🏠 Home]]

## RevenueCat Best Practices — 2026-04-13

- **External purchases** — Apple + Google now allow external purchase flows in specific regions/categories; varying fees
- **State of Subscription Apps 2025** — constant A/B testing essential; try different price points, avoid analysis paralysis
- **Web purchases** — app-to-web flows allowed in EU (DMA); requires entitlement linking via RevenueCat
- Source: [RevenueCat app-to-web guide](https://www.revenuecat.com/blog/engineering/app-to-web-purchase-guidelines/), [State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/)
