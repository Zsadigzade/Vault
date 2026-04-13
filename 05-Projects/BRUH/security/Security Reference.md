---
tags: [security, rls, csp, hardening, auth, audit]
area: security
updated: 2026-04-05
---

# Security Reference

> [!important] Last major audit: **`20260411120000_comprehensive_security_audit`** (DB + edge + client). See [[Migrations Log]] for filenames. Deep webhook rules: [[Payment Webhook Security]].

**Ops tokens:** If an API key was ever pasted into chat or logs, **rotate** it in the provider dashboard and update **only** `.cursor/.env.mcp.local` (or provider UI) — never the vault. Example (2026-04): **UptimeRobot** key rotated after MCP troubleshooting.

---

## `20260411120000` — compact summary

| Area | Change |
|------|--------|
| **DB** | `relink_auth_by_user_id` → `p_new_auth_id = auth.uid()`; replies INSERT **`sender_id = get_my_user_id()`** + non-null session; replies SELECT participant/admin; `users` SELECT tightened; `fetch_my_posts` + moderator RPCs → **`get_my_user_id()` only**; **`upsert_push_token`** rejects null session; meme_analytics direct INSERT/UPDATE policies dropped; **`get_ratings_aggregate`** admin + **`anon` revoked**; duplicate `feature_flags` read policy dropped; **`admin_audit_log`** + triggers (username cooldown, daily reply cap); **`replies.frame_data`** size cap |
| **Edge** | `timingSafeEqual` on cron/sync paths; **`corsForAdmin`** on `send-admin-reply` / `capgo-proxy`; generic errors on several handlers; **`verify-turnstile`**; **`rate-limiter`** bucket **`reply_create`** |
| **Client** | `checkRateLimit` fail-closed; Turnstile + 8-char password register; **`safeRedirect`**; admin bulk confirms; OAuth tests use **`lookup_user_for_oauth_email_conflict`** |

> [!warning] **`security.md` (external memory) once mentioned `Keyboard.resize: 'body'`** — **wrong for this project.** Canonical keyboard config: **`resize: 'none'`** — see [[Keyboard & Layout]] and [[Critical Gotchas]].

---

## RLS (Row Level Security) Patterns

### Core Principle
Password-auth users use anon Supabase sessions. Standard `auth.uid()` won't match `bruh_user_id`. All security-critical operations use SECURITY DEFINER RPCs with `get_my_user_id()`.

```sql
-- ✅ Correct pattern — derive ID server-side
CREATE POLICY "Users can see own posts" ON posts
  FOR SELECT USING (user_id = get_my_user_id());

-- ❌ Wrong — auth.uid() doesn't match bruh_user_id for password-auth users
CREATE POLICY "bad" ON posts
  FOR SELECT USING (user_id = auth.uid());
```

### Fixed IDOR Vulnerabilities (2026-04-11)

