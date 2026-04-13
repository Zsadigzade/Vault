---
tags: [features, share, social, create, instagram]
area: features
updated: 2026-04-03
---

# Share Card System

> [!note] **Implementation deep-dive** (encode rule, presave flow, piggybacking): [[Share Card & Presave]]. This note covers the **product/UX** side.

---

## What It Does

When a user posts, BRUH generates a branded image card and shares it to Instagram Stories (or any share sheet target). The card shows the meme prompt in BRUH's visual style.

---

## CreateScreen Flow

```
User types prompt
  └─ Card presaved in background (100ms debounce)

User taps "Publish + Copy Link"
  └─ await createPost()          ← post created first
  └─ Copy link to clipboard
  └─ Step 1 → Step 2 transition

User taps "Share to Instagram"
  └─ Share.share({ url: presavedCardUri })   ← near-instant, card already ready
```

---

## Visual Design

- Template: `posting.png` (background image)
- Card size: 540×960 native, 1080×1920 web
- Encodes to JPEG via `canvas.toDataURL()` — synchronous, avoids Android WebView callback delays
- IG-style gradient + BRUH branding applied to canvas

---

## Two Steps in CreateScreen

| Step | Action | Visual cue |
|------|--------|-----------|
| **Step 1** | Publish + copy link | Button turns emerald when link copied |
| **Step 2** | Share card to Instagram/Stories | `SocialShareButton` with brand gradient |

Tour flow: `create-input` → `create-challenges` → `create-step-link` → `create-step-share`

> [!note] Step panels use **title only** — no subtitle paragraphs under them. See [[Coding Patterns & Preferences]] (UI/copy style).

---

## Duplicate Post Prevention

Before posting, `createPost()` checks for an existing active post with the same question (`.ilike`, case-insensitive). Returns `{ id: null, error: "..." }` if duplicate found — no share sheet opens.

---

## Social Share Button (`SocialShareButton`)

- Variants: `lg` / `sm` sizes, optional `stepIndex` prop (for Create tour step highlight)
- STAGES animation matches the IG gradient palette
- Used in CreateScreen Step 2

---

## See also

- [[Share Card & Presave]] — implementation: encode, presave, piggyback, canvas resolution
- [[App Architecture]] — CreateScreen layout, `max-w-app-story`, `create-card-ig-ring`
- [[Decision Log]] — why `toDataURL` over `toBlob`
- [[Coding Patterns & Preferences]] — UI copy style, step panel design
- [[🏠 Home]]
