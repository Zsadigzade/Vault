---
tags: [features, ads, admob, native, monetization]
area: features
updated: 2026-04-14
---

# Ad System

> [!note] **Native only** — all ad calls are no-ops on web/PWA (`Capacitor.isNativePlatform()` guard in `src/lib/admob.ts`). Premium users see no ads (`isPremiumUserCached()`). Ad-free period: 1 hour after rewarded ad (`localStorage.bruh_adfree_until`).

---

## AdMob Publisher

Account: `ca-app-pub-1146372347903589`

| Type | Unit ID | Status |
|------|---------|--------|
| App ID (Android + iOS) | `ca-app-pub-1146372347903589~5276121484` | In AndroidManifest + Info.plist |
| Banner | `ca-app-pub-1146372347903589/5949107154` | **Unused** — removed |
| Interstitial | `ca-app-pub-1146372347903589/8394723931` | **LIVE** |
| Rewarded | `ca-app-pub-1146372347903589/4754861828` | **LIVE** |
| Native Advanced | `ca-app-pub-1146372347903589/3378784134` | **LIVE via NativeAdPlugin** |

**Test IDs:** `import.meta.env.DEV` **or** `VITE_ADMOB_USE_TEST_IDS=true` → Google sample test IDs + `initializeForTesting`. Optional `VITE_ADMOB_TESTING_DEVICE_IDS` (comma-separated) for `initializeForTesting`.

---

## Placement

| Ad Type | Where | Frequency |
|---------|-------|-----------|
| **Interstitial** | CreateScreen | Every 3rd post creation |
| **Interstitial** | MemeReplyPicker | 800ms after reply sent |
| **Rewarded** | SubscriptionPage | "Watch an ad" button |
| **InlineWideAd** | RepliesInbox feed | Every 5th post |
| **InlineWideAd** | GifBrowserSheet memes | Every 4th GIF category |
| **InlineWideAd** | GifBrowserSheet stickers | Every 4th sticker category |
| **InlineWideAd** | MemeReplyPicker GIF categories | Every 4th category |
| **InlineWideAd** | MemeReplyPicker sticker categories | Every 4th category |
| **InlineSquareAd** | GifBrowserSheet search + trending grids | ~13% random, min gap 3 |
| **InlineSquareAd** | GifBrowserSheet sticker search | ~13% via `StickerScrollGrid showAds` |
| **InlineSquareAd** | MemeReplyPicker search | ~13% via `searchAdSlots` useMemo |
| **InlineSquareAd** | MemeReplyPicker trending | ~13% via `trendingAdSlots` useMemo |
| **SponsoredReplyCard** | PostDetail swipe view | Every 5th reply |
| **InlineSquareAd** | PostDetail grid view | Every 6th cell |

**Interstitial frequency cap:** min 2 minutes between shows (`INTERSTITIAL_MIN_INTERVAL_MS = 120_000`).

---

## Ad Slot Mix

3/4 slots = real ads (NativeAdSlot on native; Klipy GIF + interstitial on web).  
1/4 slots = house ads (premium promo: premium/hint/create/brand).  
Rule: `adIndex % 4 !== 0` → real ad; `adIndex % 4 === 0` → house ad.

---

## Native Ad Plugin

Custom Capacitor plugin wrapping Google Mobile Ads Native Advanced.

| File | Role |
|------|------|
| `src/lib/nativeAd.ts` | JS bridge — `loadAd`, `showAd`, `hideAd`, `removeAd`, `removeAllAds` |
| `src/components/NativeAdSlot.tsx` | Transparent placeholder, positions native overlay via `getBoundingClientRect()`, scroll/resize repositioning, IntersectionObserver show/hide, PostHog impression/failure tracking |
| `ios/App/App/NativeAdPlugin.swift` | `AdLoader` + `NativeAdView` subview of VC root. **GMA v12 renames applied 2026-04-14** — all `GAD*` prefixes stripped. |
| `android/app/src/main/java/com/bruh/app/NativeAdPlugin.java` | `AdLoader` + `NativeAdView` overlay on window decor view |

- Layout variants: `square` (grid tiles), `wide` (full-width bars)
- Coordinate conversion: iOS CSS px = UIKit pt (1:1); Android: CSS px × density + WebView screen offset
- `removeAllAds()` called on app background (`App.tsx`)
- `Capacitor.isPluginAvailable("NativeAd")` guard prevents throws on APKs without plugin compiled in

---

## `pickAdSlots`

~13% density, min gap of 3 between ads, stable per result set via `useMemo` keyed on `[items[0]?.id, items.length]`. Used in `MemeScrollGrid.tsx`, `MemeReplyPicker.tsx`.

---

## PostHog Tracking

- `native_ad_impression` — on load success (includes `layout`)
- `native_ad_failed` — on load failure (includes `layout` + `error`)

---

## GIF & Sticker Fetching

| Content | Primary | Fallback |
|---------|---------|---------|
| GIFs (search + trending) | **GIPHY** | Klipy |
| Stickers | **Klipy** | GIPHY |

Klipy pool warmup skipped on native (only fetches on web as fallback).

---

## app-ads.txt

`landing/app-ads.txt` live at `https://bruhsocial.app/app-ads.txt` — 306 entries.

---

## See also

- [[iOS & Android]] · [[Monetization]] · [[Deploy Targets]] · [[🏠 Home]]
