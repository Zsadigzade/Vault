---
tags: [meta, agents, taxonomy, obsidian, agent:router]
area: meta
status: stable
updated: 2026-04-13
---

# Agent tag conventions (Obsidian frontmatter)

> Use **`tags:`** in YAML so **Obsidian Graph → show tags** stays useful. Agents can grep `agent:` / `topic:` to route.

## Prefixes

| Prefix | Meaning | Examples |
|--------|---------|----------|
| **`agent:entry`** | Read first in a session | `agent:entry` on [[SESSION_HANDOFF]] |
| **`agent:hub`** | Map / index — fan out to topic notes | `agent:hub` on [[🏠 Home]], [[📚 Knowledge Base]] |
| **`agent:router`** | When-to-read-what / shortcuts | `agent:router` on [[Agent Quick Reference]], [[AGENT_READ_ORDER]], playbook index notes |
| **`agent:topic`** | Domain slice for one class of tasks | `agent:topic` on deep KB notes |
| **`agent:minimal`** | Token-light: spine, habits, or archive — **skip** unless needed | [[Agent spine — minimal tokens]], [[Token & context habits — compact]], [[Vault history — archived changelogs]] |
| **`topic:*`** | Fine-grained filter | `topic:design-inspiration`, `topic:security` |

## Existing tags

Keep **`area:`** (`meta`, `architecture`, `knowledge-base`, …) and **`status:`** (`active`, `stable`) — already in vault.

## Graph colors

Folder-based **color groups** live in `.obsidian/graph.json` (`path:"KB 01 - Design & UI"`, …). Tags complement colors; they do not replace path groups.

## See also

- [[Vault link model]] · [[SITEMAP]] · [[How to Use This Vault]]
