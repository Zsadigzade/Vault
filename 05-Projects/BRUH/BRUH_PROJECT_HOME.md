---
tags: [home, index, cheatsheet, agent:hub]
area: meta
updated: 2026-04-13
aliases: ["🏠 Home", "HOME", "BRUH Home"]
---

# BRUH — Project Home

> [!tip] Agents: [[SESSION_HANDOFF]] → [[CONSTITUTION]] (read-only) → [[Agent Quick Reference]] (or faster [[Agent spine — minimal tokens]]) → topic table below. **MCP:** you may use enabled tools to **verify live APIs/ops** anytime — [[Agent MCP — live verification]] · [[12 - MCP & External APIs]].

---

## Identity

| Key | Value |
|-----|-------|
| App name | **BRUH** |
| Tagline | Cross-platform social meme-reply app |
| Platforms | iOS · Android · PWA |
| iOS Bundle ID | `app.bruhsocial.app` |
| Android Package | `com.bruh.app` (in `build.gradle`, NOT capacitor.config.ts) |
| Capacitor appId | `app.bruhsocial.app` (matches iOS only) |
| iOS Team ID | `39FVY58F26` |
| Capgo App ID | `com.bruh.app` |
| GitHub repo | `Zsadigzade/BRUH` |
| Shipped app semver | `1.1.24` (`BRUH/package.json` on disk — Capgo OTA may differ until sync) |

---

## Service URLs

| Service | URL | Hosted on |
|---------|-----|-----------|
| Main app | `bruhsocial.app` | Vercel (`landing/` · project `landing` · auto-deploy `main`) |
| Landing / share | `share.bruhsocial.app` | Vercel (same project alias) |
| Ops admin | `admin.bruhsocial.app` | Vercel (`admin-web/`) |
| Analytics dashboard | `analytics.bruhsocial.app` | Vercel (`dashboard/`) |
| Supabase project | `gpainqlxdakaczkgozko` · West EU (Ireland) | Supabase |
| PostHog | `https://eu.posthog.com` (EU region) | PostHog EU |

### Other web properties (not BRUH)

| Site | URL | Repo / notes |
|------|-----|----------------|
| Personal portfolio | https://zsadigzade.com | `Zsadigzade/Ziya_Web` · local `Desktop\Ziya_Web` · detail [[Ziya Web — Portfolio]] |

---

## Most-Used Commands

```bash
npm run dev
npm run build
npx supabase ...                     # always npx (Windows EPERM); Netlify fully removed
npx cap sync
npm run cap:sync:ios                 # iOS: includes NativeAd packageClassList fix
npx vitest run src/test/<file>.test.ts
npm run test                         # full Vitest ~155 — only when user asks or broad change
npx npm-check-updates --target minor -u && npm install   # refresh deps within current majors; detail [[Commands & Scripts]] § npm
```

---

## Top 5 Rules (Never Break)

> [!warning] CRITICAL — **canonical list:** [[CONSTITUTION]] (read-only, complete laws). **Fast scan:** identity `getUserId()`; no PostgREST `replies(count)`; keyboard `resize: 'none'` + `adjustNothing`; `await` handlers + `result?.error`; no git commit/push unless user asks. **Tables + examples:** [[Critical Gotchas]].

---

## Agent entry points

| Goal | Start here |
|------|------------|
| Immutable laws (do not edit) | [[CONSTITUTION]] |
| Current session / handoff | [[SESSION_HANDOFF]] (short) · [[SESSION_HANDOFF — Extended 2026-04]] (optional depth) |
| Folder intent map | [[SITEMAP]] |
| BRUH product map (shallow) | [[MOC — BRUH product]] |
| Third-party tools & playbooks | [[MOC — Third-party tools & playbooks]] |
| First pass / rules of the road | [[Agent Quick Reference]] |
| **MCP — live verification (use tools)** | [[Agent MCP — live verification]] |
| User’s style & workflow | [[User Preferences & Style]] |
| “Why did we decide X?” | [[Decision Log]] |
| What broke before | [[Bug History & Lessons]] |
| Dead features / failed experiments | [[13 - Tombstones & Anti-Patterns]] |
| Agent mistake log | [[AGENT_FAILURES]] |
| ASCII hub / `@`-friendly alias (same as this note) | [[BRUH_HOME]] |
| Agent read order (token discipline) | [[AGENT_READ_ORDER]] |
| Minimal token spine (skip heavy hubs) | [[Agent spine — minimal tokens]] · [[Token & context habits — compact]] |
| Tag taxonomy for agents / graph | [[Agent tag conventions]] |
| Obsidian usage | [[How to Use This Vault]] |
| **External KB** (design, security, perf, agents, etc.) | [[📚 Knowledge Base]] |
| How linking works (hubs vs full mesh) | [[Vault link model]] |
| Attachments folder (binaries, no wikilinks) | [[About attachments]] |

---

## Knowledge Base

Stack-wide topics (not BRUH-specific): [[📚 Knowledge Base]] → open **one** KB note per question.

---

## Note index (BRUH + KB markdown notes — count grows with the vault; **Cursor plan exports** removed from vault 2026-04-13 — pointer [[09 - Cursor Plans/README]])

