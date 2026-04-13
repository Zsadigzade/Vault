---
tags: [database, schema, rpc, supabase, feature-flags]
area: database
updated: 2026-04-06
---

# Database Reference

**Project:** `gpainqlxdakaczkgozko` · West EU (Ireland)

---

## Key tables (summary)

| Table | Notes |
|-------|--------|
| `users` | `id`, `auth_id`, `username`, `current_question`, `subscription_status`, `subscription_expires_at`, `region`, `region_updated_at`, … |
| `posts` | `id`, `user_id`, `question`, `created_at`, `expires_at` — **no** `reply_count` column; counts via RPC |
| `replies` | `recipient_id`, `post_id`, `sender_id` (nullable), `meme_url`, `frame_data`, `comment_text`, `status`, …; `post_id` **ON DELETE SET NULL**; scrub on post delete → `[expired]` sentinel |
| `challenges` | Global prompts; admin write via `is_admin()` |
| `regional_challenges` | AI regional; `status` pending/active/rejected |
| `challenge_questions` | Question bank; admin RLS |
| `user_saved_stickers` | Premium sticker sync; policies use **`DROP POLICY IF EXISTS`** for idempotent migrations |
| `meme_analytics` | Trending counters; **not** derived from reply row retention |
| `notifications`, `broadcasts`, `push_tokens`, `reports`, `banned_users` | Standard product tables; `notifications.type` includes **`chat`** |
| `conversations`, `conversation_participants`, `chat_messages` | 1:1 DMs — see [[Chat System]] |
| `admin_users`, `admin_audit_log` | Ops roles + audit |
| `feature_flags` | Public read; writes via RPC only ([[Security Reference]]) |
| `contact_submissions`, `website_contact_submissions` | Support; website via edge fn only |
| `inbound_forward_emails` | Resend inbound notification recipients (additive) |
| `webhook_events`, `webhook_rate_limits`, `subscription_fraud_signals`, `subscription_changes` | Webhook idempotency / abuse / audit |
| `generation_runs`, `generation_logs`, `regional_trending` | Regional AI pipeline |
| `dashboard_users` | [[Analytics Dashboard]] access |
| `error_logs`, `email_queue` | Admin realtime ([[Dashboards]]) |

### External stats cache

`external_stats_admob`, `external_stats_appstore`, `external_stats_playstore`, `external_stats_revenuecat`, `external_stats_firebase` — filled by `sync-*-stats` ([[Analytics Dashboard]]).

---

## Critical RPCs — identity

| RPC | Purpose |
|-----|---------|
| `get_my_user_id()` | SECURITY DEFINER — app user id from session; **use for all authz** on password + OAuth paths |
| `is_admin()` | No-arg; `auth.uid()` only — **never** parameterized (enumeration fix) |
| `is_superadmin()` | Catastrophic feature flags |
| `is_dashboard_user()` | Analytics app |
| `relink_auth_by_user_id(p_user_id, p_new_auth_id)` | **`p_new_auth_id` must equal `auth.uid()`** (audit) |

---

## Inbox / posts / replies / analytics (IDOR-hardened)

| RPC | Auth note |
|-----|-----------|
| `fetch_my_posts(p_user_id)` | **`get_my_user_id()` only** — param ignored for auth |
| `fetch_replies_inbox(p_user_id)` | same |
| `fetch_replies_for_post(...)` | same; keyset pagination; `p_limit` 1–200 |
| `fetch_sent_replies(p_user_id)` | same |
| `get_meme_recommendations(...)` | same; `p_limit` 1–100 |
| `increment_meme_analytics_reply` / `_view` | **`REVOKE` from `anon`** — authenticated session required |

---

## Moderation & settings

| RPC | Notes |
|-----|--------|
| `approve_reply`, `reject_reply`, `set_review_first`, `get_filter_settings` | **`get_my_user_id()` only** (no client UUID) |
| `submit_report` | Reporter id from server; self-report blocked |
| `upsert_push_token` | Rejects null session |

---

## Admin / ops RPCs (sample)

| RPC | Purpose |
|-----|---------|
| `get_pending_reports`, `ban_user`, `warn_user`, `dismiss_report`, `unban_user` | Moderation |
| `admin_set_subscription`, `admin_bulk_resolve_errors`, … | See [[Dashboards]] |
| `admin_delete_app_contact`, `admin_delete_website_contact`, bulk resolved deletes | Contact cleanup |
| `cleanup_old_resolved_contact_submissions` | pg_cron retention |
| `get_content_performance_stats` | Admin content tab |
| `admin_set_feature_flag`, `admin_delete_feature_flag` | Flags; super_admin for killswitch names |
| `get_ratings_aggregate` | Admin; **`anon` revoked** |
| `lookup_user_for_oauth_email_conflict`, `get_public_user_id_by_username`, … | Replace open `users` reads |

---

## Regional AI

| RPC | Purpose |
|-----|---------|
| `admin_trigger_regional_generation`, `admin_trigger_all_regions_generation` | pg_net → edge |
| `approve_regional_challenge`, `reject_regional_challenge` | Pending → active/rejected |

---

## Chat (1:1)

Migrations **`20260415120000_chat_system.sql`** (base) + **`20260416180000_chat_improvements.sql`** + **`20260417120000_chat_performance.sql`** (RPC/query perf — [[Chat System — Performance]]). Table name is **`chat_messages`** (not `messages`).

| RPC | Notes |
|-----|--------|
| `start_conversation(p_reply_id)` | Post owner + existing reply; dedupes by user pair; clears **`left_at`** on reopen for both participants |
| `get_my_conversations`, `get_conversation_messages`, `get_conversation_meta` | Participant-only reads; list excludes **`left_at`** rows; messages return **`deleted_at`**, **`reply_*`**, **`reactions` jsonb** |
| `send_chat_message` | Premium (+ 48h grace), blocks, **100 msgs/sender/UTC day**; optional **`p_reply_to_id`** |
| `mark_conversation_read`, `mute_conversation` | Participant UX (active participant only) |
| `delete_chat_message` | Own message, **24h** window, soft-delete |
| `toggle_chat_reaction` | Premium; insert/remove reaction row |
| `leave_conversation` | Sets **`conversation_participants.left_at`** |

---

## Feature flags (rows)

| Key | Notes |
|-----|--------|
| `registration_open`, `maintenance_mode` | Consumer gating |
| `app_killswitch`, `emergency_api_lock` | **Super-admin** only via RPC; `media-proxy` 503 when set |

---

## Client: expired reply UI

- **`REPLY_MEME_EXPIRED_SENTINEL`** = `[expired]` · **`isReplyMemeMediaExpired()`** in `src/lib/user/types.ts`.

---

## `submitContactForm` (client)

Direct insert with FK fallback: `error.code === "23503"` → retry `user_id: null`.

---

## PostgrestFilterBuilder

> [!warning] **Not** a full `Promise` — **no `.catch()`**. Use `.then(({ error }) => …)`.

---

## Migration drift

```bash
npx supabase migration repair --status reverted <id>
npx supabase db push --yes
# or
npx supabase db pull
```

---

## See also

- [[Migrations Log]]
- [[Edge Functions]]
- [[Security Reference]]
- [[Regional AI Challenges]]
- [[Chat System]]
- [[🏠 Home]]
