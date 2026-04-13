---
tags: [database, edge-functions, supabase, backend]
area: database
updated: 2026-04-08
---

# Edge Functions

**Folder:** `supabase/functions/` · **Project:** `gpainqlxdakaczkgozko`  
Deploy: `npx supabase functions deploy <name> --project-ref gpainqlxdakaczkgozko`

> [!note] **27** function packages in repo (each with `index.ts`). Names use **kebab-case** folders.

---

## Function catalog

| Function | `verify_jwt` (gateway) | Auth / notes | Key secrets |
|----------|------------------------|--------------|-------------|
| `send-push-notification` | `false` | `WEBHOOK_SECRET` timing-safe; handles **`notifications`** + **`chat_messages`** INSERT webhooks (mute + `preferences.chatMessages`) | `WEBHOOK_SECRET`, FCM service account |
| `media-proxy` | default (`true` typical) | User JWT **or** anon key for GIF/sticker proxy; killswitch read | `GIPHY_API_KEY`, `KLIPY_API_KEY` |
| `capgo-proxy` | `false` | Validates admin JWT + `is_admin()` inside | `CAPGO_API_KEY`, `EDGE_ADMIN_ALLOWED_ORIGINS` |
| `revenuecat-webhook` | `false` | Authorization / optional HMAC | [[Payment Webhook Security]] |
| `verify-turnstile` | `false` | Server Turnstile verify | `TURNSTILE_SECRET_KEY` |
| `rate-limiter` | default | Client-called buckets; fail-closed on DB error | — |
| `send-admin-reply` | default | Admin JWT + CORS | `RESEND_*`, `FROM_EMAIL`, `EDGE_ADMIN_ALLOWED_ORIGINS` |
| `inbound-email-forward` | `false` | Svix / Resend webhook | `RESEND_WEBHOOK_SECRET`, optional `FORWARD_TO_EMAIL` |
| `generate-regional-challenges` | often **`verify_jwt = false`** at deploy (cron `Bearer`) — not always in `config.toml` | `CRON_SECRET` + vault | `CRON_SECRET`, `GEMINI_API_KEY`, `GNEWS_API_KEY` |
| `send-reengagement-pushes` | `false` | `CRON_SECRET` | `CRON_SECRET`, FCM |
| `analyze-behavior` | `false` | `CRON_SECRET` | `CRON_SECRET` |
| `send-verification-email` | `false` | IP rate limit in handler | `RESEND_API_KEY`, `FROM_EMAIL` |
| `send-verification-email-batched` | default | Batched sends | Resend |
| `process-email-queue` | default | `CRON_SECRET` if set | `CRON_SECRET`, Resend |
| `request-password-reset` | `false` | IP rate limit | Resend |
| `detect-region` | `false` | JWT validated in code for DB update | — |
| `fortune-spin` | **`false`** (`config.toml`) | User JWT via **`getUser(token)`**; **`status`** / **`spin`** / **`complete_ad`**; updates **`users`** wheel + temp premium; **`check_and_increment_rate_limit`** (`fortune_spin`) | — |
| `website-contact-submit` | `false` | Public form; honeypot + IP limit | Service role insert |
| `convert-webm-to-mp4` | `true` | `getUser(token)` | size limits in handler |
| `sync-admob-stats` | `false` | `requireSyncCaller`: CRON or dashboard/admin JWT | Google OAuth secrets |
| `sync-appstore-stats` | `false` | same | App Store Connect API |
| `sync-playstore-stats` | `false` | same | Play service account JSON |
| `sync-revenuecat-stats` | `false` | same; often DB-derived MRR | optional RC API |
| `sync-firebase-stats` | `false` | same | Firebase / GA4 |
| `cleanup-webhook-data` | default | `CRON_SECRET` timing-safe | `CRON_SECRET` |
| `emergency-set-mode` | `false` | Bearer `EMERGENCY_SECRET`; toggles **`app_killswitch`**, **`emergency_api_lock`**, **`maintenance_mode`** (and other allowlisted flags) | `EMERGENCY_SECRET` |
| `health-check` | **`false`** | **Uptime / synthetic monitor** — JSON `status` + DB ping inside handler; callable without user JWT | — |

> [!tip] Exact `verify_jwt` for functions **not** listed in `config.toml` follows Supabase defaults — confirm in `supabase/config.toml` after pulls.

---

## Shared (`_shared/`)

| File | Use |
|------|-----|
| `timingSafeEqual.ts` | Secret comparisons |
| `corsForAdmin.ts` | Admin-only CORS allowlist |
| `syncAuth.ts` | `sync-*-stats` caller auth |

---

## See also

- [[Security Reference]]
- [[Payment Webhook Security]]
- [[Migrations Log]]
- [[Chat System]]
- [[12 - MCP & External APIs]]
- [[🏠 Home]]
