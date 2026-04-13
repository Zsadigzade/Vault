---
tags: [kb, postgres, migrations, supabase]
area: knowledge-base
updated: 2026-04-04
---

# Migration best practices

> [!tip] BRUH: `npx supabase db push` — [[Migrations Log]] · infra rules in repo.

---

## Idempotent DDL

- `DROP POLICY IF EXISTS` before `CREATE POLICY` where re-runs happen
- **Transactional** migrations when possible

---

## Backwards compatibility

- **Expand** schema first (add column nullable) → deploy app → **contract** (enforce NOT NULL) in later migration

---

## Data backfills

- **Batch** updates to avoid long locks
- **Index** creation — `CONCURRENTLY` on prod if outside transaction (raw Postgres); know Supabase constraints

---

## RLS rollout

- Enable RLS **with** policies tested — avoid table lockout

---

## Rollback story

- **Forward-fix** often safer than `DOWN` in prod — document recovery

---

## See also

- [[RLS Pattern Library]] · [[Index Strategy & Types]] · [[Database Reference]]
