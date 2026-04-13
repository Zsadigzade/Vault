---
tags: [kb, performance, images, media]
area: knowledge-base
updated: 2026-04-04
---

# Image & media optimization

---

## Formats

| Format | Use |
|--------|-----|
| **AVIF / WebP** | Photos; fallback `picture` or accept Safari tradeoffs |
| **SVG** | Icons, simple illustrations |
| **GIF** | Prefer **video** MP4 for animations when possible (smaller) |

---

## Loading

- **`loading="lazy"`** for below-fold images (web)
- **Dimensions** — set `width`/`height` or aspect box to reduce CLS ([[Core Web Vitals]])

---

## Responsive

- `srcset` + `sizes` for CDN images
- Supabase **Storage transforms** (if enabled) for thumbnails — see [[Supabase Storage Patterns]]

---

## Meme / GIF pickers

- **Thumbnail first** — full resolution on select
- **Decode** large images off main thread where possible (`decode()`)

---

## Video

- **Preload** metadata only unless autoplay required
- **Poster** image for LCP perception

---

## See also

- [[List Virtualization]] (unload off-screen media) · [[Capacitor Native Performance]]
