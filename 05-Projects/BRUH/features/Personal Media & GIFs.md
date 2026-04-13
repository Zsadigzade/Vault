---
tags: [features, media, gifs, stickers, indexeddb]
area: features
updated: 2026-04-06
---

# Personal Media & GIFs

> [!note] Premium **cloud** stickers: `user_saved_stickers` + RLS `get_my_user_id()`. **Local** animated GIFs: IndexedDB + `frameData` playback.

---

## GifBrowserSheet (`src/components/GifBrowserSheet.tsx`)

- Entry: **RepliesInbox** “browse GIFs” — portaled sheet; tabs **Trending / Stickers / My Own**.
- **Stacking:** sheet uses **`z-[60]`** so it sits **above** main **BottomNav** (`z-50`) — users cannot switch tabs until the sheet is closed.
- **My Own (premium):** gradient **Create GIF / Create sticker** cards (icons); personal GIFs **3-column** grid; personal stickers via **`StickerScrollGrid`**; **Manage** → `/personal-media`.
- **Inline ads (non-premium, not ad-free):** **GIF** trending + **GIF** search grids use **`InlineSquareAd`** (~13% `pickAdSlots`, min gap 3); sticker search uses **`StickerScrollGrid` `showAds`**; sticker **categories** → **`InlineWideAd`** every 4th block. See [[Monetization]].
- **Backdrop:** not tap-to-close — X, drag, or Android back only (`shellBackCoordinator` in repo).

---

## Local animated GIFs (`saveAnimatedGif` / IndexedDB)

- **`LocalMedia`:** stores **static** `dataUrl` (first frame) + **`frameData`** JSON for animation.
- **Grid / preview:** use **`GifPlayer`** when `isAnimated && frameData`; plain `<img src={dataUrl}>` shows **still** only.
- State pattern: `previewUrl` + **`previewFrameData`**; **`clearPreview()`** on dismiss / sheet reopen / Android back.
- **MemeReplyPicker** **My Own** tab (premium): **parity with GifBrowserSheet** — same gradient create cards, **3-col** GIF grid, **`StickerScrollGrid`** for stickers, saved packs **`grid-cols-4 gap-2`**. `GifPlayer` for animated local GIFs.

---

## MIME allowlist (`personalMedia.ts`)

Allowed before upload: `image/gif`, `image/png`, `image/jpeg`, `image/webp`.

---

## Public URL property

Supabase SDK returns **`publicUrl`** (camelCase) — not `publicURL`.

---

## Related UI

- **Post detail / inbox:** expired reply sentinel `REPLY_MEME_EXPIRED_SENTINEL` (`[expired]`) — [[Database Reference]], [[Reply System]].
- **Trending:** exclude `/personal/` URLs from public trending where implemented (`trending.ts`).

---

## See also

- [[App Architecture]] (sheet portal pattern)
- [[Reply System]]
- [[Monetization]] (premium)
- [[Database Reference]]
- [[🏠 Home]]
