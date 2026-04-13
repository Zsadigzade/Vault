---
tags: [preferences, patterns, style, rules, agent-guide]
area: reference
updated: 2026-04-06
---

# Coding Patterns & Preferences

> [!important] Read this before writing any code for this project. These are the established patterns and personal preferences derived from the codebase and past conversations.

---

## React Patterns

### Never `import React from 'react'`
React 18 new JSX transform. Only type imports allowed:
```tsx
// ✅ CORRECT
import type { FC, ReactNode } from 'react';

// ❌ WRONG
import React from 'react';
import React, { FC } from 'react';
```

### Data Fetching: Always `useQuery`
```tsx
// ✅ CORRECT
const { data } = useQuery({ queryKey: MY_POSTS_QUERY_KEY, queryFn: fetchMyPosts });

// ❌ WRONG — never for async data
const [posts, setPosts] = useState([]);
useEffect(() => { fetchMyPosts().then(setPosts); }, []);
```

### Query Keys: Always Module-Level
```ts
// ✅ CORRECT — src/lib/queryKeys.ts, module-level
export const MY_POSTS_QUERY_KEY = ["my-posts"] as const;

// ❌ WRONG — inline in component
const { data } = useQuery({ queryKey: ["my-posts"], ... });

// Exception: i18n-dependent keys (MUST be inside component to rebuild on language change)
const { language } = useLanguage();
const challengesKey = ["active-challenges", language]; // ← inside component is correct here
```

### Optimistic Mutations Pattern
```ts
onMutate: async (data) => {
  await queryClient.cancelQueries({ queryKey: MY_POSTS_QUERY_KEY });
  const prev = queryClient.getQueryData(MY_POSTS_QUERY_KEY);
  queryClient.setQueryData(MY_POSTS_QUERY_KEY, /* optimistic update */);
  return { prev };
},
onError: (_err, _data, context) => {
  queryClient.setQueryData(MY_POSTS_QUERY_KEY, context?.prev);
},
onSettled: () => {
  queryClient.invalidateQueries({ queryKey: MY_POSTS_QUERY_KEY });
},
```

### Realtime Invalidation: prevRef Pattern
```ts
const prevRef = useRef(someTimestamp);
useEffect(() => {
  if (someTimestamp !== prevRef.current) {
    prevRef.current = someTimestamp;
    queryClient.invalidateQueries({ queryKey: MY_POSTS_QUERY_KEY });
  }
}, [someTimestamp, queryClient]);
```

---

## Async Handlers

> [!warning] CRITICAL: Never fire-and-forget in UI handlers
```tsx
// ✅ CORRECT — always await, always check error
const handleSubmit = async () => {
  setLoading(true);
  const result = await someService(data);
  if (result?.error) {
    setError(result.error);
    setLoading(false);
    return;
  }
  // success path
  navigate("/");
};

// ❌ WRONG — fire-and-forget
const handleSubmit = () => {
  someService(data);  // failure silently ignored
  navigate("/");      // always navigates even if service failed
};
```

**Why**: `ForgotPasswordScreen.handleResetPassword` originally did this. OTP failures showed "Password reset!" and navigated away — a false success. Fixed 2026-03-27.

Use `result?.error` (optional chaining) when mocks may return `undefined` in tests.

---

## Supabase / Database

### PostgrestFilterBuilder Has No `.catch()`
```ts
// ✅ CORRECT
supabase.from('posts').update({ x: 1 }).eq('id', id)
  .then(({ error }) => { if (error) handleError(error); });

// ❌ WRONG — .catch() does not exist on PromiseLike
supabase.from('posts').update({ x: 1 }).eq('id', id)
  .catch(err => handleError(err));
```

### Never PostgREST Embedding for Counts
```ts
// ❌ WRONG — 15-20 second delay due to per-row RLS
supabase.from('posts').select('*, replies(count)');

// ✅ CORRECT — SECURITY DEFINER RPC
const { data } = await supabase.rpc('fetch_my_posts');
```

### Case-Insensitive Search
```ts
// ✅ CORRECT
.filter('username', 'ilike', `%${term.toLowerCase()}%`)
// or
.ilike('username', `%${term}%`)  // only safe if column is already lowercase
```

---

## Layout & Keyboard

### Outer Container Gets Keyboard Padding, NOT Inner Scroller
```tsx
// ✅ CORRECT
<div style={{ paddingBottom: keyboardHeight }}>     {/* outer flex column */}
  <div className="flex-1 overflow-y-auto">            {/* inner — scrolls */}
    {children}
  </div>
</div>

// ❌ WRONG
<div className="flex-1 overflow-y-auto"
  style={{ paddingBottom: keyboardHeight }}>          {/* inner — breaks scroll */}
  {children}
</div>
```

### MemeReplyPicker Keyboard Rule
Use **non-motion** wrapper with **`transition-none`** so inset snaps (not eased):
```tsx
// Comment field: scrollIntoView({ behavior: "instant" }) — not smooth
```

