---
tags: [gotchas, anti-patterns, rules, critical]
area: reference
status: stable
updated: 2026-04-06
---

# Critical Gotchas

> [!important] Check this note FIRST before writing any code. These are the mistakes that break things silently or cause hard-to-debug issues.

---

## Authentication & Identity

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Get user ID** | `supabase.auth.getUser()` for app identity | `getUserId()` from `src/lib/user` (sync) |
| **Native storage** | `localStorage.getItem("bruh_user_id")` | `getItem("bruh_user_id")` from nativeStorage.ts |
| **RPC auth** | Pass client UUID as sender/user param | Server derives via `get_my_user_id()` only |

---

## Database Queries

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Reply counts** | `supabase.from('posts').select('*, replies(count)')` → 15–20s delay | Use SECURITY DEFINER RPC |
| **Promise handling** | `.catch()` on Supabase query result | `.then(({ error }) => { if (error)... })` |
| **Search** | `.ilike()` without `.lower()` — case-sensitive | `.lower().ilike()` |
| **RLS pattern** | `auth.uid()` compared to `bruh_user_id` | Use `get_my_user_id()` in SECURITY DEFINER fn |

### PostgrestFilterBuilder Is NOT a Promise

```ts
// ❌ WRONG — .catch() does not exist
supabase.from('posts').update({...}).eq('id', id).catch(handleError);

// ✅ CORRECT
supabase.from('posts').update({...}).eq('id', id)
  .then(({ error }) => { if (error) handleError(error); });
```

---

## Keyboard & Layout

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Keyboard resize** | `Keyboard.resize: 'body'` | `Keyboard.resize: 'none'` |
| **AndroidManifest** | `adjustPan` or `adjustResize` | `adjustNothing` |
| **Keyboard inset** | Padding on inner scroller | Padding on outer flex column |
| **Keyboard height** | Hardcoded padding | Use `var(--kbd-h, 0px)` |

---

## Async & Reactivity

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Data fetching** | `useState + useEffect` for async data | `useQuery` from React Query |
| **Async handlers** | Fire-and-forget: `handler = () => { asyncFn() }` | `handler = async () => { await asyncFn(); check error }` |
| **Query keys** | Inline strings in components | Always use `src/lib/queryKeys.ts` exports |
| **i18n query keys** | Module-level key that needs language | Inside component (exception to module-level rule) |

---

## React & TypeScript

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **React import** | `import React from 'react'` | `import type { FC } from 'react'` (new JSX transform) |
| **Component tests** | `render(...)` directly | `renderWithProviders(...)` from `src/test/testUtils.tsx` |

---

## Native & Capacitor

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Reply picker** | Remove Capacitor guard from MemeReplyPicker | Guard is intentional — web users see store redirect |
| **Ad calls** | AdMob without `Capacitor.isNativePlatform()` | Already guarded in `src/lib/admob.ts` — don't bypass |

---

## Deployment & Scripts

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Global CLI** | `supabase ...` or `netlify ...` | `npx supabase ...` / `npx netlify ...` (EPERM on Windows) |
| **Android package** | Setting package in `capacitor.config.ts` | Package in `android/app/build.gradle` only |
| **Capgo + git** | Assuming `capgo-push.bat` commits code | Capgo OTA and git are separate — commit manually |
| **`.bat` files** | Committing `.bat` files | Use `.bat.example` templates; `.bat` is gitignored |
| **Dashboard webhooks** | Setting webhook secrets via Supabase Dashboard UI | Truncates secret JSON — use PL/pgSQL + Vault instead |
| **Netlify DNS CLI** | `netlify createDnsRecord` command | Use Netlify REST API directly |
| **Git auto-commit** | Committing/pushing without user asking | Never auto-commit. Wait for explicit user request. |

---

## Security

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| **Admin access** | Open `users` SELECT | Use helper RPCs (`lookup_user_for_oauth_email_conflict`, etc.) |
| **Secret compare** | `==` / `===` for secret strings | `timingSafeEqual()` from `_shared/timingSafeEqual.ts` |
| **Redirect** | `window.location = userProvidedUrl` | `safeRedirect(url)` validates same-origin first |
| **Deep links** | Adding new paths to DeepLinkHandler allowlist casually | Only `/u/` and `/post/` — allowlist is a security boundary |

---

## Feature Flags — Nuclear Options

> [!warning] Super-admin only flags — require `role = 'super_admin'` in DB
> - `app_killswitch` — disables entire app for all users
> - `emergency_api_lock` — locks all API mutations
> These cannot be toggled by regular admins and are intentionally hard to trigger.

---

## Quick Pre-Code Checklist

Before writing any new feature or fix:
- [ ] Skimmed [[CONSTITUTION]] — laws satisfied?
- [ ] Checked [[13 - Tombstones & Anti-Patterns]] — not reviving a killed approach?
- [ ] Read the **tables above** for the subsystem you touch (auth, DB, keyboard, async, deploy, security)?

---

## See also

- [[CONSTITUTION]] · [[INVARIANTS]] · [[13 - Tombstones & Anti-Patterns]]
- [[Bug History & Lessons]] (why these rules exist)
- [[Coding Patterns & Preferences]]
- [[Agent Quick Reference]]
- [[🏠 Home]]
