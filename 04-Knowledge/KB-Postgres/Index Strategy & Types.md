---
tags: [kb, postgres, indexes, performance]
area: knowledge-base
updated: 2026-04-04
---

# Index strategy & types

---

## B-tree (default)

- Equality and range on **scalar** columns — most common

---

## Composite indexes

- Order columns by **selectivity** + **query shape** (`WHERE a = ? AND b > ?` → `(a, b)`)
- **Left-prefix rule** — index `(a,b)` helps `WHERE a` but not lone `b`

---

## Partial indexes

```sql
CREATE INDEX ON posts (created_at) WHERE deleted_at IS NULL;
```

- Smaller, faster when query always filters same predicate

---

## GIN / GiST

- **JSONB**, **arrays**, **full text** — heavier write cost

---

## Covering indexes (`INCLUDE`)

- Avoid heap fetches for index-only scans when beneficial

---

## Maintenance

- **`REINDEX`** / **`VACUUM ANALYZE`** after bulk loads
- Watch **bloat** on high-churn tables

---

## See also

- [[Postgres Query Optimization]] · [[Query Patterns & Anti-Patterns]] · [[Database Reference]]
