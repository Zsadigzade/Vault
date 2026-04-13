---
tags: [overview, stack, identity]
area: overview
updated: 2026-04-06
---

# Project Overview

## What Is BRUH?

Cross-platform social meme-reply app for iOS, Android, and PWA. Users post meme prompts; others reply with GIFs/memes. Native app features gate (replies picker is native-only).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript, Vite, Tailwind CSS, Radix UI |
| Backend | Supabase (Postgres + Auth + Realtime + Edge Functions) |
| Native | Capacitor v8 (iOS + Android) |
| Push | Firebase Cloud Messaging (FCM) |
| Payments | RevenueCat |
| Ads | Google AdMob (native-only) |
| OTA updates | Capgo |
| CI/CD | Codemagic (iOS), manual (Android) |
| Landing | Netlify |
| Ops admin | Vercel (`admin-web/`) |
| Analytics | Vercel (`dashboard/`) |
| Error tracking | Sentry (EU — `de.sentry.io`) |
| Analytics events | PostHog (EU — `eu.posthog.com`) |
| GIF search | GIPHY + KLIPY |
| CAPTCHA | Cloudflare Turnstile (optional on register) |
| AI challenges | Google Gemini 2.5 Flash + GNews |

---

## App Identity

| Field | Value |
|-------|-------|
| iOS Bundle ID | `app.bruhsocial.app` |
| Android Package | `com.bruh.app` |
| Capacitor appId | `app.bruhsocial.app` |
| iOS Signing Team | `39FVY58F26` |
| Capgo App ID | `com.bruh.app` |
| Supabase Project | `gpainqlxdakaczkgozko` (West EU, Ireland) |

> [!warning] Android package `com.bruh.app` is set in `android/app/build.gradle` — NOT in `capacitor.config.ts`. The `capacitor.config.ts` appId is iOS only.

---

## Service URLs

| Service | URL |
|---------|-----|
| Main app (PWA) | `bruhsocial.app` |
| Share / landing | `share.bruhsocial.app` |
| Ops admin | `admin.bruhsocial.app` |
| Analytics | `analytics.bruhsocial.app` |
| Supabase Dashboard | `supabase.com/dashboard/project/gpainqlxdakaczkgozko` |
| GitHub repo | `github.com/Zsadigzade/BRUH` |
| PostHog | `eu.posthog.com` |
| Sentry | `de.sentry.io` (org: `bruh-social`) |

---

## Cursor MCP (for agents)

Use enabled MCP tools to **query and verify** live services while working on the repo — [[Agent MCP — live verification]] · [[12 - MCP & External APIs]]. Config: `.cursor/mcp.json` + `.cursor/.env.mcp.local`.

---

## Internationalisation

4 supported languages in `src/lib/i18n.ts`:

| Code | Language |
|------|----------|
| `en` | English (default) |
| `az` | Azerbaijani |
| `ru` | Russian |
| `tr` | Turkish |

> [!note] Language context drives i18n. Query keys that depend on language must be inside components (not module-level) — see [[Data Layer]].

---

## Key Source Directories

| Path | Purpose |
|------|---------|
| `src/lib/user/` | All user domain logic (auth, profile, session, posts, etc.) |
| `src/lib/user.ts` | 3-line backward-compat shim — real logic is in `user/` |
| `src/lib/queryKeys.ts` | All React Query keys — never inline them in components |
| `src/lib/nativeStorage.ts` | Capacitor Preferences bridge |
| `src/lib/admob.ts` | AdMob integration + real unit IDs |
| `src/lib/i18n.ts` | Translation strings |
| `src/test/setup.ts` | Global mocks (Capacitor, Supabase, PostHog, nativeStorage) |
| `src/test/testUtils.tsx` | `renderWithProviders` — use for all component tests |
| `supabase/functions/` | **26** deployable edge function packages (incl. `health-check`; verify in repo) |
| `landing/` | Netlify landing site source |
| `admin-web/` | Vercel ops admin source |
| `dashboard/` | Vercel analytics dashboard source |

---

## User Domain Modules

`src/lib/user/` contains these modules:
`types` · `profile` · `session` · `posts` · `replies` · `blocks` · `media` · `links` · `registration` · `challenges` · `contact` · `moderation` · `notifications` · `status` · `account` · `recovery` · `email` · `index`
