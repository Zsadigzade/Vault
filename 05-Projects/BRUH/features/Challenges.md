---
tags: [features, challenges, regional, ai, cron, gemini]
area: features
updated: 2026-04-03
---

# Challenges

> [!tip] Deep dive on **AI regional** pipeline (Gemini, GNews, cron body, admin monitor): [[Regional AI Challenges]].

## Two Types

| Type | Source | Scope | Approval |
|------|--------|-------|----------|
| Global challenges | Admin-created manually | All users | Admin CRUD + activation |
| Regional challenges | AI-generated (GNews + Gemini) | Per-country users | **Cron** → auto `active`; **admin trigger** → `pending` until approve — see [[Regional AI Challenges]] |

---

## Regional Challenges (summary)

### How It Works

```
Every 3 days (cron: 0 9 */3 * *)
  → generate-regional-challenges edge fn (body: triggered_by: "cron")
  → Per region (batches of 5): GNews → Gemini 2.5 Flash → insert regional_challenges
  → Cron runs: auto active + date window; admin RPC runs: pending for review
```

### Region Detection
Cloudflare `cf-ipcountry` + fallback `Accept-Language` — **zero GPS permission**. Edge: `detect-region`.

### Database (summary)

Table **`regional_challenges`**: `region`, `prompt`, `emoji`, `gradient`, `status` (`pending`|`active`|`rejected`), `source_topics`, `starts_at`, `ends_at`, `generated_at`, etc. Full schema: [[Regional AI Challenges]].

### Concurrency
5 regions processed in parallel per batch to avoid Supabase edge function 150s timeout limit.

### Threshold

| Setting | Current Value | Recommended for Prod |
|---------|--------------|---------------------|
| `MIN_REGIONAL_USERS` | `1` | `5` to `10` |

> [!warning] Set `MIN_REGIONAL_USERS` to at least 5 before global launch to avoid generating challenges for single-user regions.

---

## Challenge Query Pattern

The `["active-challenges"]` query merges global + regional:

```ts
// src/lib/queryKeys.ts
CHALLENGES_QUERY_KEY = ["active-challenges"]
regionalChallengesKey(region) = ["regional-challenges", region]
```

Both are fetched and merged client-side when displaying to users. `staleTime: 5m` for both.

---

## Admin Management

Via ops admin (`admin.bruhsocial.app`) → **Challenges tab**:
- View all global + regional challenges
- Create/edit/delete global challenges
- Trigger regional generation manually for a specific region
- Monitor generation logs
- Admin-triggered challenges stay **pending** (not auto-approved) — requires manual approval

---

## Generation RPC / Cron Config

**Cron schedule**: `0 9 */3 * *` (9 AM UTC every 3 days)

**Migration**: `20260403140000_regional_challenges_cron_body_triggered_by.sql`
- Added `triggered_by` field to distinguish cron vs admin-triggered
- Added JSON body to cron invocation for richer logging

---

## Required Secrets

| Secret | Purpose |
|--------|---------|
| `GNEWS_API_KEY` | Fetch trending news by region |
| `GEMINI_API_KEY` | Generate challenge text via Gemini 2.5 Flash |
| `CRON_SECRET` | Authenticate scheduled cron calls to edge fn |

---

## Question bank (`challenge_questions` table)

Separate from live `challenges` rows — prompt library for admins:
- Managed via ops admin → **Questions** tab
- Import via CSV or manual CRUD
- Global (not regional)

See [[Database Reference]] for related tables.

---

## See also

- [[Regional AI Challenges]]
- [[Dashboards]]
- [[Edge Functions]]
- [[🏠 Home]]
