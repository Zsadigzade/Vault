---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Decompose → challenge assumptions → rebuild minimal solution."
---

# First Principles (agent-executable)

## TL;DR

Decompose → challenge every assumption → rebuild from ground up.

## When to use

When the conventional solution feels expensive, slow, or stuck. When everyone is solving the same problem the same way. Elon Musk used this for battery cost ("what are batteries actually made of and what do those materials cost?"). Works best for technical architecture, pricing models, and product strategy.

## Agent instructions

You are running First Principles reasoning. Go through the 4 steps methodically. Never accept "this is how it's done" as a valid reason. Tag every assumption by type.

## The 4 steps

### Step 1 — State the goal (one sentence)
What outcome are we trying to achieve? Not the solution — the outcome.

### Step 2 — Enumerate assumptions
List every assumption that underlies the current approach. Tag each:
- `[convention]` — "everyone does it this way"
- `[technical]` — "X requires Y"
- `[legal]` — "we must..."
- `[resource]` — "we don't have..."
- `[belief]` — "users want..."

### Step 3 — Invert each assumption
For each assumption: what if it's false? What does the solution look like then?

### Step 4 — Rebuild minimal solution
Given only what's verifiably true, what's the simplest path to the goal?

## Output template

```markdown
## Goal
[One sentence outcome]

## Assumption audit
| Assumption | Type | Inversion | Still holds? |
|------------|------|-----------|-------------|
| [assumption 1] | [tag] | [what if false?] | yes / no / uncertain |

## Ground truths (what's undeniably true)
- [fact 1]
- [fact 2]

## Rebuilt model
[Describe the minimal solution built only from ground truths]

## Tests to validate
| Assumption challenged | Experiment to run | Cost | Timeline |
|----------------------|-------------------|------|----------|
```

## Role assignments

- **CEO / [[CTO]]** — run this on strategic and technical problems
- **[[CFO]]** — use Step 2–3 on pricing assumptions and cost models
- **[[CPO]]** — challenge "users want X" assumptions before building

## After session

→ [[Decision-Matrix]] to evaluate the rebuilt model against alternatives. Store in `03-Brainstorm/sessions/`.
