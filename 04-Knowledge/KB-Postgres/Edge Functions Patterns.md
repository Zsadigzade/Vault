---
tags: [kb, supabase, edge-functions, deno]
area: knowledge-base
updated: 2026-04-04
---

# Edge Functions patterns

> [!tip] Project catalog: [[Edge Functions]].

---

## Request lifecycle

1. **CORS preflight** — handle `OPTIONS` early
2. **Auth** — verify JWT / secret
3. **Validate** body — Zod
4. **Work** — short timeout mindset
5. **Response** — consistent JSON envelope

---

## Secrets

- `Deno.env.get` — set via Supabase **secrets** — [[Secrets Management Guide]]

---

## Error shape

```ts
return new Response(JSON.stringify({ error: "message" }), { status: 400, headers: { "content-type": "application/json" } });
```

---

## Idempotency

- Webhooks: **verify signature** + **dedupe** table — [[API Security & Rate Limiting]]

---

## Cold starts

- Keep imports **lean**; lazy init heavy clients if needed

---

## Logging

- **Structured** JSON logs; **no PII** — [[OWASP Mobile Top 10]] (M6)

---

## See also

- [[Realtime & Subscriptions]] · [[Migration Best Practices]]
