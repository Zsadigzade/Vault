---
tags: [features, chat, performance, realtime, react-query]
area: features
updated: 2026-04-18
---

# Chat — Performance & realtime (implementation)

> **Product rules + schema overview:** [[Chat System]]. **Migrations:** [[Migrations Log]] — latest chat reliability **`20260418120000_chat_reliability_and_security`**, perf **`20260417120000_chat_performance`**.

Use this note when debugging **slow sends**, **slow incoming messages**, **messages vanishing after send**, **reaction glitches**, or **chat list churn** — not needed for generic “how chat works”.

---

## Database (`20260418120000_chat_reliability_and_security.sql`)

| Change | Why |
|--------|-----|
| `get_conversation_messages` final **`ORDER BY p.p_created_at DESC, p.pid DESC`** | Deterministic order after JOIN (no scrambled pages on refetch) |
| **`get_chat_unread_total`** | One RPC vs fetching 200 conversation rows to sum unread |
| `send_chat_message` | **`pg_advisory_xact_lock(hashtext(sender))`**, **15/min** burst, **2000** char text, GIF **`https://`**, daily count under lock |
| `toggle_chat_reaction` | Emoji UTF-8 **≤32** bytes (`convert_to`) |

---

## Database (`20260417120000_chat_performance.sql`)

| Change | Why |
|--------|-----|
| `send_chat_message` daily count | **UTC day range** on `created_at` (index-friendly) instead of `(created_at AT TIME ZONE 'UTC')::date` |
| `get_conversation_messages` | **CTE** batch for `chat_message_reactions` → one pass vs per-row subquery |
| `get_my_conversations` | **Batch unread** `COUNT` via join to page CTE vs correlated subquery per row |
| `start_conversation` | **Join** `conversation_participants` + `NOT EXISTS` third user vs scanning all convs with `COUNT(*)` |

---

## Client (repo paths)

| Area | Behavior |
|------|----------|
| `ChatThread.tsx` | Realtime **INSERT**: `mapChatMessageFromRealtimeInsert` → **`setQueryData`** (prepend); **skip** `sender_id === myId`; **debounced** `invalidateQueries` (~450ms) for peer messages / deletes / RPC parity; **reactions** channel **~1500ms** debounce; **`pendingSendsRef`** defers refetch while **`ChatInput`** send in flight; **optimistic** reactions + delete + rollback; **`onSent`** invalidates **`chat-messages`** after success |
| `ChatInput.tsx` | **`cancelQueries`** before optimistic row; **`onSendStart` / `onSendEnd`**; **`onSendEnd` before `onSent`**; replace `temp-*` with real id + brief **`_status: sent`**; **`mountedRef`** |
| `chat.ts` | **`mapChatMessageRow`**, **`mapChatMessageFromRealtimeInsert`**, **`findCachedConversationIdForOtherUser`**, **`fetchChatUnreadTotal`** → **`get_chat_unread_total`** RPC |
| `PostDetail.tsx` | **`findCachedConversationIdForOtherUser`** before **`start_conversation`** RPC |
| `RealtimeContext.tsx` | Chat INSERT: if `conversation_id` in **conversations** cache → skip `conversation_participants` fetch; **debounce** `lastChatMessageAt` (~300ms) |
| `ChatBubble.tsx` | **`React.memo`** + comparator (**`reactionsEqual`** value compare); swipe **elastic / threshold haptic / spring snap** |

---

## Anti-patterns (regression risks)

- Thread realtime handler → **full `invalidateQueries` on every INSERT** (drops instant UI).
- **`invalidateQueries(chat-messages)`** during in-flight **own** send without **cancel + defer** → optimistic row can disappear (refetch before row exists).
- Global chat listener → **unbounded** `conversation_participants` queries without cache check.
- SQL daily limit → **expression on `created_at`** that blocks `(sender_id, created_at)` index.
- **`ChatBubble`** memo comparing **`reactions` by reference** → all bubbles re-render on every refetch.

---

## See also

- [[Chat System]] · [[Database Reference]] · [[Data Layer]] · [[Keyboard & Layout]]
