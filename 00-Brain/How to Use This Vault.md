---
tags: [meta, obsidian, guide]
area: meta
updated: 2026-04-13
agent_priority: human
---

# How to Use This Vault

> [!important] **Agents (Cursor / Claude):** This note is **human-first** (Obsidian UI, graph colors, plugins). For routing and rules, use [[Agent Quick Reference]] + [[🏠 Home]] + [[SESSION_HANDOFF]]. For **live infra / MCP tooling**, see [[Agent MCP — live verification]] — **do not** spend context on sections below unless the user asks about Obsidian itself.

> [!tip] You don't need to learn Obsidian deeply to get value. Use it like a searchable wiki. **Humans:** start at [[🏠 Home]]. **General stack reference:** [[📚 Knowledge Base]].

**New BRUH wiki notes:** duplicate [[Note Template]] (or start from it) so `[[wikilinks]]` connect into the graph — see [[MOC — BRUH product]].

---

## Core Navigation

| Action | Shortcut |
|--------|----------|
| Open any note | `Ctrl+O` (quick switcher) |
| Search all text | `Ctrl+Shift+F` |
| Go back | `Alt+←` |
| Open graph view | `Ctrl+G` |
| Click a `[[link]]` | `Ctrl+Click` (opens in new pane) |
| Create new note | `Ctrl+N` |

---

## Key Conventions in This Vault

### `[[wiki-links]]`
Blue underlined text like `[[Authentication]]` is a clickable link to another note. Click to navigate. In graph view (`Ctrl+G`) you'll see how all notes connect.

### Callout Blocks

> [!warning] Red block = critical rule, never violate
> [!tip] Blue block = best practice or shortcut
> [!note] Grey block = extra context
> [!important] Orange block = must-read section

### YAML Frontmatter
Every note starts with a `---` block. This is metadata — you can filter by `tags` or `area` in Obsidian search. Optional **`status`**: `active` | `stable` | `archived`. Ignore frontmatter if you just want to read.

### Constitution (agents)
[[CONSTITUTION]] is **read-only** for agents — do not edit it. Propose changes to the human instead.

### Tables
Most structured data (secrets, commands, query keys) is in tables for fast scanning.

---

## Recommended Workflow

1. **Always start at [[🏠 Home]]** — IDs, URLs, commands, and top rules are inline
2. **If something goes wrong** → check [[Critical Gotchas]] first
3. **Before touching auth code** → read [[Authentication]]
4. **Before touching DB** → read [[Database Reference]]
5. **Before touching keyboard/layout** → read [[Keyboard & Layout]]
6. **Before a deploy** → read [[Deploy Targets]] + [[Commands & Scripts]]

---

## Vault Folder Map

```
00 - Meta/          ← Constitution (read-only), Session Handoff, **Agent MCP — live verification**, Sitemap, Agent Failures, guides
01 - Overview/      ← stack, services, launch status
02 - Architecture/  ← how the app is built (+ INVARIANTS, Share Card & Presave)
03 - Database/      ← schema, RPCs, edge fns, migrations
04 - Security/      ← RLS, payments webhook, App Review
05 - Platforms/     ← iOS, Android, deep links, PWA
06 - Features/      ← payments, ads, Capgo, regional AI, media
07 - Deployment/    ← how to ship (+ Codemagic, VERSION_TRUTH_TABLE)
08 - Operations/    ← ops admin, analytics app, testing, Sentry
09 - Cursor Plans/  ← README only — plan exports not stored in vault ([[09 - Cursor Plans/README]])
09 - Critical Gotchas.md
10 - Coding Patterns & Preferences.md
11 - Bug History & Lessons.md
12 - MCP & External APIs.md
13 - Tombstones & Anti-Patterns.md
📚 Knowledge Base.md   ← index for external / stack KB (agents: many small topic notes)
KB 01 - Design & UI/
KB 02 - Security/
KB 03 - Performance/
KB 04 - UX/
KB 05 - AI & Agent Workflow/
KB 06 - TypeScript & React Patterns/
KB 07 - DevOps & Shipping/
KB 08 - Postgres & Supabase Patterns/
KB 09 - Resources & Tools/
External playbooks   ← [[Claude Skills Library (local)]] — **Git clone** on Desktop, not in vault
Templates/          ← core Templates plugin → Note Template
attachments/        ← [[About attachments]]
14 - Personal & Other Projects/
```

