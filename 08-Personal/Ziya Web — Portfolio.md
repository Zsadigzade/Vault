---
tags: [personal, web, nextjs, portfolio, zsadigzade]
area: personal-web
status: active
updated: 2026-04-07
---

# Ziya Web — personal portfolio

Immersive single-page portfolio for **Ziya Sadigzade**. Separate from the **BRUH** app repo; no shared codebase.

## Locations

| Item | Value |
|------|--------|
| Local path | `C:\Users\zsadi\Desktop\Ziya_Web` |
| GitHub | `Zsadigzade/Ziya_Web` — https://github.com/Zsadigzade/Ziya_Web |
| Production | https://zsadigzade.com |
| Alternate hostnames | `ziya-web-five.vercel.app` (Vercel alias) — use **custom domain** as canonical |

## Hosting & DNS

- **App platform:** Vercel (project **ziya-web**, Git-connected to `Ziya_Web` repo on **`master`**).
- **Registrar / DNS:** GoDaddy.
- **Apex record:** `A` **`@`** → IP shown in **Vercel → Project → Domains** for `zsadigzade.com` (e.g. `216.198.79.1` — Vercel may rotate; **always match the dashboard**).
- **`www`:** If added in Vercel, use the **CNAME** value Vercel shows (e.g. `cname.vercel-dns.com`).
- **SSL:** Issued by Vercel after DNS validates; if **HTTP-01** fails, check GoDaddy **Website Builder / forwarding** off and no conflicting **AAAA** / **CAA**.

Local link file: repo root **`.vercel/project.json`** (folder **`.vercel/`** is gitignored).

## Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 16 (App Router), React 19, TypeScript |
| Styling | Tailwind CSS v4 |
| Motion | GSAP + ScrollTrigger, Lenis (smooth scroll), Framer Motion (loader / small UI) |
| 3D | three.js, `@react-three/fiber`, `@react-three/drei`, `@react-three/rapier` (skills scene) |
| Email (contact) | Resend via `src/app/api/contact/route.ts` |
| Fonts | Inter, Space Grotesk, IBM Plex Mono (via `next/font`) |

## Environment (contact form)

Copy **`.env.example`** → **`.env.local`** (not committed):

| Variable | Purpose |
|----------|---------|
| `RESEND_API_KEY` | Resend API key |
| `CONTACT_TO_EMAIL` | Inbox for submissions |
| `CONTACT_FROM_EMAIL` | Verified sender (e.g. `Portfolio <mail@yourdomain.com>`) |

Without keys, API returns success in **demo mode** (no email sent).

## Source-of-truth toggles (`src/lib/constants.ts`)

| Constant | Role |
|----------|------|
| `SITE.url` | Canonical URL for metadata / Open Graph — keep aligned with **zsadigzade.com** |
| `SHOW_ABOUT_PHOTO` | **`false`** = hide About photo column until a real image is ready; set **`true`** to restore the frame layout |

## Product / UX notes (2026-04)

- Site **does not** show hosting vendor branding in the footer (intentional).
- **Resume / CV** download control removed from Contact; re-add later if needed.
- Visual direction: warm near-black background, muted teal accent, terracotta for primary CTAs, mono **eyebrow** labels — avoid default “AI slop” gradients and heavy glass.

## Commands

```bash
cd C:\Users\zsadi\Desktop\Ziya_Web
npm install
npm run dev
npm run build
npm run lint
```

Deploy: push **`master`** → Vercel production build (if Git integration is connected).

## See also

- [[🏠 Home]] — BRUH hub (this project is **not** BRUH)
- [[Vault Updates Summary]] — vault changelog row for this note
- [[SITEMAP]] — folder **`14 - Personal & Other Projects/`**
