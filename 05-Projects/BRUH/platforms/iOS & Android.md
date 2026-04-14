---
tags: [platforms, ios, android, capacitor, signing, native]
area: platforms
updated: 2026-04-14
---

# iOS & Android

## Identity

| | iOS | Android |
|--|-----|---------|
| ID | `app.bruhsocial.app` | `com.bruh.app` |
| Set in | `ios/.../project.pbxproj` | `android/app/build.gradle` |
| Capacitor `appId` | `app.bruhsocial.app` | Package **not** from `capacitor.config.ts` |
| Team / keystore | `39FVY58F26` | Codemagic keystore |
| CI | Codemagic on `v*` tags | Manual |

> [!warning] Capacitor `appId` matches **iOS** only; Android `applicationId` is in Gradle — intentional.

---

## iOS — key files

| Path | Role |
|------|------|
| `ios/App/App/App.entitlements` | Associated Domains, Sign in with Apple |
| `ios/App/App/Info.plist` | `bruh://`, AdMob, privacy strings, orientations |
| `ios/App/App/GoogleService-Info.plist` | FCM — **must** be in Xcode Resources (target membership) |
| `ios/App/App/NativeAdPlugin.swift` | In-app native ads — **must** be in Compile Sources; implements `CAPBridgedPlugin`, `jsName` `NativeAd`. **GMA SDK v12 renames applied 2026-04-14** — all `GAD*` prefixes removed (see note below) |
| `ios/App/App/capacitor.config.json` | Generated — use `npm run cap:sync:ios` so `packageClassList` includes `NativeAdPlugin` after each sync |
| `project.pbxproj` | Bundle ID, `DEVELOPMENT_TEAM`, build phases |

**Universal Links:** AASA `landing/.well-known/apple-app-site-association` — paths `/u/*`, `/post/*`. Entitlement: `applinks:share.bruhsocial.app` (see `App.entitlements`). Detail: [[Deep Links & PWA]].

**SPM:** Capacitor 8 — **no** CocoaPods / `pod install`.

**GMA SDK v12 renames (applied 2026-04-14):** `GADNativeAdView`→`NativeAdView`, `GADMediaView`→`MediaView`, `GADRequest`→`Request`, `GADAdLoader`→`AdLoader`, `GADAdLoaderDelegate`→`AdLoaderDelegate`, `GADNativeAdLoaderDelegate`→`NativeAdLoaderDelegate`, `GADNativeAd`→`NativeAd`. Private delegate class renamed to `NativeAdPluginLoaderDelegate` to avoid collision with the protocol.

**iPad orientations + multitasking (fixed 2026-04-14):** `Info.plist` `UISupportedInterfaceOrientations~ipad` now declares all 4 orientations (App Store validation requirement) + `UIRequiresFullScreen = true` (opts out of Split View / Slide Over — app stays portrait-only at runtime).

**Signing:** Target has `DEVELOPMENT_TEAM = 39FVY58F26` (local Debug). Release remains **manual** + Codemagic `use-profiles`.

**Build**
```bash
npm run build && npm run cap:sync:ios   # iOS: never rely on plain `npx cap sync ios` alone for NativeAd registration
```

---

## Android — key files

| Path | Role |
|------|------|
| `android/app/build.gradle` | `com.bruh.app`, signing |
| `AndroidManifest.xml` | Permissions, **`adjustNothing`** (do not change — [[Keyboard & Layout]]) |
| `res/xml/network_security_config.xml` | TLS policy |

App Links: `landing/.well-known/assetlinks.json` → [[Deep Links & PWA]].

```bash
npm run build && npx cap sync
npx cap open android
```

---

## Capacitor (both)

Source of truth: `capacitor.config.ts` — Keyboard `resize: 'none'`, Splash `launchAutoHide: false`, Capgo `appReadyTimeout` 45s. iOS copy refreshed on sync.

---

## Apple `.p8` keys (repo root — don’t mix)

| File | Key ID | Use |
|------|--------|-----|
| `AuthKey_SY6Y4PPQAZ.p8` | `SY6Y4PPQAZ` | Sign in with Apple → Supabase Apple provider JWT |
| `AuthKey_JJRJ8CXM7A.p8` | `JJRJ8CXM7A` | APNs → Supabase `APNS_*`; also ASC API (Codemagic / RC) |
| `SubscriptionKey_5YJ4C4H3KY.p8` | `5YJ4C4H3KY` | StoreKit / IAP only |

Apple provider JWT expires **2026-09-26** — `generate-apple-jwt.mjs`. Service ID: `gpainqlxdakaczkgozko.supabase.co`.

---

## App Store Review test account

Credentials in vault for sandbox review only — see original onboarding note or ASC; **do not paste into chat/commits.**

---

## Capgo

App ID `com.bruh.app` (Android-aligned). OTA: `capgo-push.bat` (no auto git push). [[Deploy Targets]].
