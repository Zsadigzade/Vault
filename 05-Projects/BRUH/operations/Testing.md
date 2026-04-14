---
tags: [operations, testing, vitest, quality]
area: operations
updated: 2026-04-14
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

## Coverage (added 2026-04-13)

```bash
npx vitest run --coverage   # generates coverage/lcov.info
```

- Provider: `@vitest/coverage-v8@3.2.4` — **must** match Vitest version exactly.
- `coverage/` is gitignored. Codemagic uploads to Codecov automatically (`CODECOV_TOKEN` in secrets group).
- **161 tests** pass as of 2026-04-13.

### Dependency fixes applied (2026-04-13)
- `minimatch` override bumped `^3.1.4 → ^10.0.0` (test-exclude needed v10)
- `@testing-library/dom` added (was missing; broke 3 component test files)

---

## New tests

- Extend `setup.ts` or local `vi.mock` for Capacitor / purchases / PostHog as needed.  
- Mock `supabase.*` to match call shape used in component.

---

## See also

- [[Coding Patterns & Preferences]]
- [[User Preferences & Style]]
- [[🏠 Home]]