### Auth Screens: Hide Logo When Keyboard Open
```tsx
const { height: kbdH } = useKeyboardHeight();
const kbdOpen = kbdH > 0;
{!kbdOpen && <BruhLogo />}  // reclaims ~100px on small screens
```

---

## AnimatePresence + Portal Pattern

> [!warning] Wrong placement causes instant unmount (no exit animation)
```tsx
// ❌ WRONG — condition outside portal, AnimatePresence never fires exit
{showSheet && createPortal(
  <AnimatePresence>
    <motion.div exit={{ opacity: 0 }}>...</motion.div>
  </AnimatePresence>,
  document.body
)}

// ✅ CORRECT — portal always mounted, condition inside AnimatePresence
{createPortal(
  <AnimatePresence>
    {showSheet && (
      <motion.div key="sheet" exit={{ opacity: 0 }}>...</motion.div>
    )}
  </AnimatePresence>,
  document.body
)}
```

All bottom sheets use `getBottomSheetPortalTarget()` from `src/lib/bottomSheetPortal.ts`.

---

## PullToRefresh Inside Sheets

Every ancestor must be a flex container:
```tsx
// ✅ CORRECT — flex chain for scroll to work
<div className="flex-1 min-h-0 flex flex-col overflow-hidden">
  <ChallengesScreen />  {/* contains PullToRefresh → flex-1 overflow-y-auto */}
</div>
```

---

## UI / Component Style Preferences

### Minimal Copy in Step Panels
CreateScreen step panels use **titles only** — no subtitle paragraphs underneath:
```tsx
// ✅ CORRECT — single title line
<p>{t('create.step1Title')}</p>

// ❌ WRONG — no extra description copy
<p>{t('create.step1Title')}</p>
<p className="text-sm text-muted">{t('create.step1Description')}</p>
```

### Step Panel Styling (brand style)
- `rounded-2xl` panels, `bg-secondary/30`, `shadow-sm`
- Thin **left vertical gradient bar** (brand colors) as accent
- Step 1 success: `emerald` border/background tint
- Spacer between card and steps: `max-h-[min(12rem,22vh)]` cap (prevents steps sitting too low on tall phones)

### Design Language
- IG accent palette: CSS `--ig-1`…`--ig-4` (purple/magenta/pink/red)
- `.text-ig-gradient`, `.bg-ig-gradient`, `.glow-ig`, `.create-card-ig-ring`
- Fonts: Plus Jakarta Sans Variable (body) + Bricolage Grotesque Variable (display)
- `max-w-app-story` ≈ 21rem for content columns (Create tab)
- `maximum-scale=5` in viewport (no `user-scalable=no` — accessibility)

---

## Error Handling

### ErrorBoundary Usage
```tsx
// Route-level wrapping via Screen helper:
function Screen({ name, children }: ...) {
  return (
    <MobileFrame>
      <ErrorBoundary componentName={name} fallback={<GoBackButton />}>
        {children}
      </ErrorBoundary>
    </MobileFrame>
  );
}
// Used for every route except /admin and /auth/callback
```

### `result?.error` Pattern
Always use optional chaining — test mocks may return `undefined`:
```ts
const result = await someService(...);
if (result?.error) { /* handle */ }
```

---

## Testing

- Use `renderWithProviders` (not bare `render`) for all component tests
- Global mocks in `src/test/setup.ts`: `@capacitor/core`, Supabase, PostHog, nativeStorage
- Targeted file during development: `npx vitest run src/test/<file>.test.ts`
- Full suite only when user asks or for broad/risky changes: `npm run test`

---

## Git / Version Control

> [!warning] NEVER auto-commit or push to git
- User wants full control of git history
- After code changes: stop. Do not stage, commit, or push
- Can *suggest* committing but never execute it
- `capgo-push.bat` does NOT commit — version bump committed manually by user

---

## Debugging on Android Release Builds

> [!note] `console.log` does NOT appear in Android logcat on release APKs
`setWebContentsDebuggingEnabled(false)` disables JS console in release builds.
Use UI toasts or Supabase `error_logs` table for device debugging instead.

---

## Canvas / Image Generation

When generating images (posting card):
```ts
// ✅ CORRECT — synchronous, gives base64 directly
const dataUrl = canvas.toDataURL("image/jpeg", quality);

// ❌ WRONG — async callback has 100-500ms scheduling overhead on Android WebView release
canvas.toBlob((blob) => { ... });
```

The `encodeCanvas()` function in `storyCardGenerator.ts` uses `toDataURL` + manual byte conversion to produce both `blob` and `base64` in one shot.

---

## TypedArray Polyfill (Android 11 / Chrome WebView 90)

`TypedArray.prototype.at` is polyfilled in `main.tsx` for all 9 typed array types.
Chrome WebView 90 / Android 11 lacks this method natively.

---

## See also

- [[User Preferences & Style]]
- [[Agent Quick Reference]]
- [[Critical Gotchas]]
- [[🏠 Home]]