### Meta & guides
| Note | Topic |
|------|--------|
| [[CONSTITUTION]] | Immutable project laws — **agents: read-only** |
| [[SESSION_HANDOFF]] | Active session state — read first, update last |
| [[SITEMAP]] | Semantic folder map (where to look / put notes) |
| [[MOC — BRUH product]] | Shallow map: architecture, DB, security, launch, key features |
| [[MOC — Third-party tools & playbooks]] | Skills bundle, MCP APIs, caveman, curated repos |
| [[Vault link model]] | Extensionless files, attachments, why we use hubs not full graph |
| [[Agent tag conventions]] | `agent:*` / `topic:*` tags + graph color note |
| [[External Git playbooks — README index]] | External repos + README links (claude-skills, caveman) |
| [[AGENT_FAILURES]] | Log of agent mistakes + prevention |
| [[How to Use This Vault]] | Obsidian shortcuts, plugins, folder map |
| [[Agent Quick Reference]] | Agent TL;DR, file map, when-to-read-what |
| [[Agent MCP — live verification]] | **Use MCP tools** to test/verify services; server map + rules |
| [[User Preferences & Style]] | Coding + UI + workflow preferences |
| [[Decision Log]] | Non-obvious decisions |
| [[Vault Updates Summary]] | Recent vault changelog (maintenance) |
| [[Vault history — archived changelogs]] | Older dated tables — **agents skip** unless tracing history |
| [[Agent spine — minimal tokens]] | Ordered reads + default skips |
| [[09 - Cursor Plans/README]] | Cursor plan exports no longer stored in vault (see note) |

### Overview
| [[Project Overview]] | Stack, services |
| [[Launch Checklist]] | TODOs, secrets, App Review |

### Architecture
| [[App Architecture]] | Providers, tabs, shell |
| [[Authentication]] | Two auth paths, `getUserId` |
| [[Data Layer]] | React Query, realtime, cache |
| [[Keyboard & Layout]] | `adjustNothing`, `--kbd-h` |
| [[Startup Sequence & Storage Keys]] | Splash, native storage |
| [[Share Card & Presave]] | Fast share / canvas |
| [[INVARIANTS]] | Logic that must not change without approval |

### Database
| [[Database Reference]] | Tables, RPCs |
| [[Edge Functions]] | All edge functions |
| [[Migrations Log]] | History, drift |

### Security
| [[Security Reference]] | RLS, audit, CSP, secrets names |
| [[Payment Webhook Security]] | RevenueCat webhook |
| [[App Review History]] | Apple 2.1 / 3.1.2 |

### Platforms
| [[iOS & Android]] | Signing, native config |
| [[Deep Links & PWA]] | Universal Links, `u.html`, SW |

### Features
| [[Reply System]] | MemeReplyPicker, native guard |
| [[Chat System]] | 1:1 DMs, native, premium send |
| [[Chat System — Performance]] | Realtime/cache + SQL perf (read only if debugging chat speed) |
| [[Challenges]] | Global challenges |
| [[Regional AI Challenges]] | GNews + Gemini pipeline |
| [[Monetization]] | RevenueCat + AdMob |
| [[Push Notifications]] | FCM |
| [[Share Card System]] | Social share UX |
| [[i18n]] | Languages, keys |
| [[Capgo OTA]] | OTA updates |
| [[Personal Media & GIFs]] | GifBrowserSheet, `frameData` |

### Personal & other projects
| [[14 - Personal & Other Projects/README]] | Folder index for non-BRUH repos |
| [[Ziya Web — Portfolio]] | Next.js portfolio · **zsadigzade.com** · Vercel + GoDaddy |

### Deployment
| [[Commands & Scripts]] | npm, Windows `.bat` |
| [[Deploy Targets]] | Netlify, Vercel, stores, deployment workflows |
| [[Windows Setup & Local Development]] | New machine setup, `.bat` scripts, local dev |
| [[Codemagic CI]] | iOS CI/CD |
| [[VERSION_TRUTH_TABLE]] | Installed dependency versions (ground truth) |

### Operations
| [[Dashboards]] | Ops admin (`admin.bruhsocial.app`) |
| [[Analytics Dashboard]] | CEO / growth (`analytics…`) |
| [[Testing]] | Vitest, mocks |
| [[Sentry]] | Error tracking |
| [[Incident Response & Debugging]] | Common errors, debugging, incident checklist |

### Reference
| [[Critical Gotchas]] | Anti-patterns |
| [[Coding Patterns & Preferences]] | Code patterns |
| [[Bug History & Lessons]] | Incident log |
| [[13 - Tombstones & Anti-Patterns]] | Removed features / failed approaches |
| [[12 - MCP & External APIs]] | MCP wiring, service APIs, quirks (detail) |
| [[caveman]] | Token compression for Claude Code + Cursor — `/caveman`, hooks, statusline |

### Knowledge Base (`04-Knowledge/KB-*` + [[📚 Knowledge Base]])
| Section | Topics |
|---------|--------|
| [[📚 Knowledge Base]] | Index of all KB notes |
| `KB-Design` | Mobile UI, Tailwind, a11y, social patterns |
| `KB-Security` | OWASP Mobile, Supabase hardening, secrets |
| `KB-Performance` | React, Vite, lists, DB, Web Vitals |
| `KB-UX` | Heuristics, onboarding, feeds, notifications |
| `KB-AI` | Cursor, prompts, MCP, skills, Ollama, RAG |
| `KB-TypeScript` | Strict TS, Query, hooks, testing |
| `KB-DevOps` | CI/CD, ASO, releases, flags |
| `KB-Postgres` | Indexes, RLS, realtime, migrations |
| `KB-Resources` | Curated repos, SaaS, devtools, AI/MCP, OSS social, growth |
| `KB-Business` · `KB-Creative-Design` · `KB-Science` · `KB-Productivity` | Strategy, craft, research, personal systems |

---

## See also

- Repo root **`CLAUDE.md`**
- External Claude memory: `.claude/projects/c--Users-zsadi-Desktop-BRUH/memory/MEMORY.md` (index) + **`ops_monitoring.md`** (incident/uptime/MCP — keep detail there, not in `MEMORY.md`)
