---
tags: [kb, ai, mcp, tooling]
area: knowledge-base
updated: 2026-04-14
---

# MCP server patterns

> [!tip] BRUH agents: you **may use MCP throughout a task** to validate assumptions — deploys, errors, analytics, DB, uptime. Policy + server map: [[Agent MCP — live verification]].

---

## When MCP vs direct API

| MCP | Direct script / dashboard |
|-----|---------------------------|
| **Interactive** agent session — live queries, **proactive verification** after edits | One-off bulk ops you automate locally |
| **Schema-aware** tools (Supabase, GitHub, Sentry, …) | Secrets you don’t want in agent context |

Project wiring: [[12 - MCP & External APIs]] · [[Agent MCP — live verification]].

---

## Tool design mental model

- **Small outputs** — paginate; avoid 10MB JSON in chat
- **Clear errors** — actionable message, not stack dumps to user

---

## Auth

- **shadcn registry MCP** — **no token**; stdio `npx shadcn@latest mcp`. Init: [[Cursor Tips & Power Features]] · [[12 - MCP & External APIs]].
- Store tokens in **MCP host** config — not in vault notes
- EU PostHog / regional endpoints — don’t assume `app.posthog.com`
- **Cursor + Windows:** some servers need a small **Node wrapper** (e.g. BRUH **`.cursor/servers/uptimerobot.mjs`**) so `--header "Authorization: Bearer …"` stays a **single argv** (avoid `cmd.exe` splitting) and so **`UPTIMEROBOT_API_KEY` is read from `.cursor/.env.mcp.local`** if the host passes a literal `${VAR}`. See [[12 - MCP & External APIs]].

---

## Composition

- Chain **read** tool → **reason** → **write** tool; confirm destructive ops

---

## Failure modes

- **Rate limits** — backoff; don’t hammer
- **Stale schema** — refresh migration list before assuming columns

---

## See also

- [[Secrets Management Guide]] · [[Cursor Tips & Power Features]]
