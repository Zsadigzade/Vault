---
tags: [meta, vault-updates, archive, agent:minimal]
area: meta
updated: 2026-04-13
---

# Vault history — archived changelogs

> **Agents:** **Skip** unless user asks “when did we…” or tracing vault evolution. **Current** maintenance digest → [[Vault Updates Summary]] (recent blocks only).

---

## 2026-04-07 — Ziya Web portfolio (vault sync)

| Topic | Notes |
|-------|--------|
| **`14 - Personal & Other Projects/`** | **New** folder for repos outside BRUH |
| [[Ziya Web — Portfolio]] | **New** — `Ziya_Web` on Desktop, GitHub `Zsadigzade/Ziya_Web`, live **zsadigzade.com**, Vercel + GoDaddy DNS, stack, env vars, `SHOW_ABOUT_PHOTO`, UX decisions |
| [[14 - Personal & Other Projects/README]] | Folder index table |
| [[SITEMAP]] | Row for `14 - Personal & Other Projects/` |
| [[🏠 Home]] | **Other web properties** table + note index row for Ziya Web |
| [[Agent Quick Reference]] | **When to read what** row + **File map** row for `Ziya_Web` |
| [[SESSION_HANDOFF]] | **See also** — pointer to [[Ziya Web — Portfolio]] |

---

## 2026-04-07 — Agentic AI routing optimization

| Topic | Notes |
|-------|--------|
| [[BRUH_HOME]] | New vault-root ASCII alias → canonical [[🏠 Home]] (grep / `@`-friendly) |
| [[AGENT_READ_ORDER]] | New meta note: session read order + explicit skip list (token discipline) |
| [[🏠 Home]] | Agent entry rows for [[BRUH_HOME]] + [[AGENT_READ_ORDER]]; note index line no longer uses a stale fixed count |
| [[SITEMAP]] | Row for `BRUH_HOME.md`; `00 - Meta/` row mentions [[AGENT_READ_ORDER]] |
| [[Agent Quick Reference]] | Tip mentions [[BRUH_HOME]] + [[AGENT_READ_ORDER]]; callout to skip to **When to read what** if Home already read |
| Repo `.cursor/rules` | `bruh-project-memory.mdc` — alternate hub path `BRUH_HOME.md` |

---

## 2026-04-07 — Repo deps / tooling refresh (vault sync)

