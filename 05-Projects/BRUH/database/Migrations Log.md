---
tags: [database, migrations, history]
area: database
updated: 2026-04-08
---

# Migrations Log

**Latest (repo):** `20260420120000_fortune_wheel_temp_premium` — **`users`** fortune-wheel columns (`last_fortune_spin_at`, `fortune_spins_today`, `fortune_spins_date`, `fortune_pending_ad`, **`temp_premium_until`**); **`_user_is_premium_chat`** includes **`temp_premium_until > now()`** for chat premium gate. Edge: **`fortune-spin`**. → [[Monetization]] · [[Edge Functions]].

Prior: `20260419120000_challenge_auto_generation_and_bulk_resolve_errors` — **`feature_flags.challenge_auto_generation`**; cron guard; **`admin_bulk_resolve_errors()`**. → [[Dashboards]] · [[Regional AI Challenges]].

Prior: `20260417120000_chat_performance` — faster chat RPCs (daily count index use, batched reactions/unread, `start_conversation` join). Requires **`20260416180000`** + **`20260415120000`** already applied ([[Chat System — Performance]] · [[Chat System]] · [[Database Reference]]).

---

## Migration History (Newest First)

| Migration ID | Date | Summary |
|---|---|---|
| `20260420120000` | 2026-04-20 | **Fortune wheel + temp premium** — `users` spin state + **`temp_premium_until`**; **`_user_is_premium_chat`** temp-premium branch |
| `20260419120000` | 2026-04-19 | **Ops admin** — `challenge_auto_generation` feature flag; cron **`generate-regional-challenges`** guarded; **`admin_bulk_resolve_errors()`** bulk-resolve open `error_logs` for admins |
| `20260417120000` | 2026-04-17 | **Chat performance** — `send_chat_message` UTC-day range count; `get_conversation_messages` + `get_my_conversations` batch aggregates; `start_conversation` participant-join lookup |
| `20260416180000` | 2026-04-16 | **Chat improvements** — `left_at`, `last_message_sender_id`, `deleted_at`, `reply_to_id`, `chat_message_reactions`; RPCs `delete_chat_message`, `toggle_chat_reaction`, `leave_conversation`; extended `get_*` / `send_chat_message` (`p_reply_to_id`); realtime on reactions; `start_conversation` clears `left_at` on reopen |
| `20260415120000` | 2026-04-15 | **Chat system** — `conversations`, `conversation_participants`, `chat_messages`; RPCs + RLS + realtime; `notifications.type` **`chat`**; trigger → `send-push-notification` for `chat_messages` |
| `20260411120000` | 2026-04-11 | **Comprehensive security audit** — replies IDOR fix, admin_users locked, `get_my_user_id()` enforced on all RPCs, `upsert_push_token` null session check, username 7d cooldown, 50 replies/day cap, `frame_data` ≤5MB, `admin_audit_log`, helper RPCs for blocked `users` reads |
| `20260410120000` | 2026-04-10 | Feature flags RPC + killswitch — `get-feature-flags` RPC, `app_killswitch` + `emergency_api_lock` super_admin gates |
| `20260409120000` | 2026-04-09 | Contact admin + realtime tables — `contact_submissions`, realtime `admin_audit_log` and `email_queue` tables |
| `20260408120000` | 2026-04-08 | Cron + sticker policies — sticker pack/sticker INSERT policies with `DROP POLICY IF EXISTS` for idempotent push |
| `20260407120000` | 2026-04-07 | DB scrub — PII cleanup and data retention rules |
| `20260406120000` | 2026-04-06 | Sticker schema — `sticker_packs`, `stickers` tables |
| `20260405120000` | 2026-04-05 | Inbox/sent IDOR fix — sender/receiver filtering hardened |
| `20260403140000` | 2026-04-03 | Regional challenges cron JSON body + admin RPC `triggered_by` field |
| `20260402120000` | 2026-04-02 | Inbound email forwarding — `inbound_forward_emails` table, edge fn webhook |
| Earlier | Pre-2026-04 | Core schema: `users`, `posts`, `replies`, `challenges`, `notifications`, `broadcasts`, `reports`, `admin_users` |

---

## Key Changes in 2026-04-11 Audit

### Database
- `relink_auth` → own `auth.uid()` only (was exploitable)
- `replies` INSERT/SELECT locked to own records via `get_my_user_id()`
- `users` SELECT restricted (was open) — helper RPCs added for admin reads
- `fetch_my_posts` + all moderator RPCs → `get_my_user_id()` only (no COALESCE client UUID)
- `upsert_push_token` rejects null session
- `meme_analytics` — no direct INSERT/UPDATE RLS
- `get_ratings_aggregate` — admin-only
- `replies.frame_data` ≤5MB CHECK constraint
- 7-day username change cooldown
- 50 replies/user/UTC day limit
- `admin_audit_log` table + helper RPCs added

### Edge Functions (same batch)
- `_shared/timingSafeEqual.ts` added
- `corsForAdmin.ts` + `EDGE_ADMIN_ALLOWED_ORIGINS` secret
- `verify-turnstile` edge function added
- `revenuecat-webhook` hardened (Bearer prefix, non-UUID skip, fail-closed)

### Client (same batch)
- `rate-limiter` server-side on post/reply/report
- Optional Turnstile on register
- `safeRedirect.ts` on auth screens
- Landing XSS fix + CSP in `landing/netlify.toml`
- `public/_headers` activated

---

## Migration Drift Fix

If remote Supabase DB has migrations not present locally:

```bash
# Option 1: repair + push
npx supabase migration repair --status reverted <migration_id>
npx supabase db push --yes

# Option 2: pull all remote state
npx supabase db pull
```

> [!note] Drift happens when migrations are applied via Supabase dashboard SQL editor or directly on remote without going through local CLI.

---

## Apply New Migration

```bash
# 1. Create migration file
npx supabase migration new <name>

# 2. Edit the SQL file in supabase/migrations/

# 3. Push to remote
npx supabase db push --yes

# 4. Verify
npx supabase migration list
```
