---
tags: [kb, react, state, architecture]
area: knowledge-base
updated: 2026-04-04
---

# State management decision tree

---

## Server state

→ **React Query** (`useQuery`, `useMutation`) — [[React Query Advanced Patterns]]  
Project: [[Data Layer]].

---

## URL state

→ **Search params** for shareable filters/tabs (`react-router` or similar)

---

## Truly global client state

→ **Lightweight store** (Zustand/Jotai) if many unrelated components need it

---

## Local UI state

→ **`useState` / `useReducer`** colocated in component

---

## Form state

→ **Controlled** fields or **react-hook-form** for complex validation — [[Form Design & Validation]]

---

## Derived state

→ **Compute in render** or `useMemo` if expensive — don’t duplicate source of truth

---

## Anti-pattern

- **Duplicating** server rows in global store “cache” — fights React Query

---

## See also

- [[App Architecture]] · [[React Query Advanced Patterns]]
