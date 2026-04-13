---
tags: [meta, vault-updates, improvements]
area: meta
updated: 2026-04-14
---

# Vault Updates Summary

> [!success] The Obsidian vault is structured for **autonomous AI agent operation** — reference docs plus **enforcement** and **session state**.

> [!note] **Older changelog:** **`[ARCHIVE]/`** removed **2026-04-13**. Pre-2026-04-13 digest tables → [[Vault history — archived changelogs]]. Use **Git** for line-level history.

> [!tip] **Token discipline:** [[SESSION_HANDOFF]] stays **short**; optional [[SESSION_HANDOFF — Extended 2026-04]]. Chat perf detail → [[Chat System — Performance]] (not duplicated in [[Chat System]]).

---

## 2026-04-14 — shadcn/ui MCP for Cursor (installed)

| Topic | Notes |
|-------|--------|
| **CLI** | `npx shadcn@latest mcp init --client cursor` — merges **`shadcn`** into **`.cursor/mcp.json`** (`npx` + `shadcn@latest mcp`). |
| **BRUH repo** | `Zsadigzade/BRUH` **`.cursor/mcp.json`** includes **`shadcn`**; enable in Cursor **Settings → MCP**. |
| **Vault** | [[12 - MCP & External APIs]] (table + init callout) · [[Cursor Tips & Power Features]] (§ shadcn/ui MCP) · [[MCP Server Patterns]] · [[Component & motion libraries — compact]] · [[Design Systems & Component Patterns]] `## See also` |

---

## 2026-04-13 — Compact agent sheets + changelog archive split

| Topic | Notes |
|-------|--------|
| **New notes** | [[Agent spine — minimal tokens]] · [[Component & motion libraries — compact]] · [[Token & context habits — compact]] · [[Developer utilities — compact]] |
| **Archive** | [[Vault history — archived changelogs]] — tables **2026-04-05**–**07** moved out of this summary |
| **Wiring** | [[📚 Knowledge Base]] (KB 01 / 05 / 09) · [[🏠 Home]] · [[AGENT_READ_ORDER]] · [[Agent Quick Reference]] · [[Agent tag conventions]] (`agent:minimal`) · [[SITEMAP]] · [[Developer design inspiration & motion tools]] `## See also` |

---

## 2026-04-13 — Claude Skills removed from vault → Git + README index

| Topic | Notes |
|-------|--------|
| **Vault** | Deleted **`claude-skills-main/`**; replaced with [[Claude Skills Library (local)]], [[Claude Skills Library — compact index]] (stub), [[External Git playbooks — README index]]. |
| **BRUH** | `.cursor/rules/claude-skills-library-router.mdc` — default local clone **`%USERPROFILE%\Desktop\claude-skills`**. |
| **Design** | New [[Developer design inspiration & motion tools]] (Godly, Unicorn Studio, Spline Community, React Bits + similar). |
| **Graph** | `.obsidian/graph.json` — color groups for `09 - Cursor Plans/`, `12 - MCP…/`, `14 - Personal…/`, `attachments/`, `BRUH_HOME`, root **13 Tombstones**. |
| **Tags** | [[Agent tag conventions]] + `agent:hub` / `agent:entry` / `agent:router` on hub notes. |

---

## 2026-04-13 — Vault lean pass (deleted low-signal bulk)

| Topic | Notes |
|-------|--------|
| **`[ARCHIVE]/` removed** | Entire folder (~42 files): archived Cursor `.plan.md` exports + index, generic KB link dumps, Vault Changelog Archive, README. **Use Git + [[SESSION_HANDOFF]]** instead. |
| **`src/` under vault removed** | Stray `First Vault/src/.../AdminContact.tsx.md` tree — not wiki content. |
| **Docs rewired** | [[🏠 Home]], [[SITEMAP]], [[📚 Knowledge Base]], [[Agent Quick Reference]], [[SESSION_HANDOFF]], [[09 - Cursor Plans/README]], [[How to Use This Vault]], [[AGENT_READ_ORDER]], [[Vault link model]]; KB 09 [[Developer Workflow Tools]] / [[Growth & Launch Toolkit]] — dropped links to deleted notes. |
| **Superseded** | **`claude-skills-main/`** later **removed** — see **2026-04-13 — Claude Skills removed from vault** above. |

