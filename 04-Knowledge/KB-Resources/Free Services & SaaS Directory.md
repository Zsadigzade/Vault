---
tags: [kb, resources, saas, free-tier]
area: knowledge-base
updated: 2026-04-04
---

# Free services & SaaS directory

> [!warning] **Verify on the vendor site.** Free tiers, quotas, and EU data residency change often. Numbers below are **indicative** for discovery, not contracts.

---

## Auth, backend & database

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Supabase](https://supabase.com/pricing) | Postgres, Auth, Storage, Realtime, Edge Functions | Hobby project limits (DB/storage/API) — check dashboard | BRUH stack default; RLS + RPC patterns |
| [Firebase](https://firebase.google.com/pricing) | Auth, Firestore, FCM, Hosting | Generous free spark quotas; limits per product | Compare push/Auth if evaluating hybrid |
| [PlanetScale](https://planetscale.com/pricing) | MySQL-compatible serverless DB | Free tier evolved — confirm current | Not Postgres; only if stack diverges |
| [Neon](https://neon.tech/pricing) | Serverless Postgres | Free branch + storage limits | Alt hosted Postgres for experiments |

---

## Error tracking & monitoring

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Sentry](https://sentry.io/pricing/) | Errors, performance, replay (product-dependent) | Developer/free event caps | Native + web crash grouping |
| [Better Stack](https://betterstack.com/pricing) | Uptime + logs | Free uptime checks (verify) | Status page + ping |
| [UptimeRobot](https://uptimerobot.com/pricing/) | HTTP/ping monitors | Limited free monitors | Simple uptime |
| [LogRocket](https://logrocket.com/pricing/) | Session replay + frontend logs | Trial / limited free (verify) | Reproducing UI bugs |

---

## Product analytics

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [PostHog](https://posthog.com/pricing) | Events, funnels, feature flags | Generous free tier (verify EU region: `eu.posthog.com`) | BRUH — use EU endpoints for compliance |
| [Mixpanel](https://mixpanel.com/pricing/) | Product analytics | Free tier with MAU caps | Retention / cohort analysis |
| [Plausible](https://plausible.io/) | Privacy-friendly web analytics | Paid cloud; **self-host** open source | Landing/marketing site if avoiding cookies |

---

## Email & transactional

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Resend](https://resend.com/pricing) | Transactional email API | Free monthly send cap (verify) | BRUH edge/cron email |
| [Loops](https://loops.so/pricing) | Product email + marketing | Free tier for small lists (verify) | Lifecycle / onboarding drips |
| [Mailgun](https://www.mailgun.com/pricing/) | Transactional | Trial / limited free (verify) | Alt SMTP/API |

---

## Media, CDN & objects

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Cloudflare R2](https://developers.cloudflare.com/r2/pricing/) | S3-compatible object storage | Free egress to Workers; storage GB-month (verify) | Cheap static/assets vs egress-heavy S3 |
| [Cloudinary](https://cloudinary.com/pricing) | Image/video transform + CDN | Free credits/limits | On-the-fly image variants |
| [imgproxy](https://imgproxy.net/) | Self-host image processing | OSS — pay only hosting | Control + cost at scale |

---

## CI/CD & builds

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [GitHub Actions](https://github.com/pricing) | CI in GitHub | Free minutes for private repos (plan-dependent) | Tests, automations |
| [Codemagic](https://codemagic.io/pricing/) | Mobile CI (iOS/Android) | Free build minutes (verify) | BRUH native builds |

---

## Push notifications

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| **FCM** (Firebase Cloud Messaging) | Mobile push | No per-message charge (Google terms apply) | BRUH native push backbone |
| [OneSignal](https://onesignal.com/pricing) | Push + email orchestration | Free tier with subscriber caps | If delegating delivery UI |

---

## OTA & app delivery

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Capgo](https://capgo.app/pricing) | Capacitor OTA | Free tier / trial (verify) | BRUH OTA path |
| **Microsoft CodePush** (App Center legacy) | Historical OTA | Ecosystem shifted — verify current support | Only if maintaining legacy |

---

## Hosting, DNS & landing

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Netlify](https://www.netlify.com/pricing/) | Static sites, serverless | Free bandwidth/build minutes (verify) | BRUH landing (`share.*`) |
| [Cloudflare](https://www.cloudflare.com/plans/) | DNS, CDN, Workers | Free DNS + basic CDN | DNS + edge workers |
| [Vercel](https://vercel.com/pricing) | Frontend + serverless | Hobby limits | Alt to Netlify for web apps |

---

## Design & assets

| Service | What it does | Free tier (indicative) | When to use |
|---------|--------------|------------------------|-------------|
| [Figma](https://www.figma.com/pricing/) | UI design | Free starter | Mockups, handoff |
| [Excalidraw](https://excalidraw.com/) | Diagrams | Free web + OSS | Architecture sketches |
| [Icons8](https://icons8.com/) / [Lucide](https://lucide.dev/) | Icons | Mixed free/Pro | Marketing + in-app icons |

---

## See also

- [[Curated GitHub Repositories]] · [[Growth & Launch Toolkit]] · [[Security Scanning & Audit Tools]] · [[12 - MCP & External APIs]]
