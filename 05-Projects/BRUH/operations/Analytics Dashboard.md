---
tags: [operations, analytics, dashboard, vercel, metrics]
area: operations
updated: 2026-04-14
---

# Analytics Dashboard

> [!note] **URL:** `analytics.bruhsocial.app` · **Code:** `dashboard/` · **Host:** Vercel (root dir `dashboard/`). Finance / growth metrics. Engineering ops live in [[Dashboards]] (`admin.bruhsocial.app`).

> [!tip] 2026-04 maintenance
> - Apr 4 Cursor pass: full **audit** of `dashboard/src` (routing, auth, RPCs, charts) + **connectivity** smoke vs Supabase.
> - When changing metrics: keep `dashboard/src/lib/queries.ts` aligned with SECURITY DEFINER RPCs and [[Edge Functions]] / [[Migrations Log]].

---

## Deployment

| Item | Value |
|------|--------|
| Repo | `Zsadigzade/BRUH` monorepo |
| DNS | CNAME `analytics` → `c8f692f5cc8b43e2.vercel-dns-017.com.` (Cloudflare DNS — Netlify removed Apr 2026) |
| Env | `dashboard/.env` — same `VITE_SUPABASE_URL` + anon key as main app |
| Headers | `dashboard/vercel.json` — nosniff, DENY frame, Referrer-Policy, Permissions-Policy |
| CI deploy | `.github/workflows/vercel-dashboard.yml` — run Vercel CLI from **repo root**; GitHub secrets **`VERCEL_DASHBOARD_PROJECT_ID`**, `VERCEL_TOKEN`, `VERCEL_ORG_ID` (see [[Deploy Targets]] · `scripts/INCIDENT_RUNBOOK.md`) |

---

## Stack

- Vite + React 18 + TS, TanStack Query v5, React Router v6
- Supabase Auth (email/password for **dashboard users** — separate from app custom auth)
- `dashboard/src/lib/queries.ts` — data fetchers (SECURITY DEFINER RPCs)
- `REFETCH_INTERVAL` = 5 min on data queries

---

## Access

- Table **`dashboard_users`** — pre-approved emails; user registers with exact email
- **`dashboard_auth_check()`** after login — links `auth_id`; returns `{ allowed }`
- **`is_dashboard_user()`** — works before `auth_id` linked (email join)

Add user (SQL): `INSERT INTO public.dashboard_users (email, name) VALUES (...);`

---

## Pages (8)

| Route | Page | Highlights |
|-------|------|------------|
| `/` | Executive Overview | Totals, DAU delta, premium, north star, D/W/M charts, alerts |
| `/product` | Product Analytics | DAU/WAU/MAU, funnel, cohorts |
| `/revenue` | Revenue & Finance | Subs, charts, links to Marketing for live RC/AdMob tiles |
| `/funnel` | Growth Funnel | Registered → post → reply → retained |
| `/marketing` | Marketing Intelligence | 5 external sources, Sync Now / Sync All |
| `/content` | Content Intelligence | Reply velocity, top memes/senders, All Time / 30d toggle |
| `/push` | Push & Notifications | Reach, platform split, opt-ins, counts by type |
| `/users` | Team Access | Invite/remove dashboard users, last login |

---

## RPCs (SECURITY DEFINER; dashboard or admin)

| RPC | Role |
|-----|------|
| `get_dashboard_overview_stats` | Hero + deltas |
| `get_dashboard_dau_series` | ~180d DAU + new users |
| `get_dashboard_growth_funnel` | Funnel + all-time |
| `get_dashboard_revenue_stats` | Subscription aggregates |
| `get_dashboard_content_stats` | Top senders/memes, series |
| `get_dashboard_push_stats` | Tokens, opt-ins, notifications by type |
| `get_marketing_stats(p_days)` | All 5 external cache tables |
| `list_dashboard_users` / `invite_dashboard_user` / `remove_dashboard_user` | Team |
| `dashboard_auth_check` | Gate after login |

Migrations: `20260329000001` … `000003` (see repo).

---

## External stats cache

Tables: `external_stats_admob`, `external_stats_appstore`, `external_stats_playstore`, `external_stats_revenuecat`, `external_stats_firebase` — RLS locked down; filled by `sync-*-stats` edge functions.

**Caller auth:** `supabase/functions/_shared/syncAuth.ts` — **`Bearer CRON_SECRET`** or JWT where caller is **`is_dashboard_user()`** or **`is_admin()`**. Dashboard **Sync** uses session token. **`verify_jwt = false`** on these functions in `config.toml`; auth inside code.

| Function | Upstream (secrets in Supabase only — never commit) |
|----------|-----------------------------------------------------|
| `sync-admob-stats` | Google OAuth / AdMob API |
| `sync-appstore-stats` | App Store Connect API (`.p8`, issuer, vendor) |
| `sync-playstore-stats` | Play Developer Reporting API (service account JSON) |
| `sync-revenuecat-stats` | Often **DB-only** MRR estimate; optional RC API |
| `sync-firebase-stats` | GA4 Data API (service account + property id) |

> [!warning] Store all integration secrets in **Supabase secrets** / password manager — **not** in this vault or git.

---

## Design

“Precision Brutalism”: neon accent `#c3f400`, Inter, flat surfaces, CSS bar charts (no chart lib).

---

## Mobile

Responsive grids, slide-in sidebar, stacked hero cards — see `dashboard/src/components/`.

---

## See also

- [[Dashboards]]
- [[Edge Functions]]
- [[Migrations Log]]
- [[12 - MCP & External APIs]]
- [[🏠 Home]]