| Table | Was | Fixed |
|-------|-----|-------|
| `replies` INSERT | Client-supplied sender_id | `get_my_user_id()` only |
| `replies` SELECT | Open (could read others') | Own records only |
| `users` SELECT | Open (anyone could read all) | Restricted + helper RPCs |
| `relink_auth` | Could link any user's auth | Own `auth.uid()` only |
| `fetch_my_posts` | COALESCE(client UUID, session) | `get_my_user_id()` only |
| Moderator RPCs | Client-supplied user IDs | `get_my_user_id()` only |

### Admin Security

```sql
-- is_admin() — no-arg, not enumerable from client
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM admin_users WHERE user_id = get_my_user_id()
  );
$$ LANGUAGE sql SECURITY DEFINER SET search_path = public;
```

- `admin_users` SELECT is restricted (not public)
- Super-admin gates on `app_killswitch` and `emergency_api_lock`

---

## Rate Limits & Caps

| Limit | Value | Enforcement |
|-------|-------|-------------|
| Replies per user per UTC day | 50 | DB trigger |
| Username changes | 1 per 7 days | DB trigger |
| `replies.frame_data` | ≤ 5MB | DB CHECK constraint |
| Login attempts | 10 per 5 min | Client localStorage |
| Password reset requests | 3 per 5 min | Client localStorage |
| Media proxy requests | 60 per min per IP | Edge function |
| Reply/post/report mutations | Per-user throttle | `rate-limiter` edge fn |

---

## Edge Function Security

### `revenuecat-webhook`
```ts
// Authorization: rawToken OR "Bearer <token>"
const authHeader = req.headers.get('Authorization') ?? '';
const token = authHeader.startsWith('Bearer ') 
  ? authHeader.slice(7) 
  : authHeader;
await timingSafeEqual(token, REVENUECAT_WEBHOOK_SECRET);
```
- Non-UUID `app_user_id` → return 200 (skip gracefully)
- `REVENUECAT_SECRET_KEY` required for hybrid REST verify — **fail-closed** without it
- HMAC layer optional via `REVENUECAT_WEBHOOK_VERIFICATION_SECRET`

### Admin Edge Functions
- All protected by `corsForAdmin.ts`
- `EDGE_ADMIN_ALLOWED_ORIGINS` secret controls allowed CORS origins
- Admin JWT verified via Supabase before any action

### Timing-Safe Comparisons
All secret comparisons use `_shared/timingSafeEqual.ts` to prevent timing attacks on `CRON_SECRET`, webhook tokens, etc.

---

## Client-Side Security

### `safeRedirect.ts`
Used on all auth screens to prevent open redirect attacks:
```ts
import { safeRedirect } from '@/lib/safeRedirect';
// Validates redirect URL is same-origin before navigating
```

### Deep Link Allowlist
Only these paths trigger in-app navigation (in `DeepLinkHandler` in `App.tsx`):
- `/u/username/postId`
- `/post/postId`

All other deep link paths → ignored (no navigation).

### Client Rate Limiting (localStorage)
```ts
// Login: 10 attempts per 5 minutes
// Password reset: 3 attempts per 5 minutes
// Checked before making Supabase calls
```

### Password OTP Rule
Password reset OTP is **never returned to the component** — handled internally by Resend email service. Components never see the token.

---

## Content Security Policy

### Main App (`index.html` meta tag)
```
connect-src: 
  - *.supabase.co (Supabase)
  - api.giphy.com (GIF search)
  - *.googleapis.com (FCM/Firebase)
  - *.sentry.io (error tracking)
  - challenges.cloudflare.com (Turnstile)
  - eu.posthog.com (analytics)
```
No `unsafe-eval` allowed.

### Landing Site (`landing/netlify.toml`)
CSP headers set + XSS fix applied (2026-04-11).

### `public/_headers` (Netlify)
Security headers file activated. Sets:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`

### `vercel.json` (Dashboards)
Security headers on analytics + ops admin Vercel deployments.

---

## Secrets — Fail-Closed Behavior

| Secret | Behavior if missing |
|--------|-------------------|
| `REVENUECAT_SECRET_KEY` | Webhook hybrid verify → **fail closed** (rejects all) |
| `REVENUECAT_WEBHOOK_SECRET` | Webhook → rejects all (no auth check possible) |
| `CRON_SECRET` | Cron fns → reject all scheduled calls |
| `EDGE_ADMIN_ALLOWED_ORIGINS` | Admin fns → reject all CORS |

---

## Supabase secrets inventory (names only)

Set via `npx supabase secrets set KEY=value --project-ref gpainqlxdakaczkgozko`. **Never commit values.**

| Secret | Used by (typical) |
|--------|-------------------|
| `RESEND_API_KEY`, `FROM_EMAIL` | Email send / queue |
| `CRON_SECRET` | `process-email-queue`, `cleanup-webhook-data`, `sync-*`, `send-reengagement-pushes`, `analyze-behavior` |
| `RESEND_WEBHOOK_SECRET`, `FORWARD_TO_EMAIL`, `FORWARD_TO_DMARC_EXCLUDED` | `inbound-email-forward` |
| `GIPHY_API_KEY`, `KLIPY_API_KEY` | `media-proxy` |
| `WEBHOOK_SECRET` | `send-push-notification` |
| FCM service account fields | `send-push-notification`, re-engagement |
| `REVENUECAT_WEBHOOK_SECRET`, `REVENUECAT_SECRET_KEY`, `REVENUECAT_WEBHOOK_VERIFICATION_SECRET` (opt) | `revenuecat-webhook` |
| `CAPGO_API_KEY` | `capgo-proxy` |
| `EMERGENCY_SECRET` | `emergency-set-mode` |
| `TURNSTILE_SECRET_KEY` | `verify-turnstile` |
| Marketing sync | `ADMOB_*`, `APPSTORE_*`, `PLAY_*`, `FIREBASE_*`, optional `REVENUECAT_PROJECT_ID` |
| `GEMINI_API_KEY`, `GNEWS_API_KEY` | `generate-regional-challenges` |

---

## `verify_jwt` (gateway) — see repo

Per-function overrides live in **`supabase/config.toml`**. Many public/webhook/cron handlers use **`verify_jwt = false`** with **auth inside the handler** (timing-safe secrets, `requireSyncCaller`, etc.). Only **`convert-webm-to-mp4`** is explicitly **`true`** in the committed snippet — re-read `config.toml` after pull.

---

## Remaining follow-ups

- Rotate any **exposed** GCP service account keys; optional git history scrub.  
- Prefer **env-only** for PII in new migrations (avoid seeding real emails in SQL).

---

## Security Checklist for New Features

- [ ] Server-side identity via `get_my_user_id()` — never accept client UUID for auth
- [ ] Use `timingSafeEqual` for any secret comparison
- [ ] Apply `corsForAdmin` if endpoint is admin-only
- [ ] Add to CSP `connect-src` if new external service
- [ ] Rate-limit if mutation endpoint (use `rate-limiter` edge fn)
- [ ] Set `SET search_path = public` on all SECURITY DEFINER functions
- [ ] Deep links: add to allowlist only if truly needed

---

## See also

- [[Payment Webhook Security]]
- [[App Review History]]
- [[Edge Functions]]
- [[Database Reference]]
- [[12 - MCP & External APIs]]
- [[🏠 Home]]
