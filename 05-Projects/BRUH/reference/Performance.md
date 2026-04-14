---
tags: [reference, performance, optimization, react, bundle]
area: reference
updated: 2026-04-14
---

# Performance Optimizations

Summary of all performance passes shipped in Apr 2026. All changes zero-behaviour.

---

## Apr 2026-04-12 pass — DB round-trip + render + bundle + prefetch

### Changes

| File | Change | Why |
|------|--------|-----|
| `20260422120000_create_post_atomic_rpc.sql` | New `create_post_atomic(p_question)` SECURITY DEFINER RPC | Merges dup-check + INSERT → one atomic call; ~200ms saved |
| `src/lib/user/posts.ts` | `createPost` → `create_post_atomic` RPC | Eliminates 2 serial round-trips |
| `CreateScreen.tsx` | `ChallengesScreen` → `lazy()` with `<Suspense fallback={null}>` | Was eager even though only shown when bottom sheet opens |
| `RepliesInbox.tsx` | `postListItems` → `useMemo` | JSX fully rebuilt on every render |
| `ChatList.tsx` | Origin meme `<img>` gets `loading="lazy" decoding="async"` + `onPointerDown` prefetch of chat messages | Defers off-screen decode; first page of messages in cache before navigation |
| `ProfileTab.tsx` | `totalReplies` → `useMemo([myPosts])` | `.reduce()` ran on every render |
| `App.tsx` | Replaced `["settings-meta"]` strings with `SETTINGS_META_QUERY_KEY` | Key drift prevention |
| `vite.config.ts` | Added `vendor-icons` chunk for `lucide-react` | Cached independently from core vendor bundle |
| `src/lib/recommendation.ts` | 5-min per-user module-level cache on `recommendViralMedia` | Was fetching fresh every GifBrowserSheet open |
| `Index.tsx` | `chatUnreadTotal` staleTime 30s → 60s | Realtime context already invalidates on new message |

### Patterns
- **`create_post_atomic` RPC:** Do not re-add client-side dup-check or separate INSERT.
- **Chat prefetch:** `onPointerDown → prefetchInfiniteQuery(chatMessagesQueryKey)` — staleTime 15s matches ChatThread.
- **`useMemo` on post list JSX:** Expensive JSX arrays depending on many state slices must be memoized.

---

## Apr 2026-04-11 pass — DB fetch + runtime

### Changes

| File | Change | Why |
|------|--------|-----|
| `ProfileTab.tsx` | Removed `fetchNotifications()` from `settings-meta` queryFn | Was fetching 100 rows every 60s for one boolean; now uses `NOTIFICATIONS_INBOX_QUERY_KEY` |
| `ProfileTab.tsx` | `settings-meta` staleTime 60s → 5 min | Premium/moderation status rarely changes; realtime handles instant premium |
| `ProfileTab.tsx` | `storedPostCount`/`storedReplyCount` → `useState` lazy init | `localStorage.getItem()` was running every render |
| `queryKeys.ts` | Added `SETTINGS_META_QUERY_KEY = ["settings-meta"]` | Removes scattered string literals |
| `RepliesInbox.tsx` | `refetchInterval` 30s → 120s | Realtime fires `invalidateQueries` on new reply; poll redundant |
| `ChatList.tsx` | Conversations staleTime 30s → 60s | Realtime handles new messages |
| `rateLimiting.ts` | 30s module-level pass cache on `checkRateLimit` | Edge fn 300–800ms cold-start per reply send; cached skips it; DB triggers enforce server-side |
| `AdSlot.tsx` | `loading="lazy" decoding="async"` on interstitial image | Was missing; defers off-screen decode |

### Patterns
- **Shared `NOTIFICATIONS_INBOX_QUERY_KEY`:** Both `CreateScreen` and `ProfileTab` subscribe — do not add a separate `fetchNotifications()` in `settings-meta`.
- **`_rlPassCache`** in `rateLimiting.ts`: module-level, 30s TTL, only caches passes (not limits).

---

## Apr 2026-04-08 pass — startup + re-render

### Startup / load time

| File | Change | Why |
|------|--------|-----|
| `main.tsx` | Sentry + web-vitals → async `import()` | Removes `@sentry/react` from sync graph; React renders immediately |
| `App.tsx` | `OnboardingFlow` + `TourOverlay` → `lazy()` | New-user-only; deferred from cold start |
| `featureFlags.ts` | `getFeatureFlags([])` batches flags in one `.in()` query | Two serial fetches → one |
| `App.tsx` | `checkSystemFlags` deferred 2s on startup | Prevents racing with session validation + region detection |
| `vite.config.ts` | `vendor-analytics` (posthog-js) + `vendor-sentry` chunks | Out of initial JS parse; lazy-fetched |

### Runtime re-render reduction

| File | Change | Why |
|------|--------|-----|
| `RealtimeContext.tsx` | Context value → `useMemo` | Every realtime event created new object ref, re-rendered all consumers |
| `LanguageContext.tsx` | `t()` → `useCallback` | New function ref every render; all `useLanguage()` consumers re-rendered |
| `Index.tsx` | "Mount on first visit" for ChatList + ProfileTab; `mountedTabs: Set<number>`; 3 stable `useCallback` | Non-default tabs skip startup mount; prop identity re-renders eliminated |
| `BottomNav.tsx` | `tabs` → `useMemo` | Array recreation on every render |

### Gotchas / invariants
- **`Sentry.ErrorBoundary` NOT in render tree.** Don't add it back — use app's `<ErrorBoundary componentName="...">`.
- **Context memoization:** Always wrap context `value` objects in `useMemo` when provider has multiple `useState` fields.
- **`t` is now stable:** `useCallback([language])` — components calling `t` do NOT re-render on unrelated context changes.
- **Mount-on-first-visit (`mountedTabs`):** `{mountedTabs.has(i) && <TabComponent />}` — do not remove this guard.
- **`getFeatureFlags`:** Use for any multi-flag startup fetch. `getFeatureFlags([{ name, defaultValue? }])` → `Promise<Record<string, boolean>>`.

---

## See also

- [[App Architecture]] · [[Data Layer]] · [[Chat System — Performance]] · [[🏠 Home]]
