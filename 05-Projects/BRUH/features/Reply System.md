---
tags: [features, replies, memes, gifs, native]
area: features
updated: 2026-04-06
---

# Reply System

## Overview

Users reply to meme posts with GIFs/memes. The reply picker is **native-app only** — web users see a store redirect.

---

## Native Guard

> [!warning] CRITICAL — Never remove this guard
> `MemeReplyPicker` has a `Capacitor.isNativePlatform()` check at the very top.
> Web users see a redirect to the app store. This is intentional product behaviour.

```tsx
// MemeReplyPicker.tsx — top of component
if (!Capacitor.isNativePlatform()) {
  return <StoreRedirect />;  // redirects to App Store / Play Store
}
```

---

## Reply Limits (DB-Enforced)

| Limit | Value | Enforcement |
|-------|-------|-------------|
| Replies per user per UTC day | **50** | DB trigger on `replies` INSERT |
| `frame_data` field max size | **5 MB** | DB CHECK constraint |
| Sender ID | Server-derived | `get_my_user_id()` only (no client-supplied sender) |

---

## `replies` Table

```sql
replies (
  id UUID,
  post_id UUID REFERENCES posts(id),
  sender_id UUID,    -- set by get_my_user_id() server-side, never client
  receiver_id UUID,
  frame_data JSONB,  -- animated GIF frame data, ≤5MB
  created_at TIMESTAMP,
  -- ...
)
```

### `frame_data` Format
Stores animated GIF frame data for locally-saved GIFs.
- `frameData` — array of frame objects (dataURL + timing)
- `dataUrl` — static preview image (NOT animated)

> [!note] When `saveAnimatedGif` runs, it stores both `frameData` (full animation) and a static `dataUrl` preview. GifPlayer uses `previewFrameData` to render animated previews without re-decoding.

---

## MemeReplyPicker Flow

```
User taps reply on a post
  → MemeReplyPicker opens (native only)
  → Tabs: Trending / Stickers / My Own (same content families as inbox browse sheet, but full-screen reply flow)
  → Search + trending GIF grids: ~13% random InlineSquareAd slots (non-premium, not ad-free)
  → Sticker categories: InlineWideAd every 4th category
  → User selects meme → comment step → sendMemeReply
  → Invalidate postDetailQueryKey + MY_POSTS_QUERY_KEY
```

---

## GifBrowserSheet (inbox “browse GIFs” only)

Separate **sheet** from MemeReplyPicker — browse/copy UX from **RepliesInbox**.

| Tab | Content | Inline ads (non-premium, not ad-free) |
|-----|---------|----------------------------------------|
| Trending | Mixed BRUH + GIPHY GIF grid | ~13% `InlineSquareAd` in GIF grid |
| Stickers | Search + category strips / grids | Sticker search: `StickerScrollGrid` + `showAds`; categories: `InlineWideAd` every 4th |
| My Own | Same layout pattern as MemeReplyPicker My Own | None |

**My Own extras:**
- Creator CTAs → `/gif-creator`, `/sticker-creator`
- Manage → `/personal-media`

---

## Reply Count Query

> [!warning] NEVER use PostgREST embedding for reply counts
> `supabase.from('posts').select('*, replies(count)')` triggers per-row RLS on every row → **15–20 second delays**
> Always use a SECURITY DEFINER RPC to get reply counts.

---

## Post Detail (Infinite Query)

```ts
// Post detail page uses an infinite query for reply pagination
queryKey: postDetailQueryKey(postId)   // ["post-detail", postId]
staleTime: 60s
```

Prefetched from inbox when user hovers/focuses a post card (reduces perceived load time).

### Chat from Post Detail

**Post owner** (recipient of replies), **native**, not blocked: **Chat** entry starts or opens a 1:1 conversation via `start_conversation(reply_id)`. Full rules (premium send, GIFs, push): [[Chat System]].

---

## Reply Inbox

`RepliesInbox` (Tab 0):
- Fetches all user's posts via `fetch_my_posts` RPC
- Query key: `MY_POSTS_QUERY_KEY` with `staleTime: 30s`
- Only polls when tab is active (`isActive` prop)
- New reply realtime event → invalidates query → re-fetches

### Inline Ad Placement
Every **5th post** in the inbox shows an inline native ad card (AdMob), skipped for premium users.
