---
tags: [architecture, react-query, realtime, cache, storage]
area: architecture
updated: 2026-04-03
---

# Data Layer

## Core Rules

> [!warning]
> - All async data = `useQuery` / `useMutation` — **never** `useState + useEffect` for data fetching
> - All query keys = `src/lib/queryKeys.ts` — **never** inline strings in components
> - Optimistic mutations: `setQueryData` → background mutation → `invalidateQueries`

---

## React Query Keys

All keys defined in `src/lib/queryKeys.ts`:

| Export | Key | staleTime | Notes |
|--------|-----|-----------|-------|
| `MY_POSTS_QUERY_KEY` | `["my-posts"]` | 30s | Inbox only; active-tab gate |
| `postDetailQueryKey(id)` | `["post-detail", postId]` | 60s | Infinite query; prefetch from inbox |
| `CHALLENGES_QUERY_KEY` | `["active-challenges"]` | 5m | Merged global + regional |
| `regionalChallengesKey(region)` | `["regional-challenges", region]` | 5m | If region known |
| `postResolutionKey(...)` | `["post-resolution", ...]` | 30s | Reply picker context (username + situation) |
| `BAN_STATUS_QUERY_KEY` | `["ban-status"]` | 0 | Always fresh, 5m polling |
| `ADMIN_STATUS_QUERY_KEY` | `["admin-status"]` | 0 | staleTime: 0 + refetchOnMount |
| `ADMIN_BADGES_QUERY_KEY` | `["admin-badges"]` | 60s | 15s polling on ops dashboard |
| `SETTINGS_META_QUERY_KEY` | `["settings-meta"]` | 60s | 5-way data fetch; gated by `inTab && isActive` |
| `NOTIFICATIONS_INBOX_KEY` | `["notifications-inbox"]` | 120s | DB + broadcasts merge; realtime via `lastNotificationAt` |
| `blockedUsernamesKey(blocked)` | `["blocked-usernames", blocked]` | default | Batch `.in()` |

---

## Realtime Subscriptions

Single channel per user: `realtime-ctx-${userId}` in `RealtimeContext.tsx`

| Table | Event | Effect |
|-------|-------|--------|
| `replies` | INSERT | Increment `newReplyCount` + update `lastReplyAt` |
| `notifications` | INSERT | Update `lastNotificationAt` → invalidate inbox |
| `broadcasts` | INSERT | Update `lastBroadcastAt` |
| `challenges` | `*` | Update `lastChallengeAt` |
| `users` | UPDATE | Detect subscription status change → invalidate premium cache |

**Auth lifecycle**: `SIGNED_IN`/`INITIAL_SESSION` → subscribe; logout → `removeChannel`. `TOKEN_REFRESHED` ignored — channel survives.

> [!warning] **DB requirements for realtime:**
> - `supabase_realtime` publication must include `replies` (migration `20260311000009`)
> - `users` table needs `REPLICA IDENTITY FULL` (migration `20260319000001`) for `payload.old` access
> Without these, realtime events for replies/user updates silently fail.

---

## Cache Invalidation Paths

| Trigger | Where | Action |
|---------|-------|--------|
| New reply realtime event | `RepliesInbox` prevRef | Invalidate `MY_POSTS_QUERY_KEY` |
| Post created | `CreateScreen` → `onPostCreated` | Increment `refreshKey` |
| Post deleted | Optimistic | `setQueryData(filter out post)` |
| Reply sent | `MemeReplyPicker` success | Invalidate `postDetailQueryKey` + `MY_POSTS_QUERY_KEY` |
| Premium status change | Realtime `users.UPDATE` | Call `invalidatePremiumCache()` |
| Admin action | Various | Invalidate `ADMIN_BADGES_QUERY_KEY` |
| Cold-start session race | `App.tsx` after `validateUserSession` | Invalidate `MY_POSTS_QUERY_KEY` |
| Navigate to post (~150ms early) | `RepliesInbox` `onPointerDown` | `prefetchInfiniteQuery(postDetailQueryKey)` |

### prevRef Invalidation Pattern
Used to trigger query invalidation from realtime context values (timestamps, counters) without running on every render:
```ts
const prevRef = useRef(someTimestamp);
useEffect(() => {
  if (someTimestamp !== prevRef.current) {
    prevRef.current = someTimestamp;
    queryClient.invalidateQueries({ queryKey: someQueryKey });
  }
}, [someTimestamp, queryClient]);
```

---

## Native Storage Bridge

`src/lib/nativeStorage.ts` wraps Capacitor Preferences with a localStorage fallback for web.

```ts
// ✅ Always use these
import { getItem, setItem } from '@/lib/nativeStorage';
await getItem('bruh_user_id');
await setItem('bruh_user_id', userId);

// ❌ Never call directly on native
localStorage.getItem('bruh_user_id');
```

**Why**: Capacitor Preferences is the source of truth on native. Direct `localStorage` access bypasses the native keychain bridge.

**Init event**: `BRUH_NATIVE_STORAGE_READY_EVENT` fires when Preferences have hydrated into the WebView — auth gate must wait for this on native before reading user ID. Full timeline + keys: [[Startup Sequence & Storage Keys]].

---

## Optimistic Mutation Pattern

```ts
// Standard pattern used throughout the app
const mutation = useMutation({
  mutationFn: async (data) => { /* API call */ },
  onMutate: async (data) => {
    await queryClient.cancelQueries({ queryKey: MY_POSTS_QUERY_KEY });
    const prev = queryClient.getQueryData(MY_POSTS_QUERY_KEY);
    queryClient.setQueryData(MY_POSTS_QUERY_KEY, /* optimistic update */);
    return { prev };
  },
  onError: (err, data, context) => {
    queryClient.setQueryData(MY_POSTS_QUERY_KEY, context.prev);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: MY_POSTS_QUERY_KEY });
  },
});
```

---

## Reply System

### PostDetail — Infinite Query
`PostDetail` uses **`useInfiniteQuery`** with `postDetailQueryKey(postId)`. Pages from `fetchPostDetailPage` / `getNextPostDetailPageParam`. Question seeded from `MY_POSTS_QUERY_KEY` cache for instant header.

### Expired Meme Sentinel
Replies may have `meme_url === '[expired]'` after post TTL scrub. Use `isReplyMemeMediaExpired(reply)` to check — never compare the literal string directly in UI.

### frame_data Lazy-Loading
`has_frame_data` flag is set on each reply object. Actual bytes fetched separately via `fetchReplyFrameData(replyId)` on demand — not included in the initial reply list fetch.

### MemeReplyPicker Optimistic Send
1. `setSent(true)` immediately (shows success UI)
2. `setTimeout(() => navigate("/"), 1200)` starts at once
3. `await sendMemeReply(...)` runs in background
4. On failure: clear timer, `setSent(false)`, show error 5s
5. On success: invalidate `postDetailQueryKey` + `MY_POSTS_QUERY_KEY`

FK violation on `sender_id` (23503) → retry with `sender_id: null`.

---

## PostgREST Embedding Warning

> [!warning] NEVER use PostgREST resource embedding for reply counts
> `supabase.from('posts').select('*, replies(count)')` triggers per-row RLS evaluation → **15–20 second delays**
> Always use a `SECURITY DEFINER` RPC to get counts. See [[Database Reference]].

---

## See also

- [[Startup Sequence & Storage Keys]]
- [[Authentication]]
- [[Database Reference]]
- [[Coding Patterns & Preferences]]
- [[🏠 Home]]
