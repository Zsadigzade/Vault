---
tags: [architecture, auth, security, session]
area: architecture
updated: 2026-04-03
---

# Authentication

## Two Auth Paths

| | OAuth / Magic-link | Custom Password Auth |
|--|-------------------|---------------------|
| Supabase session | Real JWT | Anon session via `validateUserSession` RPC |
| RLS strategy | Standard session-based RLS | SECURITY DEFINER RPCs via `get_my_user_id()` |
| `bruh_user_id` source | Written from DB by `validateUserSession` | Written by `loginWithPassword` / `registerWithPassword` |
| Use case | Social login, email magic link | Username + password accounts |

---

## The Golden Rule

> [!warning] CRITICAL
> **Always use `getUserId()`** (sync) to get the current user's ID.
> **Never** call `supabase.auth.getUser()` for app identity — this is for Supabase JWT users only, not the custom password-auth path.

```ts
// ✅ CORRECT
import { getUserId } from '@/lib/user';
const userId = getUserId();  // sync, reads from memCache → localStorage

// ❌ WRONG — breaks password-auth users
const { data: { user } } = await supabase.auth.getUser();
```

---

## `getUserId()` Read Chain

```
getUserId()
  1. memCache (in-memory, fastest)
  2. localStorage key "bruh_user_id"
  3. Returns null if neither found
```

> [!note] On native, `bruh_user_id` lives in Capacitor Preferences, bridged via `src/lib/nativeStorage.ts`. Never call `localStorage.getItem("bruh_user_id")` directly — use `getItem("bruh_user_id")` from nativeStorage.

---

## Password Auth Flow

```
registerWithPassword / loginWithPassword
  └─ Creates anon Supabase session
       └─ validateUserSession RPC
            └─ Writes bruh_user_id to storage
                 └─ getUserId() now works
```

---

## Session Management

| Event | Action |
|-------|--------|
| Login (password) | `loginWithPassword` → `validateUserSession` → store `bruh_user_id` |
| Login (OAuth) | Supabase handles JWT → `validateUserSession` also writes `bruh_user_id` |
| Logout | Clear `bruh_user_id` from storage + memCache, clear push token, clear recovery token |
| Native init | Wait for `BRUH_NATIVE_STORAGE_READY_EVENT` before reading user ID — see [[Startup Sequence & Storage Keys]] |
| Auth state change | `SIGNED_IN` / `INITIAL_SESSION` → subscribe realtime; logout → `removeChannel` |

---

## Recovery Token

- **Native-only** — stored in Capacitor Preferences (NOT mirrored to WebView localStorage on native)
- Used for account recovery flow
- Cleared on logout alongside push token

---

## RLS Strategy for Password-Auth Users

Password-auth users use anon Supabase sessions, so standard `auth.uid()` RLS won't match their `bruh_user_id`. Solution:

```sql
-- Server-side RPCs use this to get the authenticated user's ID
get_my_user_id()  -- SECURITY DEFINER, reads from session context

-- Never pass client UUID as a parameter to RPCs
-- Always derive from server-side get_my_user_id()
```

See [[Security Reference]] and [[Database Reference]] for full RLS patterns.

---

## Admin Auth

- `is_admin()` — no-arg server-side function (not enumerable from client)
- `admin_users` table SELECT is restricted (not public)
- Admin status cached via `["admin-status"]` query key with `staleTime: 0` + `refetchOnMount`
- Operations admin at `admin.bruhsocial.app` uses a separate auth layer

---

## Key Auth Files

| File | Purpose |
|------|---------|
| `src/lib/user/session.ts` | Session management, `validateUserSession` |
| `src/lib/user/registration.ts` | `registerWithPassword` |
| `src/lib/user/account.ts` | `loginWithPassword`, logout |
| `src/lib/user/recovery.ts` | Account recovery token |
| `src/lib/user/index.ts` | Exports `getUserId()` and all user functions |
| `src/lib/nativeStorage.ts` | Capacitor Preferences bridge for `bruh_user_id` |
