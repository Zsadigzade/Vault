---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Two axes; fill grid with combined concepts."
---

# Idea Matrix (agent-executable)

## TL;DR

Two axes; fill every cell with one concrete idea. Forced combination generates non-obvious options.

## When to use

Generating ideas from scratch (unlike [[SCAMPER]] which modifies existing). Best for: new product features × audience segments, channels × messages, solutions × constraints. Forces combinatorial thinking instead of additive thinking.

## When NOT to use

When you already have a clear direction and need to refine. Use [[SCAMPER]] for iteration.

## Agent instructions

1. Choose Axis A and Axis B — each should have 3–5 distinct categories. Don't make them too similar.
2. Fill every cell with one concrete idea (not "explore X" but "build Y that does Z").
3. Mark your top 3 cells with `★` and explain why.
4. Run [[Decision-Matrix]] on the top 3 if you need to pick one.

## Useful axis combinations

| Axis A (rows) | Axis B (columns) | Good for |
|---------------|-----------------|---------|
| User segment | Feature/solution | Product expansion |
| Channel | Message / angle | Marketing strategy |
| Problem severity | User technical level | Product tiering |
| Time horizon | Resource level | Roadmap planning |
| Distribution model | Pricing model | Business model exploration |

## Output template

```markdown
## Setup
**Axis A:** [what rows represent]
**Axis B:** [what columns represent]
**Context:** [what problem are we generating ideas for?]

## Matrix
|          | [Col 1] | [Col 2] | [Col 3] | [Col 4] |
|----------|---------|---------|---------|---------|
| [Row 1]  |         |         |         |         |
| [Row 2]  |         |         |         |         |
| [Row 3]  |         |         |         |         |
| [Row 4]  |         |         |         |         |

## Top 3 cells
| Cell | Idea | Why it wins |
|------|------|-------------|
| ★ [Row X × Col Y] | [concrete idea] | [reason] |
| ★ [Row X × Col Z] | [concrete idea] | [reason] |
| ★ [Row W × Col Y] | [concrete idea] | [reason] |
```

## Role assignments

- **[[CPO]]** — product × segment matrix
- **[[CMO]]** — channel × message matrix
- **[[CEO]]** — market × business model matrix
- **[[CTO]]** — solution × constraint matrix

## After session

→ [[Decision-Matrix]] to score and select top ideas. Store in `03-Brainstorm/sessions/`.
