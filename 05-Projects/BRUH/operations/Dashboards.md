---
tags: [operations, admin, dashboards, vercel]
area: operations
updated: 2026-04-14
---

# Dashboards — Ops Admin

> [!tip] **Finance / growth metrics:** [[Analytics Dashboard]] (`analytics.bruhsocial.app`). This note is **only** the engineering ops console.

---

## URL & stack

| Item | Value |
|------|--------|
| **Production** | `https://admin.bruhsocial.app` |
| **Code** | `admin-web/` (Vite) |
| **Host** | Vercel — GitHub `Zsadigzade/BRUH`, root **`admin-web`** |
| **Security headers** | `admin-web/vercel.json` — **HSTS** + **CSP** (2026-04 hardening) |
| **DNS** | Cloudflare DNS: **`admin`** CNAME → `a191df88897774c3.vercel-dns-017.com.` (Netlify fully removed Apr 2026) |
| **Local** | `npm run dev:admin` from monorepo root |
| **Consumer app** | **No** `/admin` — redirects home; admin UI **not** in PWA/APK |

---

## Access

- **`AdminGuard`** / **`AdminDashboard`:** `["admin-status"]` — **`staleTime: 0`**, **`refetchOnMount: true`** (revoked admins blocked immediately).
- **DB:** **`is_admin()`** no-arg — see [[Security Reference]].
- **Login:** `admin-web` → `/login` (**OpsLogin** — password + `is_admin` check).

### Ops JWT vs in-app `users.auth_id` (`console_auth_id`)

Password-auth users keep an **anonymous** Supabase session in the consumer app; their real row lives under `users` + `bruh_user_id`. **Ops sign-in** on `admin.bruhsocial.app` uses a normal Supabase session (e.g. Gmail OAuth) for dashboard API calls.

Migration **`20260412120000_admin_console_auth_id.sql`** adds **`admin_users.console_auth_id`** (nullable). **`is_admin` / `is_superadmin` RPCs** accept the session when **`auth.uid()`** matches either **`users.auth_id`** (legacy) **or** **`admin_users.console_auth_id`** (ops JWT). Super-admin checks in admin-web must use the identity that matches this column (see repo history: `isSuperAdmin` vs `console_auth_id`).

Detail: [[Security Reference]] · [[Authentication]] · [[Decision Log]].

---

## Tabs (19)

| key | Component | Notes |
|-----|-----------|--------|
| `overview` | AdminOverview | Stats, **command center** (incident flags snapshot incl. **`challenge_auto_generation`**, synthetic **`health-check`** GET, **ops links**), Capgo strip, **Check OTA**, quick actions; **Resolve all errors (N)** when unresolved > 0; **refetch 30s** |
| `reports` | AdminReports | Pending reports; mobile stacked cards |
| `users` | AdminUsers | Search, ban, **grant premium**, **AdminLastUpdated** |
| `contact` | AdminContact | In-app + website; reply; delete resolved; bulk delete resolved |
| `errors` | ErrorLogViewer | **Realtime** `error_logs` INSERT; **Tailwind + `admin/ui`** (2026-04); mobile-friendly filters + detail panel; **Mark all resolved** + **Resolve selected** (multi-select); **⌘/Ctrl+Shift+R** = bulk resolve (confirm) |
| `health` | AdminSystemHealth | Trends + **realtime** `error_logs` + `email_queue`; **60s** fallback; **Tailwind + `admin/ui` primitives** (2026-04) |
| `email` | AdminEmailQueue | Queue + retry |
| `ratings` | AdminRatings | Stars / text |
| `analytics` | AdminUserAnalytics | DAU/WAU/MAU (ops slice — not the CEO dashboard) |
| `content` | AdminContentPerformance | Top memes/senders — RPC |
| `stickers` | AdminStickerPackManager | CRUD packs |
| `flags` | AdminFeatureFlags | RPC toggles; **super_admin** → killswitch + **Force OTA** ([[Capgo OTA]]) |
| `export` | AdminBatchExport | CSV |
| `challenges` | AdminChallenges | Global + [[Regional AI Challenges]] monitor; **Tailwind/mobile** (2026-04); **Cron auto-generation** toggle (`challenge_auto_generation` flag) at top of regional panel |
| `questions` | AdminQuestionBank | `challenge_questions` |
| `announcements` | AdminAnnouncements | Broadcasts |
| `fraud` | FraudSignalsTab | Fraud signals |
| `audit` | SubscriptionAuditTab | Subscription audit log |
| `admins` | AdminAdminList | Roles; **super_admin** DB-protected |

