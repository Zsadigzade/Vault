---
tags: [kb, postgres, sql, supabase]
area: knowledge-base
updated: 2026-04-04
---

# Query patterns & anti-patterns

---

## N+1

| Bad | Better |
|-----|--------|
| Loop `select` per row | Single query with `IN` / join / RPC batch |

---

## Offset pagination

- `OFFSET` large values **slow** — prefer **keyset** ([[Feed & Infinite Scroll Patterns]])

---

## PostgREST embed + RLS

> [!warning] BRUH: **`replies(count)`**-style embeds can explode latency under RLS — use **RPC** ([[09 - Critical Gotchas]]).

---

## `SELECT *`

- Avoid in hot paths; fetch **needed columns** only (less I/O)

---

## Denormalization

- **Counters** maintained by triggers / background jobs vs counting rows every read

---

## Transactions

- Keep **short** — avoid holding locks while calling external APIs

---

## See also

- [[RLS Pattern Library]] · [[Edge Functions Patterns]]
