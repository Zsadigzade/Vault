---
tags: [meta, agent, mcp, cursor, verification]
area: meta
updated: 2026-04-06
---

# Agent MCP — live verification

> [!tip] **For every AI agent in Cursor (and similar hosts):** You **may and should** use **enabled MCP tools** to **read and verify live state** across the BRUH stack. Treat MCP as the default way to confirm production/API reality — not only when the human explicitly says “check Sentry.” Prefer tools over guessing from stale chat context.

**Canonical wiring + quirks:** [[12 - MCP & External APIs]] · repo `.cursor/mcp.json` · `.cursor/.env.mcp.local` (gitignored). **Claude memory index:** `.claude/projects/.../memory/MEMORY.md` → `cursor_mcp_and_service_access.md`. **Ops / uptime / incident table:** same folder **`ops_monitoring.md`** (do not duplicate long tables here).

---

## When to use MCP proactively

| Situation | Examples |
|-----------|----------|
| After code touching **backend / DB / edge** | Supabase: tables, migrations, logs, advisors; list/deploy edge functions |
| **Deploys, CI, OTA** | Vercel, Codemagic, Capgo bundles/channels, GitHub commits/PRs |
| **Incidents & “is it down?”** | UptimeRobot monitors, Sentry issues, PostHog events/insights, health-check URL (see runbook) |
| **Payments / subs** | RevenueCat project state (read-only checks) |
| **Email / domains** | Resend domain list (smoke) |
| **Stores** | App Store / Play MCP where keys are configured (often file-based) |

If a tool call fails (auth, rate limit), fall back to **targeted** curl/IWR with env loaded — **never** paste secrets into chat or commits.

---

## BRUH `mcp.json` servers (stdio / hosted)

Cursor may prefix display names (e.g. `project-0-BRUH-*`). Map by **configured name**:

| `mcp.json` name | Role |
|-----------------|------|
| `supabase` | Management-style DB/project tools via `.cursor/servers/supabase.mjs` |
| `sentry` | Issues, releases, stats (EU API base) |
| `revenucat` | RevenueCat API |
| `capgo` | OTA bundles, channels, stats |
| `codemagic` | CI apps/builds |
| `posthog-local` | **PostHog EU** REST via API key — use this (not a remote PostHog URL) |
| `netlify` | Sites/deploys (when token present) |
| `github` | Repo `Zsadigzade/BRUH` |
| `appstore` | App Store Connect (`.p8` path) |
| `googleplay` | Play Console JSON key path |
| `vercel` | Vercel project API |
| `resend` | Account/domains smoke |
| `uptimerobot` | Hosted MCP via `uptimerobot.mjs` + API key |

**Often also available:** Cursor **user-supabase** (dashboard-linked Supabase MCP) and **marketplace plugins** (e.g. Supabase, Vercel) — those may expose `mcp_auth` once; they complement the repo servers above.

---

## Rules

1. **Inspect MCP tool schemas** in the host’s MCP file tree when arguments are unclear.
2. **EU PostHog** — `https://eu.posthog.com` / **`posthog-local`** only for this project’s MCP; not `app.posthog.com` for private API.
3. **Capgo** — `authorization: <raw key>` (no `Bearer` prefix) for direct API; MCP server already does this.
4. **Destructive actions** — confirm with the human before mutating production (resolve Sentry issue, pause monitor, etc.) unless the task explicitly authorizes it.

---

## See also

- [[12 - MCP & External APIs]] · [[Agent Quick Reference]] · [[🏠 Home]]
- [[Incident Response & Debugging]] · repo `scripts/INCIDENT_RUNBOOK.md`
- [[MCP Server Patterns]] (KB) · [[SESSION_HANDOFF]]
