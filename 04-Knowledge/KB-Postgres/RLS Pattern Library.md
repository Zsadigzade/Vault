---
tags: [kb, postgres, rls, supabase]
area: knowledge-base
updated: 2026-04-04
---

# RLS pattern library

> [!tip] Project specifics: [[Security Reference]] · [[Database Reference]].

---

## `auth.uid()` mapping

- Often join `auth.users` to app `profiles` via stable **`user_id`** column

---

## Owner read/write

```sql
CREATE POLICY "own rows" ON posts FOR ALL
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());
```

*(Adjust to your FK to `profiles` / `get_my_user_id()` patterns.)*

---

## Public read, owner write

- `SELECT` true for all authenticated or anon as designed
- `INSERT/UPDATE` restricted

---

## Performance

| Issue | Mitigation |
|-------|------------|
| **per-row** function calls | **`STABLE`** functions; avoid heavy subqueries |
| **join explosion** | Prefer **security definer** RPC for aggregates |

---

## Testing RLS

- **JWT** role switching in tests or SQL session `SET request.jwt.claim.sub`
- **Negative tests** — user B cannot read A’s rows

---

## See also

- [[Supabase Security Hardening]] · [[Query Patterns & Anti-Patterns]]

## Production Patterns — 2026-04-13

- **Auto-enable RLS** — create event trigger on table creation to enable RLS automatically for new tables
- **SECURITY DEFINER RPCs** — bypass RLS for admin operations; use `get_my_user_id()` pattern for custom auth
- **Multi-tenant policies** — separate policies per role; avoid `USING (true)` on any write operation
- **Performance** — `(select auth.uid())` in policies is cached per query; avoid calling in loop
- Source: [Supabase official docs](https://supabase.com/docs/guides/database/postgres/row-level-security), [makerkit production patterns Jan 2026](https://makerkit.dev/blog/tutorials/supabase-rls-best-practices)
