---
tags: [kb, security, secrets, env]
area: knowledge-base
updated: 2026-04-04
---

# Secrets management guide

---

## Tiers

| Tier | Examples | Where |
|------|----------|--------|
| **Public client** | Supabase **anon** key, PostHog project key (often public) | Env at build / runtime config |
| **Private server** | `service_role`, webhook HMAC, API keys | Supabase **secrets**, Edge env, CI secrets |
| **Never in repo** | `.env.local`, MCP tokens, store credentials | Password manager, host dashboard |

---

## Files

| File | Git |
|------|-----|
| `.env.example` | **Yes** — dummy keys + comments |
| `.env` / `.env.local` | **No** — gitignore |
| `*.bat` with keys | Project rule: **gitignore** (use `.bat.example`) |

---

## Supabase

- **Dashboard → Project Settings → Secrets** for Edge Functions
- Rotate on employee offboarding or leak

---

## CI (Codemagic / GitHub Actions)

- Store signing certs, API keys as **encrypted** env
- **Never** echo secrets in logs

---

## Chat & agents

> [!warning] Do **not** paste secrets into Cursor chat or Obsidian notes. Use env references by **name** only.

---

## See also

- [[Supabase Security Hardening]] · [[API Security & Rate Limiting]] · [[12 - MCP & External APIs]]
