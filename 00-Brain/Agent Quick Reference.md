---
tags: [meta, agent, cheatsheet, entry-point, agent:router]
area: meta
updated: 2026-04-14
---

# Agent Quick Reference

> [!tip] **Vault:** [[HOME]] → [[VAULT_CONSTITUTION]]. **BRUH app:** [[SESSION_HANDOFF]] → [[CONSTITUTION]] (read-only) → [[BRUH_PROJECT_HOME]] or [[BRUH_HOME]]. **Multi-domain routing:** [[DISPATCHER]]. End: update [[SESSION_HANDOFF]]. **Live infra:** [[Agent MCP — live verification]]. **Stack KB:** [[📚 Knowledge Base]] (one topic per file). **Routing:** [[AGENT_READ_ORDER]].

> [!note] If you already read [[BRUH_PROJECT_HOME]] identity, URLs, and **Most-Used Commands**, skip to **When to read what** below.

**Repo:** `C:\Users\zsadi\Desktop\BRUH` · `Zsadigzade/BRUH`. **In-repo:** `CLAUDE.md`. **Claude memory:** same-folder `MEMORY.md` (index) + **`ops_monitoring.md`** (uptime/incident/CI/MCP ops — token-light table; avoid duplicating in vault).

---

## Never-break rules (summary)

> BRUH laws: [[CONSTITUTION]] (read-only). Vault laws: [[VAULT_CONSTITUTION]]. One-screen cheat: [[BRUH_PROJECT_HOME]]. Pattern tables: [[Critical Gotchas]].

---

## When to read what

| Task | Open first |
|------|------------|
| **Start / end of session** | [[SESSION_HANDOFF]] |
| **Minimize reads (token spine)** | [[Agent spine — minimal tokens]] · [[Token & context habits — compact]] |
| Immutable laws | [[CONSTITUTION]] (do not edit) |
| Where folders “mean” | [[SITEMAP]] |
| Dependency ground truth | [[VERSION_TRUTH_TABLE]] |
| Fragile sequencing (auth, splash, OTA, push) | [[INVARIANTS]] |
| Before suggesting removed tech | [[13 - Tombstones & Anti-Patterns]] |
| After agent mistakes | Append row to [[AGENT_FAILURES]] |
| Any code change | [[Critical Gotchas]] · [[Coding Patterns & Preferences]] |
| Auth / session | [[Authentication]] · [[Startup Sequence & Storage Keys]] |
| DB / RLS / RPC | [[Database Reference]] · [[Migrations Log]] |
| **Chat slow / realtime** | [[Chat System — Performance]] · [[Chat System]] |
| Edge functions | [[Edge Functions]] · [[Security Reference]] |
| Keyboard / layout | [[Keyboard & Layout]] |
| iOS / Android / links | [[iOS & Android]] · [[Deep Links & PWA]] |
| Payments / subs | [[Monetization]] · [[Payment Webhook Security]] |
| Ads | [[Monetization]] (AdMob section) — repo `memory/ads.md` |
| OTA / Capgo | [[Capgo OTA]] |
| Ops admin | [[Dashboards]] |
| CEO / finance metrics | [[Analytics Dashboard]] |
| AI regional challenges | [[Regional AI Challenges]] |
| Tests | [[Testing]] |
| Errors / Sentry | [[Sentry]] · [[Incident Response & Debugging]] |
| **Production incident / uptime / emergency flags** | Repo `scripts/INCIDENT_RUNBOOK.md` · [[Incident Response & Debugging]] |
| MCP — use tools for live checks | [[Agent MCP — live verification]] · [[12 - MCP & External APIs]] |
| **shadcn/ui registry (Cursor MCP)** | [[Cursor Tips & Power Features]] § shadcn/ui MCP · `mcp init --client cursor` — [[12 - MCP & External APIs]] |
| Token compression / terse mode | [[caveman]] — `/caveman [lite\|ultra]`, `/caveman-commit`, `/caveman:compress <file>` |
| User style / prefs | [[User Preferences & Style]] |
| **Windows setup** | [[Windows Setup & Local Development]] |
| **Deployment checklist** | [[Deploy Targets]] |
| **UI / design patterns** | [[📚 Knowledge Base]] → `KB-Design` — compact [[Component & motion libraries — compact]] |
| **Security (general)** | [[📚 Knowledge Base]] → `KB 02 - Security` (+ project [[Security Reference]]) |
| **Performance (general)** | [[📚 Knowledge Base]] → `KB 03 - Performance` |
| **UX patterns** | [[📚 Knowledge Base]] → `KB 04 - UX` |
| **Cursor / agents / prompts** | [[📚 Knowledge Base]] → `KB 05 - AI & Agent Workflow` |
| **Generic Claude Skills** (Git clone, not in vault) | [[Claude Skills Library (local)]] · [[External Git playbooks — README index]] — clone repo → Read `SKILL.md`; `.cursor/rules/claude-skills-library-router.mdc` (default `Desktop\claude-skills`); Claude marketplace for full package |
| **TypeScript / React patterns** | [[📚 Knowledge Base]] → `KB 06 - TypeScript & React Patterns` |
| **Shipping / ASO / CI** | [[📚 Knowledge Base]] → `KB 07 - DevOps & Shipping` |
| **Postgres / Supabase patterns** | [[📚 Knowledge Base]] → `KB 08 - Postgres & Supabase Patterns` |
| **Curated repos & tools** | [[📚 Knowledge Base]] → `KB 09 - Resources & Tools` — compact [[Developer utilities — compact]] |
| **Personal portfolio** (**zsadigzade.com**, not BRUH) | [[Ziya Web — Portfolio]] · repo `Desktop\Ziya_Web` |

---

## File map (high level)

| Area | Paths |
|------|--------|
| App shell | `src/App.tsx`, `src/pages/Index.tsx`, `src/components/MobileFrame.tsx` |
| User domain | `src/lib/user/` (not `src/lib/user.ts` shim only) |
| Query keys | `src/lib/queryKeys.ts` |
| Native storage | `src/lib/nativeStorage.ts` |
| Consumer admin | Removed from app — use `admin-web/` |
| Landing / share | `landing/` (Vercel — `prj_QQ75DLUaa5ks1Lcois5CFcm141pQ`) |
| Analytics app | `dashboard/` (Vercel) |
| Ops admin | `admin-web/` (Vercel) |
| DB + edge | `supabase/migrations/`, `supabase/functions/` |
| Personal site (separate repo) | `C:\Users\zsadi\Desktop\Ziya_Web` — see [[Ziya Web — Portfolio]] |

---

## Commands (Windows)

Same block as [[BRUH_PROJECT_HOME]] → **Most-Used Commands** (always `npx supabase` / `npx netlify`).

---

## See also

- [[CONSTITUTION]] · [[SESSION_HANDOFF]] · [[SITEMAP]] · [[INVARIANTS]] · [[AGENT_READ_ORDER]] · [[Agent tag conventions]]
- [[Agent MCP — live verification]] · [[BRUH_PROJECT_HOME]] · [[BRUH_HOME]] · [[📚 Knowledge Base]] · [[HOME]]
- [[How to Use This Vault]]
- [[User Preferences & Style]]
- [[Decision Log]]
