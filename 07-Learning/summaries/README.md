---
tags: [learning, summaries, agents]
area: learning
updated: 2026-04-13
tldr: "Auto-generated namespace summaries for fast agent orientation. Regenerate weekly."
---

# Namespace Summaries

## Purpose

This folder stores **auto-generated summaries** of each vault namespace. Agents read these summaries for orientation without loading every file in a namespace.

Each summary is ≤200 tokens and covers: what the namespace contains, what changed recently, and what to look for.

## How summaries are generated

The `weekly-health-check` workflow runs this step:
1. Scans each namespace for `updated:` dates in frontmatter
2. Reads `tldr:` fields from all notes
3. Generates a 100-200 token summary per namespace
4. Proposes the summary update to `06-Inbox/pending/` (low-risk auto-merge eligible)
5. Human approves → summary updates here

## Summary index

Summaries are regenerated weekly. Last generation: *(none yet)*

| Namespace | Summary file | Last updated |
|-----------|-------------|-------------|
| `00-Brain/` | [00-Brain-summary.md](00-Brain-summary.md) | — |
| `01-Agents/` | [01-Agents-summary.md](01-Agents-summary.md) | — |
| `02-Workflows/` | [02-Workflows-summary.md](02-Workflows-summary.md) | — |
| `03-Brainstorm/` | [03-Brainstorm-summary.md](03-Brainstorm-summary.md) | — |
| `04-Knowledge/` | [04-Knowledge-summary.md](04-Knowledge-summary.md) | — |
| `05-Projects/` | [05-Projects-summary.md](05-Projects-summary.md) | — |

## Manual generation

```bash
python scripts/vault_health.py --summaries-only
```

## Summary file format

```markdown
---
generated: YYYY-MM-DD
namespace: "00-Brain"
note_count: 19
---

# 00-Brain — Summary

[100-200 token description of what's in this namespace, key files, recent changes]
```
