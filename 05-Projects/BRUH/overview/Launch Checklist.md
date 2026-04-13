---
tags: [overview, launch, checklist, secrets]
area: overview
updated: 2026-04-05
---

# Launch Checklist

---

## Pre-launch TODOs

- [ ] Configure **UMP** consent form for EU/GDPR (AdMob console)
- [ ] Upload **Android keystore** to Codemagic
- [ ] Codemagic env: `CM_KEYSTORE_PASSWORD`, `CM_KEY_ALIAS`, `CM_KEY_PASSWORD`
- [ ] Supabase Auth → **Leaked password protection** (HaveIBeenPwned)
- [ ] Raise **`MIN_REGIONAL_USERS`** from `1` → `5`–`10` for production ([[Regional AI Challenges]])
- [ ] **`landing/u.html`**: confirm App Store numeric ID in `apple-itunes-app` meta if still placeholder ([[Deep Links & PWA]])

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
| **Rejection (2026-03-25)** | Guideline **2.1** Information Needed — not policy violation; Apple requested documentation + recording |
| **Resubmission** | Use [[App Review History]] — Terms/Privacy from subscription flow, white-screen fixes, native storage gate |

Screenshots: ensure **6.5"** set present in ASC.

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
