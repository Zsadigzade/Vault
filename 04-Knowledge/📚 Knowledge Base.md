---
tags: [knowledge-base, index, external, agents, agent:hub]
area: knowledge-base
updated: 2026-04-14
---

# Knowledge Base — External reference

> [!tip] **For agents:** **General + stack-tuned** guidance (React 18, TypeScript, Capacitor, Supabase, Tailwind, Vite). **One topic** per question. **BRUH-specific** rules: [[BRUH_PROJECT_HOME]], [[CONSTITUTION]], [[Agent Quick Reference]].

---

## How this relates to project docs

| Layer | Where |
|-------|--------|
| BRUH architecture, DB, deploy | [[BRUH_PROJECT_HOME]] → `05-Projects/BRUH/` (`overview/` … `operations/`, `reference/`) |
| Cursor Plan mode exports | **Removed from vault (2026-04-13).** Git history / local Cursor; [[09 - Cursor Plans/README]]. |
| Cross-cutting patterns & research | **This page** → `04-Knowledge/KB-*` folders below |

---

## KB-Design (was KB 01)

| Note | Focus |
|------|--------|
| [[Mobile Design Principles]] | Touch targets, thumb zones, safe areas |
| [[Tailwind CSS Advanced Patterns]] | Utilities, responsive, `@apply` tradeoffs |
| [[Typography & Readability]] | Scales, line height, mobile reading |
| [[Color & Contrast Accessibility]] | WCAG, dark mode contrast |
| [[Animation & Micro-interactions]] | Motion budget, CSS, lists |
| [[Dark Mode Implementation]] | `class`/`media`, persistence |
| [[Design Systems & Component Patterns]] | Radix, composition, slots |
| [[Social App UI Patterns]] | Feeds, cards, stories, reactions |
| [[Developer design inspiration & motion tools]] | Godly, React Bits, Spline, Unicorn Studio + similar |
| [[Component & motion libraries — compact]] | shadcn, Radix, Framer Motion, Floating UI, carousels — **table** |

---

## KB-Security

| Note | Focus |
|------|--------|
| [[OWASP Mobile Top 10]] | M1–M10 (2024) → Capacitor/React |
| [[Supabase Security Hardening]] | RLS, auth, secrets — see also [[Security Reference]] |
| [[Auth Security Patterns]] | Sessions, JWT refresh, OAuth |
| [[API Security & Rate Limiting]] | Edge Functions, validation, CORS |
| [[Secure Storage on Mobile]] | Preferences vs Keychain, encryption |
| [[CSP & HTTP Header Security]] | CSP, HSTS, WebView |
| [[Dependency & Supply Chain Security]] | npm audit, lockfiles, updates |
| [[Secrets Management Guide]] | Env, CI, Supabase secrets |

---

## KB-Performance

| Note | Focus |
|------|--------|
| [[React Rendering Optimization]] | memo, when not to optimize |
| [[Bundle Size & Code Splitting]] | lazy routes, dynamic import |
| [[Vite Build Optimization]] | chunks, analyze, deps |
| [[Image & Media Optimization]] | WebP/AVIF, lazy, Storage |
| [[List Virtualization]] | Long lists, infinite scroll |
| [[Network & Caching Strategies]] | React Query, HTTP cache |
| [[Capacitor Native Performance]] | Bridge, splash, WebView |
| [[Postgres Query Optimization]] | Indexes, EXPLAIN — see [[Database Reference]] |
| [[Core Web Vitals]] | LCP, INP, CLS in hybrid apps |
| [[Memory Leaks & Profiling]] | React leaks, DevTools |

---

## KB-UX

| Note | Focus |
|------|--------|
| [[Mobile UX Heuristics]] | Nielsen + mobile, Fitts |
| [[Onboarding & First-Run Experience]] | Value-first, permissions |
| [[Loading & Skeleton States]] | Skeletons, Suspense, optimistic |
| [[Error State Design]] | Empty, retry, offline |
| [[Social App Engagement Patterns]] | Feeds, retention loops |
| [[Notification UX Design]] | Timing, grouping, quiet hours |
| [[Accessibility on Mobile (WCAG)]] | Touch a11y, focus, ARIA |
| [[Form Design & Validation]] | Keyboards, inline errors |
| [[Haptic & Native Feedback]] | Capacitor Haptics |
| [[Feed & Infinite Scroll Patterns]] | Pagination UX, scroll restore |

---

## KB-AI