---

## Navigation & refresh

- **URL hash:** `#overview`, `#reports`, … — `replaceState` + `hashchange` sync.
- **Header Refresh:** calls **`invalidateAdminTabQueries(queryClient, activeTab)`** plus **`["admin-badges"]`** — refetches the current tab’s queries and sidebar badges (**no** full page reload). **Overview** and **Challenges** refreshes also invalidate **`["challenge-auto-generation-flag"]`** so the regional cron toggle stays current.
- **Header breadcrumb:** uppercase **section label** (nav group, e.g. *App monitoring*) above the active tab title — helps wayfinding when the sidebar is collapsed on mobile.
- **Sidebar:** **Filter** input (label + description match); **⌘K / Ctrl+K** focuses the filter. Browser **Ctrl/Cmd+R** remains a normal full reload (not hijacked).
- **Shared UI:** `AdminLastUpdated` on Overview, Users, Admins, Sticker packs.
- **Primitives (2026-04):** `src/components/screens/admin/ui/` — **`AdminPanel`**, **`AdminStatGrid`**, **`AdminStatCard`** (theme tokens).
- **Ops helpers:** `src/lib/adminOpsLinks.ts` (external incident links); `src/lib/adminHealthCheck.ts` (public GET `…/functions/v1/health-check`).
- **Tests:** `src/test/adminDashboardRefresh.test.ts` — `parseAdminTabFromHash`.

---

## Realtime & polling

- **Publication:** migration `20260409120000_*` — `error_logs`, `email_queue` on **`supabase_realtime`** if missing.
- **Badges query `["admin-badges"]`:** **15s** `refetchInterval` + window focus.
- **Overview `["admin-overview"]`:** **30s** refresh.
- **Overview ops widgets:** `["admin-ops-flags-snapshot"]` (**30s** interval); `["admin-ops-health-check"]` (**60s** + manual **Probe**). Invalidated with overview when using header **Refresh**.

---

## Feature flags (wired)

| Flag | Effect |
|------|--------|
| `registration_open` | Gate registration UI |
| `maintenance_mode` | Banner + pauses heavy queries / create+reply ([[App Architecture]] / `SystemFlagsContext`) |
| `app_killswitch` | Full-screen overlay; **`media-proxy` 503** with emergency lock |
| `emergency_api_lock` | Same **503** path on **`media-proxy`** |
| `challenge_auto_generation` | When **disabled**, pg_cron job **`generate-regional-challenges`** still runs but **skips** `net.http_post` to the edge fn; **manual** admin triggers unchanged ([[Regional AI Challenges]]) |

`getFeatureFlag` — 5‑min cache **except** killswitch / maintenance / emergency (always refetch).

---

## Contact cleanup

- Resolved rows: single **Delete** + **Delete all resolved (N)** with confirm.
- **pg_cron:** `cleanup_old_resolved_contact_submissions` — resolved **>30 days** removed.

---

## Quick task index

| Task | Tab |
|------|-----|
| Ban user | Users |
| Feature flag | Flags |
| Force OTA | Flags / Overview |
| Errors | Errors |
| Support reply | Contact |
| Grant premium | Users |
| Regional AI | Challenges |
| Broadcast | Announcements |

---

## See also

- [[Analytics Dashboard]]
- [[Capgo OTA]]
- [[Edge Functions]]
- [[Database Reference]]
- [[12 - MCP & External APIs]]
- [[🏠 Home]]
