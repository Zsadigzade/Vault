---
tags: [kb, typescript, strict]
area: knowledge-base
updated: 2026-04-04
---

# TypeScript strict patterns

---

## Compiler flags (high value)

| Flag | Why |
|------|-----|
| **`strict`** | Baseline |
| **`noUncheckedIndexedAccess`** | `arr[i]` may be `undefined` — catches bugs |
| **`noImplicitOverride`** | Safer inheritance |
| **`exactOptionalPropertyTypes`** | Stricter optional props (can be noisy) |

---

## Branded types

```ts
type UserId = string & { __brand: "UserId" };
function userId(id: string): UserId { return id as UserId; }
```

Prevents mixing **raw strings** where IDs expected.

---

## `const` assertions & satisfies

- **`as const`** for literal tuples / discriminated unions
- **`satisfies`** — validate object shape without widening

---

## Avoid `any`

- Prefer **`unknown`** + narrow with `typeof` / Zod
- **`eslint` rule** `@typescript-eslint/no-explicit-any`

---

## Types from schema

- **Zod** `z.infer<typeof Schema>` at API boundaries — [[API Security & Rate Limiting]]

---

## See also

- [[Testing Strategies & Patterns]] · [[React Query Advanced Patterns]]