| Note | Focus |
|------|--------|
| [[Cursor Tips & Power Features]] | Composer, @-refs, plans, **shadcn MCP** (`mcp init --client cursor`) |
| *(removed)* Cursor plan index | Vault copy **deleted 2026-04-13** — use **BRUH repo** + [[SESSION_HANDOFF]] for scope; [[09 - Cursor Plans/README]] for note. |
| [[Memory File Best Practices]] | `CLAUDE.md`, `.cursor/rules` |
| [[Context Window Management]] | Token budget, what to paste |
| [[Token & context habits — compact]] | **Table** — one-topic reads, skip lists, `/compact` |
| [[Prompt Patterns for Code]] | Constraints, examples |
| [[AI-Assisted Code Review]] | Security/refactor prompts |
| [[Agent MCP — live verification]] | **Use MCP tools** proactively for live BRUH checks (vault meta) |
| [[MCP Server Patterns]] | Tools vs APIs — [[12 - MCP & External APIs]] |
| [[Rules & Skills Authoring]] | Rules + Agent Skills |
| [[Claude Code CLI Reference]] | Flags, subcommands, env vars (Claude Code CLI) |
| [[Agent Orchestration Patterns]] | Command → Agent → Skill; when to use each |
| [[Multi-Agent-System-Design]] | Dispatcher, handoffs, CoS synthesis (vault roles) |
| [[Local-LLM-Ollama-Patterns]] | Quantization, context, Ollama API, VPS hardening |
| [[Prompt-Engineering-Advanced]] | Structured output, few-shot, CoT, injection hygiene |
| [[RAG-Knowledge-Retrieval]] | Chunking, hybrid search, rerank |
| [[Agent Debugging Strategies]] | Repro, logs, bisect |
| [[caveman]] | Token compression — installed for Claude Code + Cursor |
| [[Claude Skills Library (local)]] | **Git** alirezarezvani/claude-skills — read `SKILL.md` from clone; [[Claude Skills Library — compact index]] |

---

## KB-TypeScript

| Note | Focus |
|------|--------|
| [[TypeScript Strict Patterns]] | strict, branded types |
| [[React Query Advanced Patterns]] | Infinite, optimistic — see [[Data Layer]] |
| [[Custom Hook Patterns]] | Composition, testing |
| [[Error Boundaries & Recovery]] | Boundaries + [[Sentry]] |
| [[Component Composition Patterns]] | Compound components, Radix |
| [[State Management Decision Tree]] | Query vs local vs URL |
| [[Testing Strategies & Patterns]] | Vitest, MSW — see [[Testing]] |
| [[React 18 Concurrent Features]] | `useTransition`, Suspense |

---

## KB-DevOps

| Note | Focus |
|------|--------|
| [[CI-CD Pipeline Best Practices]] | Cache, secrets, parallel |
| [[App Store Optimization (ASO)]] | Keywords, creatives |
| [[App Store Submission Checklist]] | Apple/Google review |
| [[OTA Update Strategies]] | Staged rollout — see [[Capgo OTA]] |
| [[Monitoring & Alerting Playbook]] | Sentry, errors budgets |
| [[Feature Flags & Rollouts]] | Kill switches, experiments |
| [[Release Management]] | Versioning, changelog |

---

## KB-Postgres

| Note | Focus |
|------|--------|
| [[Index Strategy & Types]] | B-tree, partial, GIN |
| [[Query Patterns & Anti-Patterns]] | N+1, pagination, RPCs |
| [[RLS Pattern Library]] | Policies + perf — see [[Security Reference]] |
| [[Edge Functions Patterns]] | Deno, CORS — see [[Edge Functions]] |
| [[Realtime & Subscriptions]] | Channels, when not to use |
| [[Migration Best Practices]] | Idempotent SQL — see [[Migrations Log]] |
| [[Supabase Storage Patterns]] | Policies, signed URLs |

---

## KB-Resources

| Note | Focus |
|------|--------|
| [[Curated GitHub Repositories]] | Awesome lists, stack repos, design system components, token optimization tools |
| [[Free Services & SaaS Directory]] | Free-tier SaaS for indie/mobile (verify pricing) |
| [[Developer Workflow Tools]] | CLI, API clients, extensions, Git hygiene |
| [[AI & Agent Ecosystem]] | MCP repos, Cursor rules, prompt patterns |
| [[Open Source Social Apps]] | OSS social / feed references, eng blogs |
| [[Growth & Launch Toolkit]] | ASO, landing, launch, share cards, legal pointers |
| [[Performance & Debugging Tools]] | Lighthouse, analyzers |
| [[Developer utilities — compact]] | Bundlephobia, caniuse, SVG/image tools — **table** |
| [[Security Scanning & Audit Tools]] | Snyk, ZAP, audit |

---

## KB-Business · KB-Creative-Design · KB-Science · KB-Productivity

| Area | Index |
|------|--------|
| Business / strategy / GTM | [[KB-Business INDEX]] |
| Visual / brand / motion craft | [[KB-Creative-Design INDEX]] |
| Research / systems / behavior | [[KB-Science INDEX]] |
| Personal knowledge / focus | [[KB-Productivity INDEX]] |

---

## See also

- [[BRUH_PROJECT_HOME]] · [[HOME]] · [[Agent Quick Reference]] · [[How to Use This Vault]]
