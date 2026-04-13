---
tags: [features, capgo, ota, deployment]
area: features
updated: 2026-04-07
---

# Capgo OTA

> [!note] Capgo ships **JS/CSS/HTML** OTA; native binary changes still need store builds.

---

## IDs & dashboard

| Key | Value |
|-----|-------|
| **Capgo / CLI app id** | `com.bruh.app` (`app.bruhsocial.app` is **wrong** for Capgo API) |
| **Capacitor root `appId`** | `app.bruhsocial.app` (iOS) — see `capacitor.config.ts` |
| **Dashboard** | https://web.capgo.app |

---

## Auth & CLI

- REST/CLI: **`authorization: <raw API key>`** — **no** `Bearer` prefix (Bearer → `invalid_apikey`).
- **`bundle upload`:** use **`--ignore-metadata-check`** when local `node_modules` differs from channel baseline after Capacitor/plugin upgrades (OK for JS-only OTA if store binary already matches).

---

## App wiring

- Package: `@capgo/capacitor-updater`
- `src/main.tsx`: `CapacitorUpdater.notifyAppReady()` with `.catch()` so plugin errors don’t derail boot.
- `capacitor.config.ts`: `plugins.CapacitorUpdater.appId` = `com.bruh.app`; `autoUpdate: true`; **`appReadyTimeout: 45000`** (avoid default 10s rollback on slow devices).
- Entry: `splash-failsafe.ts` loads before heavy bundle — see [[Startup Sequence & Storage Keys]] / [[Bug History & Lessons]] (Capgo stuck splash).

---

## Capgo API paths (source of truth)

Per [Cap-go/capgo](https://github.com/Cap-go/capgo) `supabase/functions/_backend/public/bundle/index.ts` and `channel/index.ts`:

| Resource | Method | Path |
|----------|--------|------|
| Bundle list | GET | `/bundle/` |
| Bundle by version | GET | `/bundle/:version` |
| Channel list | GET | `/channel/` |
| Channel by id | GET | `/channel/:id` |
| Update channel | PUT | `/channel` (body) |

**`capgo-proxy`** uses **`CAPGO_API_BASE`** (default `https://api.capgo.app`) + these paths. Do **not** assume `/api/...` unless the base URL already includes it.

### Response shapes (edge proxy must handle all)

Live Capgo responses are **not** consistently `{ data: T }`:

- **`GET /channel/?channel=production`** — may return a **single channel object** at the top level, or an **array** of channels, or `{ data: … }` (array or object).
- **`GET /bundle/`** — often a **top-level array** of bundle rows; may also be wrapped in `{ data: … }`.

**`capgo-proxy`** normalizes with **`channelRowsFromBody`** / **`bundleRowsFromCapgoBody`**: accept array, `{ data: array|object }`, or a lone channel object. **`bundleVersionFromRow`** supports `version` as string or **one-element array** (Capgo quirk). Sort bundles by **`created_at` / `createdAt`** descending; respect **`is_deleted` / `isDeleted`**.

**Admin (2026-04):** **Overview** = **Channel pinned** (from channel) vs **Latest upload** (from bundle list) + drift/sync badges; **Refresh Capgo** refetches both. **Feature flags** = **Force OTA** dropdown from latest uploads + fallback to dashboard `__APP_VERSION__`. **Vercel CI:** if the Vercel project **Root Directory** is `admin-web`, run `vercel pull` / `vercel build` / `vercel deploy` from the **repo root** only — do not set GitHub Actions `working-directory: admin-web` or the CLI resolves `admin-web/admin-web` and fails.

---

## Force OTA (ops admin)

- Edge fn: **`capgo-proxy`** — caller sends **Supabase user JWT** `Authorization: Bearer <access_token>`; function verifies **`is_admin()`**, then POSTs Capgo `https://api.capgo.app/channel/` with `version` (bundle semver), `app_id: com.bruh.app`, `channel: production`, `disableAutoUpdateUnderNative: true`.
- **Supabase → Capgo:** secret **`CAPGO_API_KEY`** as **raw** `authorization` to Capgo (not Bearer).
- **`supabase/config.toml`:** `[functions.capgo-proxy] verify_jwt = false` so gateway doesn’t 401 before in-function admin check.
- UI: [[Dashboards]] → Flags / Overview (Check OTA / Force OTA — see `admin-web`). **`get-bundles`** / **`get-channel`** actions power pinned vs latest + Force OTA version list.

---

## Windows scripts (not in git)

- **`*.bat`** gitignored except `android/gradlew.bat`. Templates: **`capgo-push.bat.example`**, **`installation.bat.example`**, **`scripts/load-local-api-env.bat`**.
- **`CAPGO_API_KEY`:** `.cursor/.env.mcp.local` or `secrets.local.env` at repo root.
- **`capgo-push.bat`:** runs **`node scripts/bump-package-version.mjs`** (bumps **`package.json`** + syncs **`package-lock.json`** via `npm install --package-lock-only`) → **`npm run build`** → Capgo **`bundle upload`** — **does not** `git commit` / `push` (user commits when ready). **Copy from `capgo-push.bat.example` when the local `.bat` drifts.**
- **`installation.bat`:** next bundle version = **`node scripts/bruhSemver.mjs --from <latest Capgo name>`** after reading latest from Capgo API (same rollover rule).

### BRUH semver (patch 0–99)

Third segment is **not** unbounded: **`1.0.99` → `1.1.0`**, not **`1.0.100`** or **`1.0.101`**. Implemented in **`scripts/bruhSemver.mjs`** (`nextBrhVersion`); **`npm run version:bump`** runs **`scripts/bump-package-version.mjs`**. **`bump-package-version.mjs`** must keep **`npm install --package-lock-only`** from writing to **stdout** (use **`stdio: ['ignore','ignore','inherit']`**) so Windows **`for /f in ('node …')`** in the bat file captures **only** the final version line. Read **`package.json` `version`** with **Node** in the bat — **not** `findstr` + `for /f` (breaks on semver dots).

> [!danger] **Stale local `capgo-push.bat` anti-pattern** — Never use batch arithmetic **`set /a PATCH=…+1`** for the next version; from **`1.0.100`** that yields **`1.0.101`**. Always delegate to **`bump-package-version.mjs`**.

CLI: `node scripts/bruhSemver.mjs --from X.Y.Z` prints next version only. Repo **`CLAUDE.md`** documents the rule.

---

## Version sync rule

> [!warning] **Never** upload to Capgo without bumping `package.json` first.  
> `__APP_VERSION__` comes from package version at build time; mismatch confuses admin OTA UI.

---

## See also

- [[Deploy Targets]]
- [[Commands & Scripts]]
- [[Dashboards]]
- [[Edge Functions]]
- [[🏠 Home]]

## Capgo Patterns — 2026-04-13

- **Full OTA journey tracking** — checks, downloads, installs, policy blocks, rollbacks all logged; debug in seconds
- **Delta updates** — only JS/HTML/CSS diffs sent; reduces update payload size significantly
- **`notifyAppReady()`** — call after app initialization; tells Capgo SDK app is stable (prevents rollback)
- Source: [Capgo live updates docs](https://capgo.app/docs/live-updates/), [capacitor-updater GitHub](https://github.com/Cap-go/capacitor-updater)
