---
tags: [meta, session, handoff, wip, agent:entry]
area: meta
status: active
updated: 2026-04-12
---

# Session handoff

> Read first in substantive BRUH sessions; update last before ending. **Vault-wide entry:** [[HOME]] · [[VAULT_CONSTITUTION]]. **Keep this file short** — depth: [[Chat System]] · [[Chat System — Performance]] · [[Push Notifications]] · [[Migrations Log]]. **Older April detail:** [[SESSION_HANDOFF — Extended 2026-04]].

## Apr 2026-04-11 session changes

### Design branch — Figma redesign (`design/new-ui`)
| Area | File(s) | Change |
|------|---------|--------|
| **CreateScreen** | `src/components/screens/CreateScreen.tsx` | Full Figma copy: animated card border, 3 quick-prompt chips (Challenges, Roast Me, Cord), `GET YOUR LINK` / `SHARE IT` dividers, Inter font, live-stat footer. Roast Me + Cord inject random templates. |
| **ChatList** | `src/components/screens/ChatList.tsx` | Inbox-style header with pink unread count pill, darker card rows with unread dot, refined swipe actions. |
| **ProfileTab** | `src/components/screens/ProfileTab.tsx` | Full-width gradient banner, large centred avatar (80px) with initials fallback, 3-column stats (Links / Replies / Reactions), Settings row at bottom. |
| **BottomNav** | `src/components/BottomNav.tsx` | Create → gradient pill circle (glows pink active), smaller icon tiles, Inter labels. |
| **index.css** | `src/index.css` | `font-display` → Inter Variable (branch-only). |

Branch: **`design/new-ui`** (pushed, not merged to `main`). Build clean. Switch: `git checkout design/new-ui`.

> **Archived perf passes (Apr 08/11) + i18n, bug-fix, SEO sessions (Apr 09/10):** [[SESSION_HANDOFF — Extended 2026-04]].

---

## Current objective

- **Chat:** Reliability + security pass shipped; **Apr 2026 UX pass** — keyboard stays open after send, clear delivered OS notifs on thread open, origin meme tap → `GifPreviewModal`, list swipe mute/leave, push title/body format + foreground toast suppressed when in thread; scroll-to-bottom FAB portaled to `[data-tour-portal]`. → [[Chat System]] · [[Push Notifications]] · [[Keyboard & Layout]].
- **DB:** Latest migration **`20260421120000_chat_leave_clears_messages`** — `messages_cleared_before TIMESTAMPTZ` on `conversation_participants`; `leave_conversation` stamps both `left_at` and `messages_cleared_before = NOW()`; `get_conversation_messages` filters `m.created_at >= v_cleared_before`. Prior: **`20260420120000_fortune_wheel_temp_premium`**. Drift → [[Migrations Log]].
- **Client polish:** Premium motion pass shipped. **BottomNav** active-tab icon stroke uses shared SVG `linearGradient` with `gradientUnits="userSpaceOnUse"` (keeps Create (+) visible). **Chat / notifications:** composer Sticker icon; ChatList empty state + Create CTA; **Settings → Notifications** — mark all read, clear all w/ undo toast, swipe-to-delete, first-visit swipe hint.
- **UI / Ads pass:** Create publish button — pulse-ring, shimmer, spring-bounce, spinner. **Fortune Wheel** → dedicated `/fortune-wheel` page (`FortuneWheelPage.tsx`); Profile shows styled button card. **Ad tiles** in GifBrowserSheet + MemeReplyPicker use `HiddenInterstitialAdGif` (~13% density, `pickAdSlots`). **Fortune Wheel SVG** overhaul: 8 slices with emoji + rotated labels; amber/gold premium slice; outer rim; golden pointer; non-rotating hub; pulsing glow.
- **Performance pass 3 (Apr 2026-04-22):** `create_post_atomic` RPC, `ChallengesScreen` lazy, `postListItems` useMemo, ChatList lazy images + prefetch, `totalReplies` useMemo, `vendor-icons` chunk, `recommendViralMedia` 5-min cache, `chatUnreadTotal` staleTime 60 s. All 161 tests pass.

---

## Apr 2026-04-22 session changes (performance pass 3)

| Area | File(s) | Change |
|------|---------|--------|
| **create_post_atomic RPC** | `supabase/migrations/20260422120000_create_post_atomic_rpc.sql` · `src/lib/user/posts.ts` | Merged dup-check + INSERT → single atomic SECURITY DEFINER RPC; saves ~200ms per post |
| **ChallengesScreen lazy** | `src/components/screens/CreateScreen.tsx` | `ChallengesScreen` → `lazy()` + `<Suspense fallback={null}>` |
| **postListItems useMemo** | `src/components/screens/RepliesInbox.tsx` | Full post list JSX in `useMemo` |
| **ChatList lazy images + prefetch** | `src/components/screens/ChatList.tsx` | `loading="lazy" decoding="async"` on thumbnails; `onPointerDown` prefetches thread messages |
| **totalReplies useMemo** | `src/components/screens/ProfileTab.tsx` | `reduce()` inside `useMemo([myPosts])` |
| **SETTINGS_META_QUERY_KEY** | `src/App.tsx` | Replaced `["settings-meta"]` string literals with constant |
| **vendor-icons chunk** | `vite.config.ts` | `lucide-react` → separate chunk |
| **recommendViralMedia cache** | `src/lib/recommendation.ts` | 5-min per-user module-level cache |
| **chatUnreadTotal staleTime** | `src/pages/Index.tsx` | 30 s → 60 s |

