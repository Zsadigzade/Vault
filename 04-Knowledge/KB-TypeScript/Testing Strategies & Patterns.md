---
tags: [kb, testing, vitest, react]
area: knowledge-base
updated: 2026-04-04
---

# Testing strategies & patterns

> [!tip] BRUH: `renderWithProviders`, targeted `npx vitest run` — [[Testing]] · [[User Preferences & Style]].

---

## Pyramid

| Layer | Scope |
|-------|--------|
| **Unit** | Pure functions, hooks with wrappers |
| **Integration** | Component + QueryClient + router |
| **E2E** | Few critical flows (Detox/Appium) — expensive |

---

## React Testing Library

- Test **behavior**, not implementation details
- **Avoid** snapshot soup for large trees

---

## MSW

- Mock **HTTP** at network layer — realistic loading/error tests

---

## Query hooks

- Wrap with **`QueryClientProvider`**; use **`queryClient.setQueryData`** for seeding

---

## Async

- `await findBy*` / `waitFor` — avoid `act` warnings by using RTL helpers

---

## Flakes

- Fake timers for debounce; **isolate** tests from real network

---

## See also

- [[Error Boundaries & Recovery]] · [[Custom Hook Patterns]] · [[Agent Debugging Strategies]]