---

## Graph view colors

Configured in `.obsidian/graph.json` **color groups** (folder paths + `file:` queries for root notes):

| Color role | Folder / note |
|------------|---------------|
| Gray | `00 - Meta` |
| Blue | `01 - Overview` |
| Purple | `02 - Architecture` |
| Green | `03 - Database` |
| Red | `04 - Security` |
| Orange | `05 - Platforms` |
| Cyan | `06 - Features` |
| Yellow | `07 - Deployment` |
| Pink | `08 - Operations` |
| Muted | `Templates` |
| Alert red | `09 - Critical Gotchas` (root) |
| Teal | `10 - Coding Patterns & Preferences` (root) |
| Amber | `11 - Bug History & Lessons` (root) |
| Blue-violet | `12 - MCP & External APIs` (root) |
| Dark slate | `13 - Tombstones & Anti-Patterns` (root) |
| Muted brown | `attachments/` (optional graph group) |
| White (hub) | `🏠 Home` (root) |
| Gold (hub) | `📚 Knowledge Base` (root) |
| Teal-green | `KB 01 - Design & UI` |
| Deep red | `KB 02 - Security` |
| Forest green | `KB 03 - Performance` |
| Orange | `KB 04 - UX` |
| Purple | `KB 05 - AI & Agent Workflow` |
| Bright blue | `KB 06 - TypeScript & React Patterns` |
| Yellow-gold | `KB 07 - DevOps & Shipping` |
| Cyan | `KB 08 - Postgres & Supabase Patterns` |
| Brown / muted | `KB 09 - Resources & Tools` |
| Blue-gray | `09 - Cursor Plans/` |
| Dark teal (folder) | `12 - MCP & External APIs/` (e.g. [[caveman]]) |
| Rose | `14 - Personal & Other Projects/` |
| Sand | `BRUH_HOME` (root) |
| Graphite | `attachments/` |

### If graph folder colors don’t show

Obsidian keeps **two** graph configs:

| File | Used for |
|------|----------|
| `.obsidian/graph.json` | **Global** graph (command palette / some entries) |
| `.obsidian/workspace.json` | **Graph tab** saved in your layout — its own `state` |

A **Graph** tab with `"state": {}` **does not** inherit `graph.json`, so colors look missing even though `graph.json` is correct. This vault copies **`colorGroups` (and matching options) into `workspace.json`** for the open graph tab.

**After editing JSON:** quit Obsidian fully (check Task Manager for a second `Obsidian` process on Windows), then reopen the vault.

**Optional plugin:** [Sync Graph Settings](https://obsidian.md/plugins?id=sync-graph-settings) copies `graph.json` → local graph when you want to avoid hand-editing `workspace.json`.

---

## Recommended community plugins (optional)

| Plugin | Why |
|--------|-----|
| **Dataview** | Query notes by `area` / `tags` in frontmatter |
| **Templater** | Advanced templates (if you outgrow core **Templates**) |
| **Calendar** | Daily notes for session log |

**Core (already useful):** Templates — folder `Templates/` (see `.obsidian/templates.json`), **Daily notes**, **Graph**, **Backlinks**.

**Accent:** `.obsidian/appearance.json` uses red `#ff0000`.

---

## Tips for New Obsidian Users

- **Tags**: Click a tag like `#security` in any note to find all notes with that tag
- **Graph View** (`Ctrl+G`): Visual map of all connected notes — great for understanding relationships
- **Starred notes**: Click the star icon on frequently used notes (they appear in sidebar)
- **Split panes**: Drag a tab to open two notes side by side
- **Back/Forward**: `Alt+←` / `Alt+→` works like browser history

---

## See also

- [[🏠 Home]] · [[📚 Knowledge Base]]
- [[Agent Quick Reference]]
