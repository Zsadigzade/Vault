---
tags: [architecture, keyboard, layout, android, capacitor]
area: architecture
updated: 2026-04-13
---

# Keyboard & Layout

## The One Rule

> [!warning] CRITICAL — Never change these settings
> `windowSoftInputMode="adjustNothing"` in `AndroidManifest.xml`
> `Keyboard.resize: 'none'` in `capacitor.config.ts`
> The WebView **does NOT resize** when the keyboard appears. CSS + `--kbd-h` handles everything.

> [!note] **Chat thread (`ChatThread`)** — On some Android WebViews, **`100dvh`** can **shrink** when the keyboard is open. Putting **`padding-bottom: var(--kbd-h)`** on the **same** full-screen flex root **adds** to that shrink → large **gap** between composer and keyboard. **Fix in repo:** keep the thread column **without** root `--kbd-h` padding; **`position: fixed`** composer with `bottom: var(--kbd-h)` + horizontal `env(safe-area-inset-*)`; message scroller gets **static `pb`** to clear the composer height (+ safe area).

---

## Configuration

**`android/app/src/main/AndroidManifest.xml`**:
```xml
android:windowSoftInputMode="adjustNothing"
```

**`capacitor.config.ts`**:
```ts
Keyboard: {
  resize: KeyboardResize.None,  // 'none'
  style: KeyboardStyle.Dark,
}
```

---

## CSS Variable `--kbd-h`

Tracks keyboard height in pixels. Updated via Capacitor Keyboard plugin events.

```css
/* Use this to push content above keyboard */
padding-bottom: var(--kbd-h, 0px);

/* Inset goes on the OUTER flex column, not inner scroller */
.outer-flex-col {
  padding-bottom: var(--kbd-h, 0px);
}
```

> [!warning] The inset must be on the **outer** flex column, NOT the inner scrollable container. Getting this wrong causes content to be hidden behind the keyboard.

---

## BottomNav Behaviour

- BottomNav is `absolute z-50` positioned
- It **unmounts** while the keyboard is open
- This prevents the nav from being pushed up by keyboard height changes
- Re-mounts when keyboard dismisses

---

## Index Layout

```
Index.tsx padding-bottom: calc(4.75rem + safe-area)   ← when keyboard hidden
                         0                              ← when keyboard visible (BottomNav gone)
```

---

## Anti-Patterns — Never Do

| Anti-pattern | Effect | Fix |
|---|---|---|
| `Keyboard.resize: 'body'` | Resizes entire WebView — breaks layout avoidance | Use `'none'` |
| `adjustPan` | Pans viewport — unpredictable layout | Use `adjustNothing` |
| `adjustResize` | Resizes WebView — breaks shell | Use `adjustNothing` |
| Inset on inner scroller | Content shifts inside scroll area | Move inset to outer flex column |
| Hardcoded `padding-bottom` near keyboard | Doesn't respond to keyboard state | Use `--kbd-h` var |

---

## Keyboard Event Sequence (Android)

```
User taps input
  → Keyboard.willShow fires → --kbd-h set (initial height)
  → Keyboard.didShow fires → --kbd-h refined (final IME height — use for gap-free dock)
  → Keyboard shown
  → BottomNav unmounts (Index tab shell only)

User dismisses keyboard
  → Keyboard.willHide fires → --kbd-h set to 0
  → Keyboard hidden
  → BottomNav remounts
```

---

## Safe Area Insets

Bottom safe area (iPhone home indicator, Android gesture bar) must be added separately:
```css
padding-bottom: calc(var(--kbd-h, 0px) + env(safe-area-inset-bottom));
```

The `4.75rem` in Index.tsx accounts for BottomNav height + safe area.

---

## MemeReplyPicker Keyboard Avoidance

`MemeReplyPicker` uses a specific pattern for keyboard avoidance that differs from the general rule:

```tsx
// ✅ Correct — paddingBottom on inner content div with transition-none
<div style={{ paddingBottom: keyboardHeight }} className="transition-none">
  <Grid className="transition-none" />
  comment input
</div>

// ❌ Wrong — do NOT put paddingBottom on the outer sliding motion.div
<motion.div style={{ paddingBottom: keyboardHeight }}>  // breaks animation
```

Also: `scrollIntoView({ behavior: "instant" })` (not `"smooth"`) on comment input focus — avoids janky scroll animation while keyboard is opening.

---

## ChatThread (reference) — verified pattern

- **List:** `data-chat-thread-scroll` on the message scroller; bottom padding **`calc(5.5rem + env(safe-area-inset-bottom) + var(--kbd-h))`** so scroll height clears **composer + keyboard** (`adjustNothing`).
- **Composer:** fixed wrapper `bottom: var(--kbd-h)`; inner wrapper **`data-chat-composer`**. `ChatInput`: when keyboard open, **no** `env(safe-area-inset-bottom)` on footer (`pb-0`) — avoids double-count with Android `--kbd-h`.
- **Scroll:** `scrollTo({ top: scrollHeight })` — not `scrollIntoView` (scrollport extends behind keyboard).
- **On keyboard open:** scroll list with **`behavior: 'auto'`** — smooth scroll was firing **after** the 500 ms `_kbdTransitioning` guard and triggered global **scroll → blur** (see below).
- **Global `dismissKeyboardOnScroll` (`App.tsx`):** if focused element is inside **`[data-chat-composer]`** and the scroll event target is **`[data-chat-thread-scroll]`**, **do not blur** — composer is not a descendant of the list.
- **`kbd-change`:** thread scrolls to bottom when keyboard opens (from 0); `keyboardOpen` prop drives `ChatInput` padding.

---

## See also

- [[App Architecture]] · [[Chat System]] · [[Critical Gotchas]]
- [[MOC — BRUH product]] · [[🏠 Home]] · [[SITEMAP]]
