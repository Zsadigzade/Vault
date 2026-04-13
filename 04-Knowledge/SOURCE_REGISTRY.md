---
tags: [sources, registry, agents]
area: knowledge-base
updated: 2026-04-13
tldr: "Trusted feeds/domains; tier sets automation aggressiveness."
---

# Source registry

## Trusted tier A (structured capture → inbox, still human promote)

- Add RSS/Atom URLs or domains below as bullets with `tier: A` comment in your editor.

## Tier B (inbox only, no auto-summary without human)

- Default for new sources until reviewed.

## Citation rule

Every capture uses block from `_Sources/CITATION_BLOCK.md`.

## Example entries

```yaml
- id: example-blog
  url: https://example.com/feed.xml
  tier: B
  notes: "Verify license before summarizing"
```
