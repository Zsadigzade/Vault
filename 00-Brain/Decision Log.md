---
tags: [meta, decisions, history, rationale]
area: meta
updated: 2026-04-06
---

# Decision Log

> [!note] Non-obvious product and engineering decisions. For bug root-cause stories see [[Bug History & Lessons]].

---

## 2026-04 — Admin ops identity

| Decision | Rationale |
|----------|-----------|
| **`admin_users.console_auth_id`** + `is_admin` / `is_superadmin` accept **ops Supabase JWT** | Consumer app often stays on **anon** password-auth session; ops console uses a real OAuth/magic-link `auth.uid()`. RPCs must recognize admin rows by **console auth id** without trusting client-supplied user UUIDs. |

---

## 2026-04 — Security & webhooks

| Decision | Rationale |
|----------|-----------|
| **`get_my_user_id()` only** on inbox / post replies / sent / meme-rec / `fetch_my_posts` / moderator RPCs | Closes IDOR when client-supplied UUID was trusted. |
| **RevenueCat webhook:** optional HMAC; Authorization accepts raw or `Bearer`; non-UUID `app_user_id` → **200 skip** | Stops RC retry storms; aligns with real RC dashboard options. |
| **Push via PL/pgSQL + Vault**, not Dashboard Database Webhooks | Dashboard UI **truncated** webhook secret JSON → `22P02` + rolled back INSERTs. |
| **`is_admin()` no-arg** | Old `is_admin(uuid)` allowed **enumerating** admin UUIDs. |
| **`feature_flags` public read, RPC-only writes** | Consumer needs flags; writes gated (`super_admin` for killswitch names). |

---

## 2026-04 — App shell & performance

| Decision | Rationale |
|----------|-----------|
| **Index tabs stay mounted**; gate queries with `isActive` | Cuts background polling / work when user is on another tab. |
| **Premium check after `initRevenueCat()`** on startup | Avoids buy-button flash for subscribed users on native. |
| **`--kbd-h` + manual insets**; keyboard `resize: 'none'` | Body resize reflow broke layout; Android `adjustNothing`. |

---

## 2026-04 — Data lifecycle

| Decision | Rationale |
|----------|-----------|
| **`meme_analytics` at send time** | Reply row purge/scrub does **not** rewind trending counters. |
| **Scrub replies on post delete** (`[expired]` sentinel) + weekly purge | Retention + storage; pending **reports** block purge of that reply. |
| **`canvas.toDataURL`** for posting card, not `toBlob` | Android WebView release: `toBlob` callback latency killed share UX — see [[Share Card & Presave]]. |

---

## 2026-03 — Regional challenges

| Decision | Rationale |
|----------|-----------|
| **Cron body `triggered_by: "cron"`** → auto-activate AI challenges | Scheduled runs publish without admin gate; **admin** triggers stay `pending` for review. |
| **Region via Cloudflare `cf-ipcountry`** (edge `detect-region`) | No location permission; VPN caveat documented in [[Regional AI Challenges]]. |

---

## 2026-03 — Admin & analytics split

| Decision | Rationale |
|----------|-----------|
| **Ops admin** on Vercel `admin-web/` at `admin.bruhsocial.app` | Removes heavy admin bundle from consumer app; DNS CNAME from Netlify zone. |
| **Analytics** on Vercel `dashboard/` at `analytics.bruhsocial.app` | Finance/growth metrics separate from engineering ops. |

---

## Older (still binding)

| Decision | Rationale |
|----------|-----------|
| **Password auth → anon Supabase session + relink** | Custom auth model; RLS uses DEFINER RPCs + `get_my_user_id()`. |
| **Replies native-only** | Product constraint; `MemeReplyPicker` guards web → store CTA. |
| **Capgo `appId` = `com.bruh.app`** | Capacitor `appId` matches iOS bundle — Capgo API uses Android-style id for uploads. |

---

## See also

- [[Bug History & Lessons]]
- [[Migrations Log]]
- [[Security Reference]]
- [[🏠 Home]]
