---
tags: [tools, mcp, api, cursor, external-services]
area: reference
updated: 2026-04-14
---

# MCP & External APIs

> [!success] **AI agents:** You are **expected** to use enabled MCP tools to **test, verify, and query** live services while working on BRUH — not only on explicit “check production” requests. Start here for wiring; permission + workflow: [[Agent MCP — live verification]].

---

## MCP Setup Location

| File | Purpose |
|------|---------|
| `.cursor/.env.mcp.local` | All API keys/tokens (gitignored) |
| `.cursor/mcp.json` | MCP server configuration |
| `.cursor/servers/*.mjs` | MCP server scripts (shared helper **`mcp-stdio.mjs`** + e.g. **`uptimerobot.mjs`**, **`posthog.mjs`**) |

Setup: `cd .cursor && npm install` to install server dependencies.

> [!note] Cursor may not auto-load `.env.mcp.local`. **`mcp-stdio.mjs`** merges that file **at import time** when `mcp.json` still passes literal `${VAR}`. **`uptimerobot.mjs`** also re-reads the file for `UPTIMEROBOT_API_KEY`. Restart Cursor after any `mcp.json` edits.

---

## MCP servers in repo `mcp.json`

| Key | Transport | Typical use |
|-----|-----------|-------------|
| `supabase` | stdio | DB/project/edge introspection (custom server) |
| `sentry` | stdio | Issues, releases (EU) |
| `revenucat` | stdio | Subscriptions / project |
| `capgo` | stdio | OTA bundles, channels |
| `codemagic` | stdio | CI apps |
| `posthog-local` | stdio | **PostHog EU** via REST + personal API key |
| `netlify` | stdio | Sites / deploys |
| `github` | stdio | `Zsadigzade/BRUH` |
| `appstore` | stdio | ASC (local `.p8`) |
| `googleplay` | stdio | Play JSON key path |
| `vercel` | stdio | Deployments / project |
| `resend` | stdio | Domains / account smoke |
| `uptimerobot` | stdio → hosted MCP | Monitors, incidents (`mcp-remote` + API key) |
| `shadcn` | stdio | **shadcn/ui registries** — list/browse/add components via MCP (`npx shadcn@latest mcp`). **No API key.** |

**shadcn MCP — Cursor init:** run from the app root (where `components.json` lives, if any):

```bash
npx shadcn@latest mcp init --client cursor
```

