---
tags: [meta, preferences, style, workflow]
area: meta
updated: 2026-04-06
---

# User Preferences & Style

> [!note] Derived from project rules, `CLAUDE.md`, memory files, and Cursor chat history (Create tab iterations, admin web, security, keyboard, testing policy).

---

## Coding & docs style

| Preference | Detail |
|------------|--------|
| **Minimal copy in UI** | Step panels and flows prefer **titles only** — no long subtitle paragraphs under Create steps. |
| **Compact reference docs** | External memory (`MEMORY.md`) stays **low-token**; deep dives in topic files. Same idea for this vault: tables + callouts, avoid fluff. |
| **Comments** | Avoid **verbose** comments that only narrate obvious code. **Do** add comments when they help agents **track and find** non-obvious flows (keyboard, splash, Capgo, coordinators). |
| **TypeScript / React** | No `import React from 'react'` — use `import type { … } from 'react'`. Data via **React Query** (`useQuery`), not `useState`+`useEffect` for server data. |
| **Query keys** | From `src/lib/queryKeys.ts` — not inline strings (except intentional i18n-dependent keys inside components). |

---

## UI / product preferences

| Preference | Detail |
|------------|--------|
| **Visual iteration** | Frequent tweaks to spacing, typography, touch targets; references to **screenshots** or **Capgo build versions** (e.g. “revert toward 1.00.59”). |
| **Create tab** | **Square** gradient-framed card (`create-card-ig-ring`), **IG-style** purple/magenta/pink accents, `max-w-app-story` column. Prefer **minimal extra copy** (titles/short labels) after layout passes — avoid new subtitle blocks unless needed. |
| **Brand palette** | CSS `--ig-1`…`--ig-4`, `.text-ig-gradient`, `.glow-ig`. Fonts: Plus Jakarta + Bricolage Grotesque variable. |
| **Accessibility** | Viewport allows zoom (`maximum-scale=5`, no `user-scalable=no`). |
| **Premium / paywall** | After onboarding: **non-premium only** — upsell on each main-shell `Index` mount (stagger delay vs rate-us). Details: [[Monetization]] · [[App Architecture]]. |

---

## Workflow preferences

| Preference | Detail |
|------------|--------|
| **Plans** | Often works from **attached plans**; expects agents **not** to edit plan files unless asked. |
| **Memory updates** | Frequently requests **updates to `.claude/.../memory/`** after significant changes. |
| **Tests** | **Targeted** `npx vitest run <path>` while iterating; **full** `npm run test` (~155 tests) **only when explicitly requested** or for large risky refactors. |
| **Git** | **Full control** — agents must **not** commit/push unless the user explicitly asks in that message. `capgo-push.bat` bumps version / uploads OTA but does **not** replace user’s commit workflow. |
| **Secrets** | Do **not** paste secrets into chat or commits; use env / MCP / Supabase secrets. |
| **Production state** | Prefer **MCP or API checks** over guessing — [[Agent MCP — live verification]] · [[12 - MCP & External APIs]] (Supabase, Sentry, PostHog **EU**, etc.). |

---

## Likes

- Fast, visible UI improvements aligned with reference visuals.
- Security-hardening with clear migration + deploy follow-through.
- Idempotent SQL (`DROP POLICY IF EXISTS` where needed for `db push`).
- Clear separation: ops admin vs analytics dashboard vs consumer app.

---

## Dislikes / never do

| Never | Why |
|-------|-----|
| `git commit` / `push` without explicit ask | User owns history. |
| Full test suite after every tiny fix | Noisy and slow — use targeted Vitest. |
| `Keyboard.resize: 'body'` (or `adjustPan` / `adjustResize`) | Breaks keyboard architecture — see [[Keyboard & Layout]]. |
| Fire-and-forget `async` in `onClick` / `onSubmit` | False success UX — see [[Coding Patterns & Preferences]]. |
| Supabase **Database Webhooks** UI for push triggers | Truncates secrets → broken JSON — see [[Bug History & Lessons]]. |
| `netlify api createDnsRecord` for DNS | CLI bug — use REST API — see [[12 - MCP & External APIs]]. |
| PostgREST `replies(count)` embedding | 15–20s RLS disaster — use RPCs. |
| Remove native guard from [[Reply System]] | Replies are **native-only** by design. |

---

## See also

- [[Coding Patterns & Preferences]]
- [[Critical Gotchas]]
- [[Agent Quick Reference]]
- [[🏠 Home]]
