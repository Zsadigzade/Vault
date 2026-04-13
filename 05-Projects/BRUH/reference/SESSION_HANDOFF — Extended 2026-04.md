---
tags: [meta, session, handoff, archive]
area: meta
status: reference
updated: 2026-04-12
---

# Session handoff — extended (2026-04)

> **Default entry point:** [[SESSION_HANDOFF]] (short). Open only for **older milestone detail** without loading the full pulse into context.

---

## Chat v2 UX + DB (2026-04-06)

- Migration **`20260416180000_chat_improvements.sql`** — `left_at`, `last_message_sender_id`, `deleted_at` + **`delete_chat_message`**, **`reply_to_id`**, **`chat_message_reactions`** + **`toggle_chat_reaction`**; **`send_chat_message`** `p_reply_to_id`; **`start_conversation`** clears `left_at` on reopen. Client: FAB, new-msg divider, **MessageContextMenu**, optimistic send, **TypingIndicator** + presence `typing:{cid}`, list swipe mute/leave. **Deferred:** online dot on list avatars.
- Thread keyboard: scroller `paddingBottom` + `scrollTo`; **`dismissKeyboardOnScroll`** skips chat composer; **`ChatInput`** `keyboardOpen` → `pb-0`. → [[Keyboard & Layout]] · [[Chat System]].
- Base **`20260415120000_chat_system`**. → [[Migrations Log]].

## Other April milestones (skim)

- PostDetail / Create / inbox tweaks; AdMob test IDs + **GifBrowserSheet** ads; iOS **NativeAd** + Codemagic; ops **INCIDENT_RUNBOOK**, **health-check**, dashboard GHA; MCP **UptimeRobot** + stdio fix; vault **Agent MCP** notes; Sentry alerts deferred.

---

## Performance changes — Apr 2026-04-11 (DB fetch + runtime pass)

All `src/`. Zero behaviour changes — pure perf.

### DB fetch reduction
| File | Change | Why |
|------|--------|-----|
| `ProfileTab.tsx` | Removed `fetchNotifications()` from `settings-meta` queryFn | Was fetching 100 rows every 60 s for one boolean. Now reads `NOTIFICATIONS_INBOX_QUERY_KEY` cache CreateScreen already populates |
| `ProfileTab.tsx` | `settings-meta` staleTime 60 s → 5 min | Premium/moderation status rarely changes; realtime handles instant premium; 5× fewer refetches |
| `RepliesInbox.tsx` | `refetchInterval` 30 s → 120 s | Realtime fires `invalidateQueries` on new reply; poll was redundant |
| `ChatList.tsx` | Conversations staleTime 30 s → 60 s | Realtime bumps on new messages; 60 s sufficient |
| `rateLimiting.ts` | 30 s module-level pass cache on `checkRateLimit` | Edge fn 300–800 ms cold-start per reply send; cached skips it; DB triggers enforce server-side |
| `AdSlot.tsx` | `loading="lazy" decoding="async"` on interstitial image | Was missing; defers off-screen decode |

### React render reduction
| File | Change | Why |
|------|--------|-----|
| `ProfileTab.tsx` | `storedPostCount`/`storedReplyCount` → `useState` lazy init | `localStorage.getItem()` was running every render |
| `queryKeys.ts` | Added `SETTINGS_META_QUERY_KEY` constant | Removes scattered `["settings-meta"]` string literals |

---

## Performance changes — Apr 2026-04-08 (startup + re-render pass)

All `src/`. Zero behaviour changes — pure perf.

### Startup / load time
| File | Change | Why |
|------|--------|-----|
| `main.tsx` | Sentry + web-vitals → async `import()` | Removes `@sentry/react` from sync graph; React renders immediately |
| `App.tsx` | `OnboardingFlow` + `TourOverlay` → `lazy()` | New-user-only paths; dep trees deferred from cold start |
| `featureFlags.ts` | `getFeatureFlags()` batches flags in one `.in()` query | Two serial fetches → one |
| `App.tsx` | `checkSystemFlags` deferred 2 s on startup | Prevents racing with session validation + region detection |
| `vite.config.ts` | `vendor-analytics` (posthog-js) + `vendor-sentry` chunks | Out of initial JS parse; lazy-fetched |

### Runtime re-render reduction
| File | Change | Why |
|------|--------|-----|
| `RealtimeContext.tsx` | Context value → `useMemo` | Every realtime event created new object ref, re-rendered all consumers |
| `LanguageContext.tsx` | `t()` → `useCallback` | New function ref every render; all `useLanguage()` consumers re-rendered |
| `Index.tsx` | "Mount on first visit" for ChatList + ProfileTab; 3 stable `useCallback` | Non-default tabs skip startup mount; prop identity re-renders eliminated |
| `BottomNav.tsx` | `tabs` → `useMemo` | Array recreation on every render |
| `MemeScrollGrid.tsx` | Deduplicated row-2 render (~20 lines); `renderGifRow` accepts `sentinel` | Code quality |

---

## Apr 2026-04-10 — i18n full pass (pass 2)

