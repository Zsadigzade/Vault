---
tags: [features, push, fcm, notifications]
area: features
updated: 2026-04-07
---

# Push Notifications

## Stack

| Component | Technology |
|-----------|-----------|
| Service | Firebase Cloud Messaging (FCM) |
| Edge function | `supabase/functions/send-push-notification` |
| Token storage | `upsert_push_token` RPC |
| Realtime trigger | `notifications` table INSERT; **`chat_messages`** INSERT → same edge fn (DB trigger) |

---

## FCM Secrets (Supabase)

| Secret | Purpose |
|--------|---------|
| `FCM_PROJECT_ID` | Firebase project identifier |
| `FCM_CLIENT_EMAIL` | Service account email |
| `FCM_PRIVATE_KEY` | Service account private key (PEM) |

All three required for `send-push-notification` edge function to authenticate with FCM.

---

## Token Registration Flow

```
User grants notification permission
  → Capacitor PushNotifications.register()
  → FCM returns device token
  → upsert_push_token(token, platform) RPC
       → validates non-null session (rejects if no auth)
       → upserts into push_tokens table
```

> [!warning] `upsert_push_token` rejects null sessions (hardened in 2026-04-11 audit). Ensure user is authenticated before registering push token.

---

## Token Lifecycle

| Event | Action |
|-------|--------|
| Login | Register push token after auth |
| Logout | Delete push token from DB + clear from Preferences |
| App foreground | Re-register token (FCM tokens can rotate) |
| Permission denied | Skip registration gracefully |

---

## Notification Types

Notifications arrive via two paths:

| Path | Source | Stored in |
|------|--------|-----------|
| Push (FCM) | `send-push-notification` edge fn | External (FCM) |
| In-app | DB `notifications` table | `notifications` table |
| Broadcasts | DB `broadcasts` table | `broadcasts` table |

The `notifications-inbox` query merges DB notifications + broadcasts into a unified feed.

**In-app inbox UI (`NotificationsSettings.tsx`, route `/settings/notifications`):** **Mark all read**; **Clear all** with Sonner **Undo** (~4s) and delayed DB/localStorage persist; **swipe left** on a row to delete (notifications) or dismiss (broadcasts) — Framer **`drag="x"`**; red trash affordance behind row. Bulk RPCs: **`markAllNotificationsRead`**, **`deleteAllNotifications`** (`src/lib/user/notifications.ts`); **`markAllBroadcastsReadLocally`** / **`dismissAllBroadcastsLocally`** (`notificationsInbox.ts`). One-time swipe hint: **`bruh_notif_swipe_hint_shown`** in localStorage.

---

## Realtime Integration

When a reply is received:
1. `replies` INSERT → realtime subscription fires in `RealtimeContext`
2. `newReplyCount` incremented
3. `lastReplyAt` updated
4. RepliesInbox badge updates

When a notification arrives:
1. `notifications` INSERT → `lastNotificationAt` updates
2. `NOTIFICATIONS_INBOX_KEY` query invalidated
3. Notification badge shows

**Chat:** `chat_messages` INSERT → `send-push-notification` with `table: 'chat_messages'` → FCM to the **other** participant unless `conversation_participants.muted` or `push_tokens.preferences.chatMessages === false`. In-app row in `notifications` with `type: chat`. Tap navigates to `/chat/:conversationId`. **Alert copy (2026-04):** **title** = sender **username** only (no leading 💬); **body** = plain text message, or **🎬** + GIF title / **🎬 GIF**, or **🩹 Sticker** when `gif_source` / title heuristics indicate sticker. **Client:** `clearChatNotifications` removes delivered tray entries for that `conversationId`; `setActiveChatConversationId` suppresses redundant foreground toast when the user is already in-thread. See [[Chat System]].

---

## `send-push-notification` Edge Function

Accepts:
```ts
{
  user_id: string;      // target user
  title: string;
  body: string;
  data?: Record<string, string>;  // deep link payload
}
```

Looks up device token from `push_tokens` table, sends via FCM v1 HTTP API.

---

## Notification Channels (Android)

Android requires notification channels for Android 8.0+. Channels defined in `android/app/src/main/res/xml/` or via Capacitor plugin config.

| Channel | Purpose |
|---------|---------|
| `replies` | New meme reply received |
| `general` | Broadcasts + system notifications |
| `chat` | New chat message (FCM + in-app; preference **`chatMessages`**) |

---

## See also

- [[Chat System]]
- [[Edge Functions]]

## FCM Best Practices — 2026-04-13

- **Notification channels** — required for Android 8.0+; always create named channels with appropriate importance
- **FCM token storage** — store securely server-side; refresh and re-register on token rotation
- **In-app suppression** — suppress notification display if user already in the relevant thread/screen
- **Notification fatigue** — balance frequency; opt-outs spike when users feel overloaded
- Source: [Braze push best practices](https://www.braze.com/resources/articles/push-notifications-best-practices), [Zignuts FCM Android guide](https://www.zignuts.com/blog/implement-push-notifications-in-android)
