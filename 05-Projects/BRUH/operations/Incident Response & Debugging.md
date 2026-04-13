---
tags: [debugging, incidents, errors, logs, troubleshooting, sentry, posthog]
area: operations
updated: 2026-04-06
---

# Incident Response & Debugging

> [!important] Always **check logs first** — Sentry, PostHog, Supabase — before diving into code. Production state comes from MCP/API, not guessing. **Use enabled MCP tools** (Sentry, PostHog `posthog-local`, Supabase, UptimeRobot, etc.) as the first hop — see [[Agent MCP — live verification]] · [[12 - MCP & External APIs]].

**Repo runbook (canonical ops checklist):** `scripts/INCIDENT_RUNBOOK.md` — UptimeRobot / health-check URL, Sentry (EU), emergency `curl` for **`emergency-set-mode`** (`app_killswitch`, `emergency_api_lock`, **`maintenance_mode`**), Capgo rollback, deploy commands, GitHub/Vercel analytics workflow notes.

---

## Emergency Contacts & Escalation

| Issue | Immediate Check | If Stuck |
|-------|-----------------|----------|
| App crashes everywhere | [[#Sentry—Error Tracking\|Sentry]] for error spike | Check [[Critical Gotchas]] for common causes |
| Auth failing | Supabase auth logs + PostHog funnel | [[Authentication]] — `getUserId()` vs `supabase.auth.getUser()` |
| Keyboard/layout broken | Device/browser specifics in PostHog | [[Keyboard & Layout]] — never use `resize: 'body'` |
| Database slow | Edge function logs + DB query times | Never use `replies(count)` PostgREST |
| OTA not deploying | [[Capgo OTA]] — version sync check | Capgo dashboard API logs |
| Native build broken | Codemagic logs + Xcode/Android Studio | [[iOS & Android]] |

---

## Sentry (Error Tracking)

**Host:** `de.sentry.io` (EU region)
**Org:** `bruh-social`
**Consumer project slug:** `react-native` (matches Vite `sentryVitePlugin` — name is historical)
**Other:** Admin app, Dashboard projects as configured in Sentry

**Alerts:** advanced metric/session/performance rules **deferred** until paid tier — see [[Sentry]].

### Accessing Logs

1. **Supabase → Project Settings → Functions → Logs** (for edge functions)
2. **Sentry** → Org → Browse projects → Select app → Look at error list
3. **PostHog** → Insights → Errors → filter by error type

### Common Patterns

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `"Cannot read property 'uid' of undefined"` | `supabase.auth.getUser()` on password-auth user → null session | Use `getUserId()` from nativeStorage (`src/lib/user`) |
| `"TypeError: e.catch is not a function"` | `.catch()` on PostgREST result (PromiseLike, not Promise) | Use `.then(({ error }) => ...)` |
| `"15-20s timeout"` | PostgREST `replies(count)` embedding | Use SECURITY DEFINER RPC |
| `"IDOR: user can see others' data"` | RLS using `auth.uid()` instead of `get_my_user_id()` | Check DB migration + redeploy |
| `"Layout broken on Android"` | Keyboard set to `resize: 'body'` | Change to `resize: 'none'` in `capacitor.config.ts` |
| `"401 Unauthorized"` | Edge function `verify_jwt = true` but JWT is invalid | Check auth flow + edge function config.toml |

---

## PostHog (Product Analytics)

**Host:** `https://eu.posthog.com` (EU region)
**Dashboard:** `https://eu.posthog.com/project/<project-id>`

### Quick Checks

```
Insights → Funnels → select step 1-2-3
  → see drop-off rate
  → drill into failed step
```

**Key funnels:**
- **Registration:** email → code → password → success
- **Auth callback:** OAuth start → redirect → session confirmed
- **Create post:** upload GIF → text entry → publish
- **Payments:** see premium upsell → click buy → confirm

### Error Spikes

```
Insights → Errors
  → Filter by error type / device / version
  → Check graph over time
  → Drill into session recordings
```

---

## Supabase Logs

### Database Operations

```bash
# Pull remote state to see what ran
npx supabase db pull

# Check recent migrations
npx supabase migration list
```

### Check Logs via Dashboard

1. Supabase → Project → **Statistics**
2. Look at API requests / errors
3. Check **Database** → **Query Performance** if slow

### Edge Function Logs

```bash
npx supabase functions logs <function-name>
```

**Common edge function issues:**
- Missing env secret → `undefined`
- `verify_jwt = true` but JWT invalid → 401
- Timeout (>600s) → function killed
- Rate limit triggered → 429 from Cloudflare

---

## Client-Side Debugging

### Browser DevTools (Web)

**F12 in browser:**
- **Console:** All `console.log` + errors
- **Network:** API requests to Supabase
- **Application → Cookies / Local Storage:** `bruh_user_id`, auth tokens
- **Performance:** Timeline flamegraph

### Native Debugging

#### iOS (Xcode)
```
Menu → View → Debug Area → Bottom tab
  → Console tab shows native + web logs
  → Breakpoints via Xcode
```

#### Android (Android Studio)
```
View → Tool Windows → Logcat
  Filter: "ReactNativeWebView" or "CordovaWebView"
  → Search "E/" for errors
```

**⚠️ Release builds don't show `console.log`** — use Supabase error tables or Sentry instead.

---

## Common Fixes

### Rate Limit Exceeded

**Source:** `rate-limiter` edge function (posts, replies, reports)

**Fix:**
1. Check PostHog — how many calls in last minute?
2. Verify mutation is **not** fire-and-forget (should await)
3. If real issue: increase limit in `rate-limiter` function

### Authentication Fails After Password Reset

**Likely cause:** OTP not being passed correctly to `loginWithPassword`.

**Debug steps:**
1. Check email was sent (Supabase → Auth → Users)
2. Verify OTP length (should be 6 digits)
3. Check client code — OTP stored correctly?
4. **Never log OTP to console** — security risk

### Keyboard Layout Broken

**Symptoms:** Text input hidden, can't scroll, layout shifts

**Causes:**
- `Keyboard.resize: 'body'` → **wrong**, use `'none'`
- `adjustPan` / `adjustResize` → **wrong**, use `adjustNothing`
- Keyboard padding on inner scroller instead of outer container

**Fix:**
1. Check `capacitor.config.ts` → `windowSoftInputMode`
2. Check component paddingBottom — should be on outer flex column
3. Verify `--kbd-h` CSS var is being set (2026-03 patch)

---

## Deployment Issues

### Capgo OTA Not Showing in App

**Steps to debug:**
1. Check Capgo dashboard — is version uploaded?
2. **Verify version sync:** `package.json` version matches uploaded version
3. Check app settings → are auto-updates enabled?
4. Force reload: Close app completely + reopen

**⚠️ Common mistake:** Capgo-push bumps version but git commit isn't pushed. App sees wrong version.

### iOS Build Fails in Codemagic

**Check:**
1. Tag format correct? `git tag v1.0.68` (not `1.0.68`)
2. Codemagic secrets present? Certificate + provisioning profile (should be ✅)
3. Team ID matches? iOS Bundle ID = `app.bruhsocial.app` → Team ID `39FVY58F26` in entitlements

### Android Build Fails

**Check:**
1. Package name in `android/app/build.gradle` = `com.bruh.app` (NOT in capacitor.config.ts)
2. Keystore password correct? (set in Codemagic `CM_*` secrets)
3. Native code change? Might need full rebuild, not OTA

---

## Database Issues

### Query Timeout (> 30 seconds)

**Most likely:** `replies(count)` PostgREST embedding

**Fix:**
```sql
-- ❌ BAD — 15-20s per post
SELECT id, body, replies(count) FROM posts WHERE user_id = auth.uid();

-- ✅ GOOD — use RPC
SELECT * FROM fetch_my_posts();  -- includes reply_count
```

### RLS Rejection (`new row violates row-level security`)

**Cause:** INSERT/UPDATE not matching RLS policy

**Debug:**
1. Check policy — does it use `get_my_user_id()` or `auth.uid()`?
2. Password-auth users have `auth.uid()` = null → use `get_my_user_id()`
3. Check record before insert — owner matches?

### Migration Drift

**Symptom:** Local state ≠ remote state

**Fix:**
```bash
# See what's out of sync
npx supabase migration list

# Repair (if local is correct)
npx supabase migration repair --status reverted <id>
npx supabase db push --yes

# Or pull latest from remote
npx supabase db pull
```

---

## Testing Locally

### Supabase Local Stack

```bash
npx supabase start
# → PostgreSQL + Supabase emulator on localhost:54321

npx supabase stop
```

### Reset Local DB

```bash
npx supabase db reset
# → Clears + reapplies all migrations
```

---

## Memory Files (Detailed Incident Logs)

These live in repo memory — check them for patterns:

- `.claude/projects/.../memory/MEMORY.md` — high-level index
- `.claude/projects/.../memory/bug_history_and_lessons.md` — incident root causes
- `.claude/projects/.../memory/security.md` — past security issues
- `.claude/projects/.../memory/database.md` — DB gotchas

---

## Post-Incident Checklist

After fixing a production issue:

- [ ] Documented in [[Bug History & Lessons]]
- [ ] Added test case (if valid regression)
- [ ] Cross-checked Sentry / PostHog for other instances
- [ ] Updated [[Critical Gotchas]] if pattern
- [ ] Notified team (if user-facing)
- [ ] Root cause clear (not just symptom fix)

---

## See also

- [[Sentry]]
- [[Analytics Dashboard]]
- [[Edge Functions]]
- [[Database Reference]]
- [[Critical Gotchas]]
- [[🏠 Home]]