| Area | Change |
|------|--------|
| **Architecture** | `src/lib/i18n.ts` → thin ~50-line loader. 4 locale JSON files `src/lib/locales/{en,az,ru,tr}.json` (~420 keys each). `TranslationKey = keyof typeof en` — typo = compile error. |
| **RegisterScreen** | All step headlines, strength labels, validation errors, UI buttons use `t()`. `STEP_HEADLINES` + `STRENGTH_LABELS` removed from module level. |
| **ForgotPasswordScreen** | Subtitle, instructions, labels, errors, button states fully translated. |
| **EmailSettings** | Header, desc, current email, errors, code-sent confirmation, verify/update labels. |
| **PasswordSettings** | All validation errors, placeholders, button states, forgot link. |
| **RecoveryCodeSettings** | Title, what-is-this, loading/unavailable, copy/save states, backup email flow. |
| **WelcomeScreen** | Tagline + Get Started button. |
| **LanguagePage** | One remaining hardcoded desc → `t("settings.languageDesc")`. |
| **FortuneWheelPage** | `HOW_IT_WORKS` + `PRIZE_FEATURES` moved into component (module-level = no lang change reaction); all strings use `t()`. |
| **FortuneWheel** | `BASE_SLICES` stays module-level; slices built via `useMemo([t])` mapping types → translated labels. |
| **CreateScreen** | `prompts` → `useMemo([t])`; maintenance toast uses `t("create.maintenanceMode")`. |
| **ProfileTab** | 7 toast/error strings + 3 premium labels use `t()`. |
| **New locale keys** | ~30 keys: `register.next`, `register.createAccount`, `register.joinTheChaos`, etc. |

---

## Apr 2026-04-10 — bug fixes

| Area | File | Fix |
|------|------|-----|
| Edge function count | `health-check/index.ts` | `EXPECTED_EDGE_FUNCTIONS` stays **27** — `contact-submit/` was empty orphan (removed). |
| Orphaned folder | `supabase/functions/contact-submit/` | Empty stub deleted |
| Rating re-show bug | `src/pages/Index.tsx` | `handleRatingSubmit` sets `bruh_rated` optimistically before API call |
| Test act() warnings | `bruh.e2e-integration.test.tsx` | `afterEach` event dispatch wrapped in `hookAct` |
| Sentry startup perf | `src/lib/sentryUser.ts` | Static `import * as Sentry` → dynamic `import('@sentry/react')` guarded by `VITE_SENTRY_DSN` |

---

## Apr 2026-04-09 — bug fixes (pass 2)

| Area | File | Fix |
|------|------|-----|
| Status bar overlap | `src/index.css` | `.safe-top` minimum 20px → 44px |
| Post creation speed | `src/lib/user/posts.ts` | Removed `checkRateLimit("post_create")` — DB trigger + dup check sufficient; edge fn adding 300–800 ms cold-start |
| Sentry TDZ fatal | `src/pages/Index.tsx` | `ReferenceError: Cannot access 'k' before initialization` — `useEffect` invalidating `CHAT_UNREAD_TOTAL_QUERY_KEY` must be **after** `useState(getInitialTab)` at line 119. Resolved in Sentry. |

---

## Apr 2026-04-09 — bug fixes + SEO

| Area | File | Fix |
|------|------|-----|
| Tour guide | `ChallengesScreen.tsx` | `startGroupIfNotDone("challenges")` effect (400ms delay); `data-tour="challenges-overview"` on outer wrapper |
| Reply badge persistence | `RealtimeContext.tsx` | `newReplyCount` persisted to `bruh_reply_badge`; restored on cold start; cleared on logout |
| Chat unread staleness | `Index.tsx` | `useEffect` invalidates `CHAT_UNREAD_TOTAL_QUERY_KEY` on `activeIndex === 0`. **CRITICAL:** after `useState(getInitialTab)` at line 119 |
| In-app FAQ | `HelpSettings.tsx` | 4 stale entries → 8 accurate (Premium price, Fortune Wheel, Challenges, web reply limit, anon rules) |
| Profile post/reply count | `ProfileTab.tsx` | Lifetime-max localStorage counters `bruh_lifetime_posts_{userId}` / `bruh_lifetime_replies_{userId}` |

### Landing page SEO (Apr 2026-04-09)

- **`index.html`** — title/description/keywords, canonical, favicons `?v=2`, `og:image` → `logo.jpg` (88KB), JSON-LD `@graph`: `MobileApplication` + `Organization` + `WebSite` + **`FAQPage`** (5 Q&As)
- **`sitemap.xml`** (new) — 6 URLs with priorities + lastmod
- **`robots.txt`** — `Disallow: /u.html`, `Sitemap:` directive
- **`vercel.json`** — replaced deleted `netlify.toml`; cache-control, CSP, URL rewrites
- All sub-pages — canonical, `favicon.png?v=2`, meta robots, OG tags
- **`faq.html`** — **FAQPage JSON-LD** with 14 Q&A pairs; fixed Android availability
- **Pending:** Google Search Console → URL Inspection → Request Indexing for `bruhsocial.app/` + `bruhsocial.app/faq.html`

---

## See also

- [[SESSION_HANDOFF]] · [[Vault Updates Summary]]
