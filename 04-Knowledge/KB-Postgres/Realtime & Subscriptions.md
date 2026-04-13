---
tags: [kb, supabase, realtime]
area: knowledge-base
updated: 2026-04-04
---

# Realtime & subscriptions

---

## When realtime helps

| Good fit | Poor fit |
|----------|----------|
| Notifications, live counters (careful) | High-frequency firehose per row under RLS |
| Presence / typing | Bulk analytics |

---

## Channels

- **Topic design** — `room:123` not global `public:all`

---

## Authorization

- **RLS** still applies — verify who may subscribe
- Don’t leak **private** data via broadcast payloads

---

## Scaling

- **Debounce** client updates; **batch** server events
- Consider **polling** fallback for low-priority data

---

## Postgres changes

- **`realtime.broadcast`** patterns vs direct table replication — know tradeoffs

---

## See also

- [[Supabase Security Hardening]] · [[Query Patterns & Anti-Patterns]]
