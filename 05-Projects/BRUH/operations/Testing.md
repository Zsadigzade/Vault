---
tags: [operations, testing, vitest, quality]
area: operations
updated: 2026-04-06
---

# Testing

---

## When to run

| Situation | Command |
|-----------|---------|
| Iterating on a fix | `npx vitest run <path>` or `-t "test name"` |
| User explicitly asks, or **large / risky** change | `npm run test` (~155 tests) |

> [!tip] Project policy: **do not** run the full suite after every small change — see [[User Preferences & Style]].

---

## Infra

- **Runner:** Vitest  
- **Global mocks:** `src/test/setup.ts` — `@capacitor/core` (and related), Supabase chainable + `rpc`, PostHog, nativeStorage  

---

## `renderWithProviders`

- **File:** `src/test/testUtils.tsx`  
- Use for any component that calls React Query hooks — **not** bare `testing-library` `render`.

```tsx
import { renderWithProviders } from "@/test/testUtils";
```

---

## Suites (representative)

- Auth: `passwordAuth`, `oauthAuth`, `user`
- Integration: `feature-integration`, `bruh.e2e-integration` (large — top-level `vi.mock` list)
- Screens: `LoginScreen`, `DeleteAccountSettings`, etc.

---

## Gotchas

| Issue | Mitigation |
|-------|------------|
| **framer-motion mock** | Proxy returns new component type each access — **re-query DOM inside each `act` step** (e.g. OTP inputs). |
| **OTP tests** | One `fireEvent` per `await act` — not a tight loop. |
| **Fake timers** | Break `findByText` polling — prefer real timers + `waitFor`. |
| **`vi.mock`** | Only at module top (hoisted). |
| **`hideMeme`** | Async; keys `bruh_hidden_memes_<uid>`. |
| **Paste in jsdom** | Often doesn’t update controlled inputs — mock or alternate assertion. |

---

## New tests

- Extend `setup.ts` or local `vi.mock` for Capacitor / purchases / PostHog as needed.  
- Mock `supabase.*` to match call shape used in component.

---

## See also

- [[Coding Patterns & Preferences]]
- [[User Preferences & Style]]
- [[🏠 Home]]
