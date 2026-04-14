---
tags: [overview, launch, checklist, secrets]
area: overview
updated: 2026-04-14
---

# Launch Checklist

---

## Pre-launch TODOs

- [x] Configure **UMP** consent form for EU/GDPR (AdMob console) — **DONE 2026-04-13**
- [x] Upload **Android keystore** to Codemagic — **DONE** (`android_signing` group: `CM_KEYSTORE_PASSWORD`, `CM_KEY_ALIAS`, `CM_KEY_PASSWORD`, `BRUH_KEYSTORE`)
- [x] **Codemagic env vars** — **DONE 2026-04-13**: all 5 Vite public vars (`VITE_SUPABASE_URL/ANON_KEY`, `VITE_SENTRY_DSN`, `VITE_POSTHOG_KEY/HOST`) added to both workflows; `secrets` group imported for `SENTRY_AUTH_TOKEN` source map uploads; `sentryVitePlugin` guarded behind `!!SENTRY_AUTH_TOKEN`
- [x] **`MIN_REGIONAL_USERS`** — already `5` in `generate-regional-challenges/index.ts` ([[Regional AI Challenges]])
- [ ] Supabase Auth → **Leaked password protection** (HaveIBeenPwned) — **DEFERRED**: only matters for premium tier; remind when premium goes live
- [x] **`landing/u.html`**: App Store ID `6761007303` confirmed in `apple-itunes-app` meta ✅

### Recurring: Apple Sign In JWT renewal
> [!warning] Apple Sign In client secret JWT **expires 2026-09-26**. Regenerate using `generate-apple-jwt.mjs` (repo root) and update Supabase Apple provider → Secret Key before this date. See [[iOS & Android]] for key details.

---

## App Store Connect / App Review

| Item | Status / notes |
|------|----------------|
| App ID (ASC) | `6761007303` |
| Bundle ID | `app.bruhsocial.app` |
| Product | `bruh_pro_weekly` — $0.99/wk — see [[Monetization]] |
| Test account | `applereview` / `BruhReview2026!` (custom password auth — rotate if policy changes) |
| **Rejection (2026-03-25)** | Guideline **2.1** Information Needed — replied with recording + credentials |
| **Rejection (2026-04-05)** | Guideline **3.1.2(c)** (Privacy Policy URL + EULA missing in ASC) + Guideline **2.1(b)** (IAP not responsive; Paid Apps Agreement missing) |
| **Resubmission (2026-04-14)** | ✅ **IN REVIEW** — all issues resolved (see [[App Review History]]) |

Screenshots: ✅ uploaded.

---

## Supabase secrets (inventory)

| Secret | Purpose |
|--------|---------|
| `RESEND_API_KEY`, `FROM_EMAIL` | Email |
| `CRON_SECRET` | Cron + many edge paths |
| `GIPHY_API_KEY`, `KLIPY_API_KEY` | Media |
| `WEBHOOK_SECRET` | Push edge auth |
| FCM fields | Push delivery |
| `REVENUECAT_*` | [[Payment Webhook Security]] |
| `CAPGO_API_KEY` | [[Capgo OTA]] / `capgo-proxy` |
| `EMERGENCY_SECRET`, `TURNSTILE_SECRET_KEY` | Optional / break-glass |
| `EDGE_ADMIN_ALLOWED_ORIGINS` | Admin edge CORS |
| `GNEWS_API_KEY`, `GEMINI_API_KEY` | [[Regional AI Challenges]] |
| Marketing sync secrets | [[Analytics Dashboard]] |

> [!warning] **Never** paste secret **values** into this vault or chat. Full name list: [[Security Reference]].

---

## Post-approval / ongoing

- Google Play upload (Android often manual vs iOS Codemagic)
- Monitor **Sentry** ([[Sentry]]) — **metric / session / performance alert rules deferred** until paid Sentry tier; use Issues + `scripts/sentry-tail.js` meanwhile (see [[Sentry]])
- **Uptime:** optional **UptimeRobot** (or similar) on `GET …/functions/v1/health-check` — steps in repo `scripts/INCIDENT_RUNBOOK.md` (full ops checklist there)
- Verify AdMob UMP in EU
- Netlify: redeploy `landing/` after contact form / CSP changes ([[Deploy Targets]])

---

## See also

- [[App Review History]]
- [[Codemagic CI]]
- [[Monetization]]
- [[🏠 Home]]
