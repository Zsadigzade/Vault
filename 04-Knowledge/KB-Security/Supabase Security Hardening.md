---
tags: [kb, security, supabase, rls]
area: knowledge-base
updated: 2026-04-04
---

# Supabase security hardening

> [!tip] BRUH-specific policies and names: [[Security Reference]] · [[Database Reference]].

---

## Row Level Security (RLS)

| Rule | Detail |
|------|--------|
| **Default deny** | Enable RLS on all user-facing tables; explicit `SELECT`/`INSERT`/`UPDATE`/`DELETE` policies |
| **Never trust client** | All reads/writes go through policies or `SECURITY DEFINER` RPCs with explicit checks |
| **Service role** | Edge Functions / server only — **never** in app bundle |

---

## Auth configuration

- Enable **leaked password protection** (Have I Been Pwned) in dashboard (see `CLAUDE.md`)
- Review **redirect URLs** and **site URL** for OAuth / magic link
- **MFA** for admin accounts where possible

---

## API keys

| Key | Exposure |
|-----|----------|
| **anon** | Public — OK in client with RLS |
| **service_role** | **Secret** — server/Edge only |

Rotate on leak; use **Supabase Vault** / env for function secrets.

---

## Postgres hardening

- **Least privilege** DB roles for migrations vs runtime
- **Extensions** — only install what you need
- **Audit** sensitive tables (triggers or external audit log)

---

## Realtime

- Channels must respect **RLS**-backed authorization — verify who can subscribe

See [[Realtime & Subscriptions]].

---

## Backups & PITR

- Enable **PITR** / backups per compliance needs; test restore periodically

---

## See also

- [[RLS Pattern Library]] · [[Edge Functions Patterns]] · [[Secrets Management Guide]]
- [[Auth Security Patterns]] · [[OWASP Mobile Top 10]]
