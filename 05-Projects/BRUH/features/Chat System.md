---
tags: [features, chat, dm, premium, native]
area: features
updated: 2026-04-07
---

# Chat System

1:1 **direct messages** between users who already have a **meme reply** relationship. **Native only** (iOS/Android) — same rule as [[Reply System]] picker; web shows “download the app”.

**Layout:** Fixed composer `bottom: var(--kbd-h)`; list **`paddingBottom`** includes **`var(--kbd-h)`**; **`App.tsx`** scroll-dismiss skips chat (`data-chat-composer` + `data-chat-thread-scroll`). **Scroll-to-bottom FAB** is **not** `fixed` inside the route `Screen` — it is **`createPortal`**’d to **`[data-tour-portal]`** with **`position: absolute`** so `right`/`bottom` are correct (Framer **`motion.div`** on `Screen` otherwise breaks `fixed`). → [[Keyboard & Layout]].

**Performance / realtime implementation (agents debugging slowness):** → [[Chat System — Performance]] — do not duplicate here.

---

## Product rules

| Rule | Detail |
|------|--------|
| Start chat | **Post owner** from **PostDetail** — RPC `start_conversation(p_reply_id)`; optional **cache** `findCachedConversationIdForOtherUser` before RPC |
| Deduplication | One conversation per **user pair**; reuse existing; **`left_at`** cleared on reopen |
| Send | **Premium** (`_user_is_premium_chat` + 48h grace); **reactions** premium |
| Read | All participants read history; free users see **upsell** (no composer) |
| Blocks | Checked on start + send |
| Rate limit | **100** msgs / sender / **UTC day** |
| Mute / leave / delete | `muted`; **`leave_conversation`** → `left_at`; **`delete_chat_message`** 24h soft-delete |
| Reply | **`reply_to_id`** + quoted preview |

---

## Database (repo)

**Migrations:** `20260415120000_chat_system` · `20260416180000_chat_improvements` · **`20260417120000_chat_performance`** ([[Migrations Log]] · [[Chat System — Performance]])

| Object | Notes |
|--------|--------|
| Tables | `conversations`, `conversation_participants`, `chat_messages`, `chat_message_reactions` |
| RPCs | `start_conversation`, `get_my_conversations`, `get_conversation_messages`, `get_conversation_meta`, `send_chat_message`, `mark_conversation_read`, `mute_conversation`, `delete_chat_message`, `toggle_chat_reaction`, `leave_conversation` — **SECURITY DEFINER**, `p_user_id` / `get_my_user_id()` |
| Realtime | `chat_messages`, `chat_message_reactions` in publication |
| Push | `chat_messages` INSERT → `send-push-notification` |

---

## Client (repo)

| Area | Path / key |
|------|------------|
| API | `src/lib/user/chat.ts`, `chatTypes.ts` |
| UI | **`chatUi.ts`** (shared Tailwind tokens — headers, cards, composer surface, peer bubbles; aligns with settings visual language) · `ChatList.tsx`, `ChatThread.tsx`, `ChatInput.tsx`, `ChatBubble.tsx`, `ChatHeader.tsx`, `GifPreviewModal`, `TypingIndicator`, `MessageContextMenu`, `chatQuickReactions.ts` |
| Shell | `RealtimeContext` — `lastChatMessageAt`; thread channels for messages + reactions + typing presence |
| Nav / i18n | Index tab **Chat**; `chat.*` keys; push prefs `chatMessages` |

**Native UX (2026-04):** After send, keyboard stays open (`ChatInput` — prevent focus steal on send/GIF buttons + refocus textarea). **GIF/sticker picker** — Lucide **`Sticker`** icon (not `ImagePlus`) opens **`GifBrowserSheet`**. **`clearChatNotifications(conversationId)`** + **`setActiveChatConversationId`** in **`src/lib/notifications.ts`** — opening a thread clears matching delivered OS pushes; foreground chat push skips Sonner if user is already in that thread. **ChatList** — `data-swipe-row`; mute/leave strip `opacity-0` until swipe; touch `stopPropagation` + **`Index.tsx`** ignores horizontal tab swipe when target is inside swipe row. **Origin meme** in thread context card → tap opens **`GifPreviewModal`**. **Empty list** — full-height **`EmptyState`** with **`emojiFloat`**, **`chat.emptyHint`**, CTA **Create a post** → **`onGoCreate`** switches **`Index`** to Create tab (1).

**Deferred:** online dot on **ChatList** avatars.

---

## See also

- [[Chat System — Performance]] · [[Database Reference]] · [[Migrations Log]] · [[Push Notifications]] · [[Reply System]] · [[App Architecture]] · [[Monetization]]