| Topic | Notes |
|-------|--------|
| [[SESSION_HANDOFF]] | Pulse bullet: moderate **npm-check-updates** workflow, **dashboard/** Vite 8, dropped **@types/dompurify**, ESLint **ignores** (**android/**, **supabase/functions/**), **`isAdMobTestMode`**, **patch-package** + **`npx cap sync`** reminder, **update-all-packages.bat.example** |
| [[Commands & Scripts]] | New section **npm: dependency updates (moderate)** |
| [[🏠 Home]] | Cheatsheet line for **`npx npm-check-updates --target minor -u`** |
| Repo | Already applied in **Zsadigzade/BRUH** (lockfiles + lint/build fixes) |

---

## 2026-04-06 — Chat UI polish (vault sync)

| Topic | Notes |
|-------|--------|
| [[Chat System]] | Client table: **`chatUi.ts`** + design note (alignment with settings shell — blur headers, gradient tiles, card rows) |
| [[SESSION_HANDOFF]] | Semver **`1.0.96`**; pulse bullet for **`chatUi.ts`** + touched components (`ChatList`, `ChatThread`, `ChatHeader`, `ChatInput`, `ChatBubble`, menu, typing) |
| [[🏠 Home]] | Shipped semver **`1.0.96`** |
| [[App Architecture]] | Key files row for **`chatUi.ts`** |
| Repo | Visual-only; no DB/API contract changes |

---

## 2026-04-06 — 3-tab shell + settings subpages (vault sync)

| Topic | Notes |
|-------|--------|
| [[App Architecture]] | **3 tabs:** Chat (0) · Create (1, default) · Profile (2); **`ProfileTab`** + **`RepliesInbox`**; **`/settings`** route; **`/inbox`** → Profile; nav badges (chat unread / profile replies) |
| [[SESSION_HANDOFF]] | Semver **`1.0.95`**; pulse bullets for shell, **`SettingsSubpageShell`**, tour `data-tour` keys |
| [[🏠 Home]] | Shipped semver **`1.0.95`** |
| Repo | `SettingsSubpageShell.tsx` + shared list classes; hub/subpage design alignment |

---

## 2026-04-06 — Chat performance + vault split (vault sync)

| Topic | Notes |
|-------|--------|
| [[Chat System — Performance]] | **New** — migration `20260417120000`, client realtime/cache/debounce table, regression risks |
| [[Chat System]] | Slimmed; points to performance note |
| [[Migrations Log]] | New row + “latest” = performance migration |
| [[Database Reference]] | Chat section lists third migration |
| [[SESSION_HANDOFF]] | **Short pulse**; extended history → [[SESSION_HANDOFF — Extended 2026-04]] |
| [[🏠 Home]] · [[Agent Quick Reference]] | Semver `1.0.92`; links to performance + extended handoff |

---

## 2026-04-06 — Chat v2 (DB + client) (vault sync)

| Topic | Notes |
|-------|--------|
| [[Chat System]] | Migration **`20260416180000`**: reactions, reply threading, soft-delete, leave conv, **You:** preview; client FAB, new-msg divider, context menu, optimistic send, typing presence, list swipe mute/leave |
| [[Migrations Log]] · [[Database Reference]] | New row + RPC table updates |
| [[SESSION_HANDOFF]] | Current objective + last-known chat bullets |

---

## 2026-04-06 — Chat native UI + keyboard + profile version (vault sync)

| Topic | Notes |
|-------|--------|
| [[Chat System]] | Client table: fixed composer + `--kbd-h`, `GifPreviewModal`, grouping, safe areas, semver footnote in **Settings** only |
| [[Keyboard & Layout]] | **ChatThread exception** — fixed `bottom: var(--kbd-h)` vs `100dvh` + root padding double-offset; scroller `pb` for bar height |
| [[SESSION_HANDOFF]] | Premium refresh without cache flash on resume; removed global build overlay; profile shows semver only |
| Repo | `AppBuildLabel` removed; `useAppVersionDetails.ts` → `getBuildSemver()` only |

---

## 2026-04-06 — Chat system (vault sync)

| Topic | Notes |
|-------|--------|
| [[Chat System]] | **New** — schema, RPCs, client map, push + prefs |
| [[Database Reference]] · [[Migrations Log]] · [[Edge Functions]] · [[Push Notifications]] · [[Reply System]] · [[App Architecture]] · [[Deep Links & PWA]] · [[Monetization]] · [[SESSION_HANDOFF]] · [[🏠 Home]] | Cross-links + migration `20260415120000` |

---

## 2026-04-06 — AdMob docs + reply/browse UX (vault sync)

| Topic | Notes |
|-------|--------|
| [[Monetization]] | Pre-publish **test ad IDs** (`DEV` / `VITE_ADMOB_USE_TEST_IDS` / device list); placement table: **GifBrowserSheet** GIF grids + sticker ads; **NativeAdSlot** iOS-only in React (Android fallbacks) |
| [[Personal Media & GIFs]] | Sheet: inline ad summary; **MemeReplyPicker My Own** parity with sheet |
| [[Reply System]] | MemeReplyPicker vs **GifBrowserSheet** flow corrected; ad frequencies → ~13% / wide rows |
| [[SESSION_HANDOFF]] | Bullet: AdMob test mode + grid ads + My Own redesign |

---

## 2026-04-06 — Agent MCP (live verification)

| Topic | Notes |
|-------|--------|
| [[Agent MCP — live verification]] | **New** — agents **should use MCP tools proactively** to verify live BRUH services; server map + rules |
| [[12 - MCP & External APIs]] | Agent callout, `mcp.json` table, PostHog **`posthog-local`**, expanded agent behavior |
| Cross-links | [[🏠 Home]] · [[Agent Quick Reference]] · [[📚 Knowledge Base]] (KB 05) · [[MCP Server Patterns]] · [[Incident Response & Debugging]] · [[SESSION_HANDOFF]]; repo `.cursor/rules/bruh-project-memory.mdc`; Claude `memory/` |

---

## 2026-04-06 — Agentic cleanup

| Topic | Notes |
|-------|--------|
| Cursor Plan exports | Moved **36** `.plan.md` + index → `[ARCHIVE]/Cursor Plans/` (later **whole `[ARCHIVE]/` deleted** 2026-04-13 — [[09 - Cursor Plans/README]]) |
| Dedup | [[🏠 Home]] keeps canonical commands + never-break summary; [[Agent Quick Reference]] links instead of repeating rules/commands |
| [[Critical Gotchas]] | Shorter pre-code checklist |
| [[Coding Patterns & Preferences]] | User prefs table removed — canonical [[User Preferences & Style]] |
| [[App Architecture]] | Native back: `shellBackCoordinator` (repo), not plan-only link |
| Counts / version | Edge fns **26**; Vitest **~155**; `package.json` **1.0.75** — align across hub + repo docs |
| Claude memory | `architecture` / `security` / `database` trimmed → vault canonical + deltas |
| New ops docs | Admin `console_auth_id`, GitHub `vercel-*.yml`, TS `baseUrl` deprecation note — [[Dashboards]], [[Deploy Targets]], [[VERSION_TRUTH_TABLE]] |

---

## 2026-04-05 — Vault sync (ops / MCP / Sentry)

| Topic | Notes |
|-------|--------|
| Create / inbox / tsconfig | Repo: Next idea removed; Challenges in `CreateScreen` card footer; `GifBrowserSheet` **`z-[60]`** over BottomNav; invalid `ignoreDeprecations` removed from `tsconfig.app.json` — [[Personal Media & GIFs]] · [[App Architecture]] · [[SESSION_HANDOFF]] |
| PostDetail + inbox UX | Card/grid toggle in **filter row** (was tiny header control). Removed **Hide this meme**, **Safety → Hidden GIFs**, `media.ts`, related i18n/tour; inbox badge = **`reply_count`** only. **`hidden_memes`** DB table unused by client — [[Reply System]] · [[SESSION_HANDOFF]] · [[13 - Tombstones & Anti-Patterns]] |
| Create keyboard | **`useKeyboardHeight` dropped from CreateScreen** only — static layout while typing; App/Index **`--kbd-h`** + BottomNav behavior unchanged — [[Keyboard & Layout]] · [[SESSION_HANDOFF]] |

Cross-note updates from **late Apr 5** Cursor work (incident prep, UptimeRobot MCP, Sentry alert deferral):

| Topic | Vault notes touched |
|-------|---------------------|
| Incident runbook, health-check URL, emergency flags | [[SESSION_HANDOFF]] · [[Incident Response & Debugging]] · [[Launch Checklist]] |
| `health-check` edge fn, `emergency-set-mode` + `maintenance_mode`, count **26** fns | [[Edge Functions]] · [[Project Overview]] |
| GitHub **`vercel-dashboard.yml`**, repo-root CLI, `VERCEL_DASHBOARD_PROJECT_ID` | [[Deploy Targets]] |
| Codemagic Android **`PACKAGE_NAME`** = `com.bruh.app` | [[Codemagic CI]] |
| UptimeRobot hosted MCP, `.cursor/servers/uptimerobot.mjs`, env fallback | [[12 - MCP & External APIs]] · [[SESSION_HANDOFF]] |
| Sentry alerts **deferred** until paid plan; bootstrap script + runbook in repo | [[Sentry]] · [[Launch Checklist]] · [[Incident Response & Debugging]] |
| Rotated third-party keys → never vault; update `.env.mcp.local` only | [[Security Reference]] |
| Agent “where is the runbook?” | [[Agent Quick Reference]] |
| KB: MCP Windows / env | [[MCP Server Patterns]] |
| KB: monitoring + Sentry deferral + health URL | [[Monitoring & Alerting Playbook]] |
| Analytics CI deploy row | [[Analytics Dashboard]] |
| Admin-web HSTS + CSP | [[Dashboards]] |
| Hub date | [[🏠 Home]] |
| Claude `memory/` token diet | **`ops_monitoring.md`**; **`MEMORY.md`** + **`sentry.md`** shortened |

---

## See also

- [[Vault Updates Summary]] · [[🏠 Home]] · [[Agent Quick Reference]]
