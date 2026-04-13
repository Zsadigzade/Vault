---
tags: [features, challenges, regional, ai, gnews, gemini, cron]
area: features
updated: 2026-04-07
---

# Regional AI Challenges

> [!tip] **Global** manual challenges live in `challenges` + admin CRUD. **Regional** AI challenges are a **second** system — table `regional_challenges`, edge fn `generate-regional-challenges`. Overview: [[Challenges]].

---

## Behavior (cron vs admin)

| Trigger | Body | Result |
|---------|------|--------|
| **pg_cron** | `triggered_by: "cron"` | Inserts **`active`** with `starts_at` / `ends_at` (~3-day window) — **auto-published** — **unless** `feature_flags.challenge_auto_generation` is **disabled** (cron still runs; **no** HTTP call to the edge fn) |
| **Admin RPC** | `triggered_by: "admin"` | Inserts **`pending`** — approve/reject in admin **Challenges** tab |

Migrations: `20260403140000_regional_challenges_cron_body_triggered_by.sql` (cron JSON body + admin RPCs send `admin`); **`20260419120000_challenge_auto_generation_and_bulk_resolve_errors.sql`** (flag + guarded cron). **Admin UI:** Challenges tab → **Cron auto-generation** ON/OFF (uses `setFeatureFlag`).

---

## Region detection (zero permission)

| Source | Detail |
|--------|--------|
| **Primary** | Cloudflare **`cf-ipcountry`** on Supabase edge requests |
| **Fallback** | `Accept-Language` (e.g. `tr-TR` → `TR`) |
| **Edge fn** | `detect-region` — JWT-bound DB update; client: `src/lib/user/challenges.ts` |
| **Client cache** | `bruh_user_region` + `bruh_user_region_ts`, TTL **1 day** |
| **DB** | `users.region`, `users.region_updated_at` |
| **Gotcha** | VPN exit country ≠ physical location |

---

## Database

### `regional_challenges`

| Column | Notes |
|--------|--------|
| `status` | `pending` \| `active` \| `rejected` |
| `source_topics` | JSONB (headlines / context) |
| `starts_at` / `ends_at` | Set when activated |

RLS: public read **`active`**; admin full access.

### `regional_trending`, `generation_runs`, `generation_logs`

- Trending headline cache; per-run metrics; terminal logs for admin monitor.  
- Realtime: `REPLICA IDENTITY FULL` where needed for postgres_changes.

---

## Edge: `generate-regional-challenges`

- Auth: **`Authorization: Bearer CRON_SECRET`** (admin path: RPC + pg_net, not direct browser).
- Secrets: `CRON_SECRET`, `GEMINI_API_KEY`, `GNEWS_API_KEY` (vault/secrets).
- **GNews:** daily limit **100**; `allRegions` mode uses parallel batch / global headlines to save quota.
- **Gemini:** `v1beta` + **`gemini-2.5-flash`**; **`thinkingBudget: 0`**; filter `parts` with `thought: true`; no `responseMimeType` on v1beta.
- **Concurrency:** batches of **5** regions (timeout ~150s).
- **Cancellation:** checks `generation_runs.status` between batches.
- **`MIN_REGIONAL_USERS`:** code constant (raise to **5–10** for prod — see [[Launch Checklist]]).

---

## RPCs

| RPC | Purpose |
|-----|---------|
| `admin_trigger_regional_generation(p_region?)` | pg_net POST to edge fn |
| `admin_trigger_all_regions_generation()` | `allRegions: true` |
| `approve_regional_challenge(id, interval_days)` | `pending` → `active` |
| `reject_regional_challenge(id)` | → `rejected` |

---

## Client

- `src/lib/user/challenges.ts` — detect, fetch active/pending, trigger, cancel run.
- `src/lib/queryKeys.ts` — `regionalChallengesQueryKey(region)`, `PENDING_REGIONAL_CHALLENGES_QUERY_KEY`.
- `ChallengesScreen.tsx` — merges regional (up to 7) + global (pad to 10), dedupe by prompt.

---

## Admin UI (`AdminChallenges`)

- **GenerationMonitor** — realtime logs, stop generation, clear completed runs.
- **RegionalAIPanel** — GNews quota bar, Active Regions / All Regions buttons, pending grouped by region.

---

## GNews country coverage

Supported country codes include: `au br ca cn eg fr de gr hk in ie il it jp mx nl no pk pe ph pt ro ru sg es se ch tw ua gb us tr ar za ng ke gh nz`.  
Some EU codes (e.g. CZ, SK, HU) may use language-only fetch — see repo `regional_challenges` country map in code.

---

## See also

- [[Challenges]]
- [[Database Reference]]
- [[Edge Functions]]
- [[Dashboards]]
- [[🏠 Home]]
