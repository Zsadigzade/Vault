---
tags: [kb, performance, postgres, sql]
area: knowledge-base
updated: 2026-04-04
---

# Postgres query optimization

---

## EXPLAIN

- **`EXPLAIN (ANALYZE, BUFFERS)`** on slow queries in staging
- Watch **seq scans** on large tables, **nested loops** with huge rows

---

## Indexes

- See [[Index Strategy & Types]]
- **Partial** indexes for hot subsets (`WHERE status = 'active'`)

---

## N+1

- **Join** or **batch RPC** instead of per-row client queries — project rule: avoid PostgREST embed that triggers RLS per row ([[09 - Critical Gotchas]])

---

## Pagination

- **Keyset** (`WHERE id < $cursor ORDER BY id DESC LIMIT n`) beats `OFFSET` at depth

---

## RPC vs direct table

- Complex aggregations — `SECURITY DEFINER` RPC with fixed query plan can beat ad-hoc client filters

---

## See also

- [[Query Patterns & Anti-Patterns]] · [[RLS Pattern Library]] · [[Database Reference]]
