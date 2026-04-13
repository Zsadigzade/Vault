---
tags: [learning, patterns, agents]
area: learning
updated: 2026-04-13
tldr: "Agent-discovered patterns that generalize across projects. Filed here after inbox approval."
---

# Patterns Discovered

## Purpose

This folder stores **generalizable patterns** that agents discovered while working on specific projects. Unlike project-specific notes (which live in `05-Projects/`), patterns here apply across multiple contexts and are worth keeping permanently.

## What qualifies as a pattern

- A solution that worked and **could work again** in a different project
- An anti-pattern (what not to do) that caused a real failure
- A workflow or process improvement that proved durable
- A prompt engineering trick that improved agent output quality

**Does NOT belong here:**
- Project-specific facts (put in `05-Projects/`)
- Generic best practices you could find in a book (put in `04-Knowledge/`)
- One-off observations without repeatable signal

## How patterns get filed here

1. Agent identifies a generalizable pattern during work
2. Agent creates a capture note in `06-Inbox/pending/` with:
   - `proposed_location: "07-Learning/patterns-discovered/[pattern-name].md"`
   - `confidence: [0.0–1.0]`
   - `evidence: [what happened that surfaced this]`
3. Human reviews and approves via `approve_inbox.py`
4. Approved note moves here and is indexed below

## Pattern index

*(Empty — patterns get added here as discovered)*

| Pattern | Domain | First seen | Confidence |
|---------|--------|-----------|-----------|
| — | — | — | — |

## Pattern file format

```markdown
---
tags: [learning, pattern, domain:X]
area: learning
discovered: YYYY-MM-DD
first_seen_in: "05-Projects/[PROJECT]"
confidence: 0.85
source_agent: [role]
---

# Pattern: [Name]

## What it is
[One paragraph description]

## When to apply
[Context that triggers this pattern]

## When NOT to apply
[Context where this doesn't hold]

## Evidence
[What happened that surfaced this — be specific]

## Related
[Links to KB notes, other patterns]
```
