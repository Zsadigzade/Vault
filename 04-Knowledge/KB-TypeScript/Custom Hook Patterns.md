---
tags: [kb, react, hooks]
area: knowledge-base
updated: 2026-04-04
---

# Custom hook patterns

---

## When to extract

| Extract | Keep inline |
|---------|-------------|
| Reused stateful logic across 2+ components | One-off &lt;10 lines |
| Side effects with clear lifecycle | Tightly coupled to single component |

---

## API shape

- Return **tuple** for small arity (`useToggle`) or **object** for named fields (prefer object for public hooks — easier to extend)

---

## Dependencies

- **Exhaustive deps** — eslint `react-hooks/exhaustive-deps`
- Stabilize callbacks with **`useCallback`** only when consumers are memoized ([[React Rendering Optimization]])

---

## Naming

- Prefix **`use`** — `useFeed` not `getFeed`

---

## Testing

- **`@testing-library/react-hooks`** or render wrapper with providers — [[Testing Strategies & Patterns]]

---

## See also

- [[Component Composition Patterns]] · [[State Management Decision Tree]]
