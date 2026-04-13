---
tags: [deployment, codemagic, ios, ci, cd]
area: deployment
updated: 2026-04-05
---

# Codemagic CI

---

## Triggers

- **iOS App Store workflow:** tags matching **`v*`** (e.g. `v0.1.8`).  
- **Local helper:** `codemagic-push.bat.example` — copy to `.bat`, customize; pushes `main` + semver tag.  
- **Android workflow:** often **manual** / disabled auto-trigger — user builds Play uploads separately.

---

## iOS workflow (`ios-app-store`)

| Setting | Value / Notes |
|---------|---------------|
| Instance | `mac_mini_m2`, Node 22 |
| Xcode project | `--project ios/App/App.xcodeproj` (**no** workspace — Cap8 + SPM) |
| Signing | **Manual** — `CODE_SIGN_STYLE = Manual`, `CODE_SIGN_IDENTITY = "Apple Distribution"` (Release) |
| Certificate | `Bruh_IOS` (.p12) uploaded to Codemagic Code Signing Identities |
| Provisioning profile | `Bruh_IOS` (.mobileprovision); `ios_signing.provisioning_profiles: [Bruh_IOS]` in yaml |
| Submit TestFlight | YES (auto); App Store submit: manual |
| Notifications | Build success/failure → `zsadigzade@gmail.com` |

---

## Capacitor 8 / iOS

- **No CocoaPods step** — Swift Package Manager via `ios/App/CapApp-SPM/Package.swift`.  
- Prior fixes: manual signing, all iPad orientations in `Info.plist`, `CODE_SIGN_STYLE = Manual` Release.

---

## Android

- Keystore: `android_signing` group in Codemagic UI — `CM_KEYSTORE_PASSWORD`, `CM_KEY_ALIAS`, `CM_KEY_PASSWORD`, `BRUH_KEYSTORE` (file). ✅ Configured.
- **google-services.json** in repo for FCM (Android build).
- **`PACKAGE_NAME` / applicationId:** must be **`com.bruh.app`** in `codemagic.yaml` / Gradle (2026-04 repo fix — was incorrectly `app.bruh.social`-style id).

---

## Environment variables (fixed 2026-04-13)

`.env` is gitignored — Codemagic never sees it. All vars must be declared in `codemagic.yaml` or Codemagic UI groups.

### Public vars (inline in `codemagic.yaml` — both workflows)

| Var | Value |
|-----|-------|
| `VITE_LANDING_URL` | `https://share.bruhsocial.app` |
| `VITE_SUPABASE_URL` | `https://gpainqlxdakaczkgozko.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | (anon key — safe to commit) |
| `VITE_SENTRY_DSN` | (EU ingest DSN — safe to commit) |
| `VITE_POSTHOG_KEY` | `phc_aTv83kLWjx9JUKFiEoRexOKAD8KM9BOBOzvKBnb3YM3` |
| `VITE_POSTHOG_HOST` | `https://eu.i.posthog.com` |

### Secret groups (Codemagic UI)

| Group | Vars | Used in |
|-------|------|---------|
| `android_signing` | `CM_KEYSTORE_*`, `BRUH_KEYSTORE` | Android workflow |
| `secrets` | `SENTRY_AUTH_TOKEN` | Both workflows — source map upload |

`SENTRY_AUTH_TOKEN` scopes: `project:read` + `release:admin`. Token in Codemagic UI → `secrets` group. `sentryVitePlugin` in `vite.config.ts` is guarded: `!!process.env.SENTRY_AUTH_TOKEN` — skips gracefully if missing.

---

## Notifications

- Build success/failure emails — configure in Codemagic UI (e.g. owner Gmail).

---

## iOS Signing Assets

| Asset | Value / Notes |
|-------|---------------|
| Distribution certificate | `distribution.p12`, password: `bruh2026` |
| App Store Connect API key | `AuthKey_JJRJ8CXM7A.p8` (Key ID `JJRJ8CXM7A`) |
| ASC API key note | **Dual-purpose** — same key used for APNs push secrets in Supabase (`APNS_KEY_ID`) and by RevenueCat. Don't rotate without updating all three. |

> [!warning] The ASC API key (`JJRJ8CXM7A`) is shared with Supabase APNs config and RevenueCat. Rotating it requires updating all three services simultaneously.

---

## Related IDs (non-secret)

| Item | Value |
|------|--------|
| App Store Connect App ID | `6761007303` |
| Bundle ID | `app.bruhsocial.app` |
| Play package | `com.bruh.app` |

---

## See also

- [[Deploy Targets]]
- [[Commands & Scripts]]
- [[Launch Checklist]]
- [[iOS & Android]]
- [[🏠 Home]]