---

## 2026-04-13 — Extensionless files & link model

| Topic | Notes |
|-------|--------|
| **Inventory** | No extensionless files under `First Vault/` (excl. `.obsidian`). Only `.md` + (formerly) `.gitkeep`. |
| **[[About attachments]]** | New note in `attachments/`; removed `.gitkeep` so folder stays in Git via the `.md` file and joins graph. |
| **[[Vault link model]]** | Documents why **full pairwise** linking of all notes is not used; hubs + spine + bundle footers instead. Linked from [[🏠 Home]], [[SITEMAP]], [[MOC — BRUH product]]. |

---

## 2026-04-13 — Obsidian graph (link coverage)

| Topic | Notes |
|-------|--------|
| **`claude-skills-main/`** (historical) | Footers were added then folder **deleted** — use **Git clone** per [[Claude Skills Library (local)]]. |
| **Active notes (had zero `[[wikilinks]]`)** | [[Keyboard & Layout]] · [[i18n]] · [[Deploy Targets]] — `## See also` → MOC, Home, SITEMAP, related notes. |
| **Archived plans (later deleted)** | Same footers were added **2026-04-13 AM**; folder **`[ARCHIVE]/`** removed **2026-04-13 PM** — see lean pass above. |
| **Other stragglers (earlier pass)** | [[14 - Personal & Other Projects/README]]; [[Note Template]] linked from [[How to Use This Vault]] + [[MOC — BRUH product]]. |
| **Verify** | Full vault scan: **0** markdown files without any `[[...]]` wikilink. |

---

## 2026-04-13 — Non-markdown inventory (agent-facing vault)

| Finding | Action |
|---------|--------|
| **`claude-skills-main/`** | **Removed from vault** — use Git (see newer changelog section). |
| **Root `claude-skills-main.zip`** | **Removed** earlier — duplicate archive. |
| **`.obsidian/`** (~10 files: `*.json`, theme `manifest.json` / `theme.css`) | **Do not delete** — Obsidian app config and themes; not for LLM context, required for the editor. |
| **`attachments/`** | Note [[About attachments]] replaces `.gitkeep` for Git + graph. |

If the vault feels large, check **`.obsidian`** cache; playbook bulk now lives in a **separate Git clone**, not the vault.

---

## Earlier vault changelog (moved)

> Dated tables **2026-04-05**–**2026-04-07** → [[Vault history — archived changelogs]]. **Agents:** skip unless tracing history.

---

## How to Maintain This Vault

### After Major Changes
1. Update relevant `.md` file directly
2. Link from Home/Agent Reference if first-time feature
3. Note the date in frontmatter (`updated: YYYY-MM-DD`)
4. Keep external memory in sync (`.claude/projects/.../memory/` files)
5. Large historical digests → **recent** dated section here; older blocks → append [[Vault history — archived changelogs]]

### When Creating New Sub-Agent
```
1. [[Agent Quick Reference]] — TL;DR + when-to-read-what
2. [[User Preferences & Style]] — how you like code written
3. [[🏠 Home]] — full note map
```

---

## Vault Stats (2026-04-13 snapshot)

| Metric | Count / note |
|--------|----------------|
| Total `.md` files in vault (approx.) | **~180** BRUH + KB (+ meta) — **no** claude-skills tree |
| Git clone (outside vault) | Optional **`Desktop\claude-skills`** for playbooks |
| `KB 01`–`KB 09` topic files | **~74** |
| Meta (`00 - Meta/`) | Grew — MOCs, [[Vault link model]], etc. |
| **`[ARCHIVE]/`** | **Removed** |
| Cursor plans | **`09 - Cursor Plans/README`** only — no `.plan.md` in vault |

---

## See also

- [[Vault history — archived changelogs]] — older dated tables
- [[🏠 Home]] — main entry point
- [[Agent Quick Reference]] — agent TL;DR
- Root **`CLAUDE.md`** — canonical project rules
- `.claude/projects/.../memory/MEMORY.md` — external memory index
