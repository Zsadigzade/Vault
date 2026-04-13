---
tags: [meta, graph, obsidian, agents, agent:router]
area: meta
status: stable
updated: 2026-04-13
---

# Vault link model

## Extensionless and non-markdown files

**Scan (2026-04-13):** Under `First Vault/` (excluding `.obsidian/`) there are **no extensionless files**. Content is essentially **`.md` notes only**, plus this folder’s **binary attachments** once you add them. The former `.gitkeep` here was replaced by [[About attachments]] so the folder is still tracked and **linked in the graph**.

**`.obsidian/`** holds JSON/CSS for the Obsidian app — **do not** treat as wiki notes or bulk-edit for links.

## “Connect every file to each other” — not the goal

Pairwise linking **all** notes would mean on the order of **millions** of edges (\(N(N-1)/2\) for large \(N\)). That drowns humans and agents in noise.

**Instead — hub-and-spoke:**

1. **Spine:** [[SESSION_HANDOFF]] → [[🏠 Home]] → [[AGENT_READ_ORDER]] → one topic note.
2. **Maps:** [[MOC — BRUH product]] · [[MOC — Third-party tools & playbooks]] · [[SITEMAP]].
3. **External playbooks:** [[Claude Skills Library (local)]] — **Git clone** of alirezarezvani/claude-skills (no vault copy).
4. **Coverage check:** every `.md` should contain at least one `[[wikilinks]]` (automated passes have enforced this where gaps appeared).

From any note, you should reach [[🏠 Home]] in a **small number of hops** by following links — not by direct edges to every other note.

## See also

- [[How to Use This Vault]] · [[Note Template]] · [[Agent tag conventions]]
- [[Claude Skills Library (local)]] · [[09 - Cursor Plans/README]]
- [[About attachments]]
