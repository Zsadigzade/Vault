---
tags: [kb, security, api, edge-functions]
area: knowledge-base
updated: 2026-04-04
---

# API security & rate limiting

---

## Edge Functions (Supabase / Deno)

| Control | How |
|---------|-----|
| **Auth** | Verify JWT or shared secret header; reject missing/invalid early |
| **Input** | Zod / schema validate JSON body & query params |
| **CORS** | Allowlist origins — avoid `*` with credentials |
| **Errors** | Generic message to client; log details server-side only |

See [[Edge Functions Patterns]] · project [[Edge Functions]].

---

## Rate limiting

| Layer | Options |
|-------|---------|
| **Edge** | In-memory (per isolate — limited), KV/Redis, or upstream API gateway |
| **Supabase** | Auth rate limits (built-in); custom limits in Edge |
| **Client** | UX debounce only — **not** security |

---

## Idempotency

- **Webhooks:** HMAC verify + idempotency key / dedupe table (e.g. RevenueCat pattern in project)
- **POST** that creates resources: accept `Idempotency-Key` for retries

Project: [[Payment Webhook Security]].

---

## SSRF & outbound calls

- Don’t let user supply **arbitrary URLs** for server fetch without allowlist
- Timeout + size limits on HTTP responses

---

## See also

- [[Secrets Management Guide]] · [[OWASP Mobile Top 10]] (M4, M5)