---

## Apr 2026-04-21 session changes

| Area | File(s) | Change |
|------|---------|--------|
| **Leave chat clears messages** | `supabase/migrations/20260421120000_chat_leave_clears_messages.sql` | `messages_cleared_before TIMESTAMPTZ` on `conversation_participants`. `leave_conversation` stamps NOW(). `get_conversation_messages` filters. |
| **GIF search infinite scroll** | `GifBrowserSheet.tsx` · `MemeReplyPicker.tsx` | `SEARCH_PAGE=20` + `searchOffset`/`searchHasMore`; IntersectionObserver sentinel; sticker tab routes to `onLoadMore`. |
| **Keyboard stays open on search** | Same two files | `type="search"` `inputMode="search"` `enterKeyHint="search"` + `onFocus` scroll-into-view (350ms). |
| **Blank origin-meme GIF** | `ChatThread.tsx` | `overflow-hidden`, `bg-secondary`, `object-contain`, `h-20 w-20`, `loading="lazy"`. |
| **Reaction popup — any hold** | `ChatBubble.tsx` | `onTouchStart/End/Cancel` removed from outer row; only on GIF button, caption div, text bubble. |
| **Duplicate X in search inputs** | Both files | `[&::-webkit-search-cancel-button]:hidden` — hides native clear; custom `<X>` is the only control. |

---

## Last known state (pulse)

- **Repo / semver:** `1.1.17` (`package.json` — current on `main`). **Active design branch:** `design/new-ui` (Figma redesign, not merged). Switch: `git checkout design/new-ui`. **Bump rule:** third segment **0–99** — **`1.0.99` → `1.1.0`**, never `1.0.100`. **`npm run version:bump`** → `scripts/bump-package-version.mjs`. → [[Capgo OTA]] · [[Commands & Scripts]].
- **Client shell:** 3 tabs in `Index.tsx` — **Chat** (0) · **Create** (1, default) · **Profile** (2). Create: single CTA (publish → green "Link Copied!" → share image); pulse-ring + shimmer. ProfileTab: Fortune wheel button card → `/fortune-wheel`. Bottom nav: unread badges, gradient stroke on active tab. → [[App Architecture]].
- **Settings:** Hub (`SettingsScreen.tsx`). All subpages share `SettingsSubpageShell`. Delete account uses `headerTone="danger"`. Tours wired.
- **Chat (native):** `ChatThread` scroll FAB portaled; `ChatBubble` long-press scoped to bubble only; `ChatInput` refocus after send; `notifications.ts` — `clearChatNotifications`, `setActiveChatConversationId`. Edge `send-push-notification` chat branch deployed. → [[Chat System]].
- **Monetization / ads:** `hasAnyPremiumAccess()` = `isPremiumUserCached()` OR `isTemporaryPremiumActive()`. Fortune wheel edge fn `fortune-spin` — ~12% win, 8h cooldown, 3 spins/UTC day. `EXPECTED_EDGE_FUNCTIONS` = **27**. → [[Monetization]].
- **Hosting (complete):** All domains on **Vercel**. DNS on **Cloudflare**. GoDaddy = registrar only. **Netlify fully removed**. Vercel project `landing` (prj_QQ75DLUaa5ks1Lcois5CFcm141pQ), auto-deploy from `main`, root `landing/`. → memory `dns_records.md`.
- **Supabase SSH docs:** `ssh supabase.sh <cmd>` for live docs — in `CLAUDE.md` + `.cursor/rules/bruh-project-memory.mdc`.
- **iOS:** Mac/Xcode device run for push + native ads still pending.

## Pending decisions

- None recorded.

## Blockers

- None — optional: Mac/Xcode device run for push + native ads.

## Next steps

1. **Google Search Console** — URL Inspection → Request Indexing for `https://bruhsocial.app/` and `https://bruhsocial.app/faq.html`.
2. Mac/Xcode: archive or device; confirm push + native ads.
3. **`npm run test`** — verify no regressions from chat / GIF search changes.

## See also

- [[CONSTITUTION]] · [[Agent Quick Reference]] · [[Agent spine — minimal tokens]] · [[🏠 Home]] · [[BRUH_HOME]] · [[AGENT_READ_ORDER]] · [[SESSION_HANDOFF — Extended 2026-04]] · [[Claude Skills Library (local)]] (Git clone + BRUH Cursor router) · [[External Git playbooks — README index]]
- Side repo: personal portfolio **zsadigzade.com** → [[Ziya Web — Portfolio]] (not BRUH)