Merges a **`shadcn`** block into **`.cursor/mcp.json`**. Then **Cursor → Settings → MCP** — enable **shadcn** (green dot when healthy); **restart Cursor** after edits. Official doc: [ui.shadcn.com/docs/mcp](https://ui.shadcn.com/docs/mcp). UX prompts: *“List components in the shadcn registry”*, *“Add button and dialog”*. If **custom registries** in `components.json` misbehave with a **global** MCP config, prefer **project**-level `.cursor/mcp.json` or run MCP with **`--cwd`** pointed at the project (see shadcn CLI `mcp --help`).

Also use **Cursor-managed** MCPs when present (e.g. **user-supabase**, marketplace **Supabase** / **Vercel** plugins). Those may require a one-time **`mcp_auth`**.

---

## External Service Quick Reference

| Service | Base URL | Auth Method | Key/Notes |
|---------|----------|-------------|-----------|
| **Supabase** | `SUPABASE_URL` | anon key / service role | Project: `gpainqlxdakaczkgozko` |
| **Sentry** | `https://de.sentry.io/api/0` | `SENTRY_AUTH_TOKEN` | Org: `bruh-social`; **EU host** |
| **PostHog** | `https://eu.posthog.com` | `POSTHOG_API_KEY` | **EU** — MCP: **`posthog-local`** only in `mcp.json`; `app.posthog.com` → 401 with EU keys |
| **RevenueCat** | `REVENUCAT_API_BASE` | `sk_...` secret key | V1 API (V2 incompatible with secret key format) |
| **Capgo** | `https://api.capgo.app` | `CAPGO_API_KEY` | Raw key in `authorization` header — **no `Bearer` prefix** (Bearer → `invalid_apikey`) |
| **Codemagic** | `https://api.codemagic.io` | `x-auth-token: CODEMAGIC_API_TOKEN` | `/apps` endpoint (not root `/workflows`) |
| **GitHub** | `https://api.github.com` | `GITHUB_TOKEN` | Owner: `Zsadigzade`, Repo: `BRUH` |
| **Vercel** | Vercel API | `VERCEL_AUTH_TOKEN` | Two projects: `admin-web/` + `dashboard/` |
| **Resend** | Resend API | `re_...` key | Prod edge uses Supabase secrets |
| **Netlify** | `https://api.netlify.com` | `Authorization: Bearer <token>` | Token in `%APPDATA%\Netlify\Config\config.json` |
| **UptimeRobot** | Hosted MCP `https://mcp.uptimerobot.com/mcp` | Main or read-only API key | Env: `UPTIMEROBOT_API_KEY` in `.cursor/.env.mcp.local`; `mcp.json` → `node .cursor/servers/uptimerobot.mjs` |

---

## Critical API Quirks

### PostHog — EU Only (MCP = `posthog-local`)

```bash
# ✅ CORRECT — EU region (REST + MCP server)
POSTHOG_API_BASE=https://eu.posthog.com

# ❌ WRONG — returns 401 for EU-region keys
POSTHOG_API_BASE=https://app.posthog.com
```

Use MCP server **`posthog-local`** (stdio + API key). The remote URL `https://mcp-eu.posthog.com/mcp` was **removed** from BRUH `mcp.json` because Cursor often fails to expand `${POSTHOG_API_KEY}` in URL-MCP headers, causing repeated **`mcp_auth`** prompts. Avoid `npx @posthog/wizard` in agents — use manual setup.

### Capgo — Raw API Key (No Bearer)

```bash
# ✅ CORRECT
Authorization: <raw-api-key>

# ❌ WRONG — returns invalid_apikey
Authorization: Bearer <raw-api-key>
```

### Netlify DNS — CLI Is Broken

```bash
# ❌ WRONG — npx netlify api createDnsRecord always returns 422
npx netlify api createDnsRecord --data "{...}"

# ✅ CORRECT — use REST API directly
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"hostname":"full.hostname.bruhsocial.app","type":"TXT","value":"...","ttl":3600}' \
  "https://api.netlify.com/api/v1/dns_zones/699d83563a6094d223531b6a/dns_records"
```

**DNS Zone ID for `bruhsocial.app`**: `699d83563a6094d223531b6a`
Hostname must be the **full FQDN** (not just subdomain).

---

## Netlify Site IDs

| Site | ID | Domains |
|------|----|---------| 
| **bruhsocial** (primary) | `a41413fd-311e-41ef-aa0c-2947ef3d9497` | `bruhsocial.app` + `share.bruhsocial.app` alias |
| bruh-share (secondary) | `a8b4d69e-b8dc-46bd-bbe7-a6d28e0a7e31` | No custom domain — ignore |

Deploy command:

```bash
npx netlify deploy --site a41413fd-311e-41ef-aa0c-2947ef3d9497 --dir . --prod
```

---

## Agent Behavior Rules for Live Infra

1. **Use MCP tools first** for anything that touches **live** state (see [[Agent MCP — live verification]]).
2. If MCP is unavailable or insufficient: **targeted** curl/IWR with env loaded from `.cursor/.env.mcp.local`.
3. **Never** paste secrets in chat or commits.
4. Prefer **read** tools before **write**; confirm destructive ops with the human unless the task explicitly allows them.

---

## Smoke Test Results (2026-04-02)

All confirmed working:

- Supabase REST root
- Sentry issues list
- RevenueCat `/v2/projects`
- Capgo app GET (raw `authorization` key)
- Codemagic `/apps`
- PostHog EU `@me`
- GitHub `Zsadigzade/BRUH`
- Vercel projects
- Resend `/domains`

Skipped: Netlify (owner deploys manually)
File-only: App Store `.p8` + issuer, Play service JSON (not API-accessible)

---

## Agent Tools

| Tool | What it does | Detail |
|------|--------------|--------|
| **Caveman** | Token compression for all agents — cuts ~75% output tokens, full accuracy | [[caveman]] |

---

## See also

- [[Agent MCP — live verification]]
- [[Deploy Targets]]
- [[Security Reference]]
- [[🏠 Home]]
- [[caveman]]
