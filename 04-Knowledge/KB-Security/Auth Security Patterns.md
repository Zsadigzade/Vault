---
tags: [kb, security, auth, jwt]
area: knowledge-base
updated: 2026-04-04
---

# Auth security patterns

---

## Sessions & tokens

| Practice | Detail |
|----------|--------|
| **Short-lived access** | Prefer refresh rotation where provider supports it |
| **Secure storage** | Native: Keychain/Keystore via secure plugins if storing refresh; avoid arbitrary secrets in `localStorage` |
| **Transport** | HTTPS only; no token in URL query strings (referrer leaks) |

---

## OAuth / magic link

- **State parameter** — CSRF protection for OAuth flows
- **Redirect URI allowlist** — exact match in provider + Supabase dashboard

---

## Custom password flows

If using **custom** session model (e.g. anon + RPC):

- **Never** duplicate identity checks only in UI — enforce in **RPC/RLS**
- Rate-limit **login** attempts (Edge Function or Supabase rate limits / WAF)

Project: [[Authentication]] — two auth paths; use **`getUserId()`** not `getUser()` for app identity per project rules.

---

## JWT claims

- Treat JWT as **assertion**, not authorization alone — **RLS** must align
- Validate **issuer**, **audience**, **exp** on server when verifying manually

---

## Logout

- Clear **client** session + **server** refresh if applicable
- Invalidate device tokens for push on account delete

---

## See also

- [[Supabase Security Hardening]] · [[Secure Storage on Mobile]] · [[API Security & Rate Limiting]]
