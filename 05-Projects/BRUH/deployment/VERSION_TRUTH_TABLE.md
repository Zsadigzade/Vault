---
tags: [deployment, versions, dependencies, agents]
area: deployment
status: stable
updated: 2026-04-06
---

# Version truth table

> [!tip] **Ground truth** for dependency versions is `package.json` in the BRUH repo. Update this table when `package.json` changes. Agents: do not assume newer major/minor APIs exist unless listed here or verified in repo.

**App package version (sample):** `1.0.75` — verify in repo `package.json` → `"version"` (Capgo channel may lag until OTA/store).

---

## TypeScript config note (TS 6.0 path)

Root `tsconfig.json` keeps **`baseUrl` + `paths`** for `@/*` (needed for tooling). **`tsconfig.app.json`** sets **`"ignoreDeprecations": "6.0"`** so the TS 6 **`baseUrl` deprecation** does not fail builds while the layout stays as-is. Do not remove without a deliberate paths migration.

---

## Core runtime

| Package | Range in package.json | Notes |
|---------|------------------------|-------|
| react / react-dom | ^18.3.1 | React 18; new JSX transform (no default React import). |
| typescript | ^5.8.3 | TS 5.x today; `ignoreDeprecations` in `tsconfig.app.json` for forward compatibility. |
| vite | ^5.4.21 | Vite 5 plugin ecosystem. |
| vitest | ^3.2.4 | Test runner v3. |

---

## Capacitor & native

| Package | Range in package.json | Notes |
|---------|------------------------|-------|
| @capacitor/core / cli / ios / android | ^8.3.0 (platforms) | Capacitor 8; check individual plugins for patch drift. |
| @capacitor/* plugins | ^8.x (per package) | Keep plugin majors aligned with core 8. |
| @capgo/capacitor-updater | ^8.45.0 | OTA; `appReadyTimeout` and notifyAppReady error handling are critical. |
| @capacitor-community/admob | ^8.0.0 | Native-only ad paths. |
| @revenuecat/purchases-capacitor | ^12.3.0 | Native purchases; webhook uses RC **V1** API compatibility (see vault MCP note). |

---

## Data & backend client

| Package | Range in package.json | Notes |
|---------|------------------------|-------|
| @supabase/supabase-js | ^2.101.0 | v2 client; Postgrest builders are not full Promises. |
| @tanstack/react-query | ^5.95.2 | v5 APIs; use `useQuery` patterns from project docs. |

---

## UI

| Package | Range in package.json | Notes |
|---------|------------------------|-------|
| tailwindcss | ^3.4.17 | Tailwind v3. |
| @radix-ui/react-* | ^1.x / ^2.x per component | Radix; compose with existing primitives. |
| framer-motion | ^12.38.0 | Motion v12. |
| lucide-react | ^0.462.0 | Icons. |

---

## Tooling (dev)

| Package | Range in package.json | Notes |
|---------|------------------------|-------|
| eslint | ^9.32.0 | Flat config / ESLint 9. |
| supabase (CLI) | ^2.76.16 | Use `npx supabase` on Windows. |

---

## See also

- [[Project Overview]] · [[Commands & Scripts]] · [[🏠 Home]]
- Repo `package.json` · `package-lock.json`
