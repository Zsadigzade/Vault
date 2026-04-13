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

## Supabase Realtime Updates — 2026-04-13

- **Log Drains** (Pro tier) — stream Postgres/Auth/Storage/Edge/Realtime logs to Datadog, Grafana Loki, Sentry, Axiom, S3
- **Broadcast** — send messages to connected clients without DB persistence; lowest latency
- **Presence** — track online users per channel; shared state across clients
- **Postgres Changes** — listen to INSERT/UPDATE/DELETE via websockets; note: RLS applies per-row
- Source: [Supabase changelog](https://supabase.com/changelog), [Realtime docs](https://supabase.com/docs/guides/realtime)
