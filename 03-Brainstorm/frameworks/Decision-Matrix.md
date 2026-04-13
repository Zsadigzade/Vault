---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Weighted criteria; CFO weights cost, CISO weights risk."
---

# Decision Matrix (agent-executable)

## TL;DR

Weighted criteria scoring; CFO weights cost 1.5×, CISO weights risk 1.5×. Sensitivity check prevents false precision.

## When to use

When you have 3–6 options and need a defensible, documented choice. After [[SCAMPER]], [[Idea-Matrix]], or [[Double-Diamond]] has generated options. Not for binary decisions (use [[First-Principles]] instead).

## Agent instructions

1. List all options (minimum 2, maximum 6).
2. Define criteria — always include: **impact**, **cost**, **risk**, **time-to-value**, **reversibility**.
3. Assign weights (must sum to 10). Apply role multipliers: [[CFO]] weights cost, [[CISO]] weights risk.
4. Score each option on each criterion: 1 (poor) → 5 (excellent).
5. Calculate weighted total: `sum(score × weight)` per option.
6. Run sensitivity: what single weight change flips the winner?

## Default criteria and weights

| Criterion | Default weight | Role multiplier |
|-----------|---------------|----------------|
| Impact | 3 | — |
| Cost | 2 | 1.5× if [[CFO]] involved |
| Risk | 2 | 1.5× if [[CISO]] involved |
| Time-to-value | 2 | — |
| Reversibility | 1 | 1.5× if [[CTO]] involved |

## Output template

```markdown
## Options
1. [Option A]
2. [Option B]
3. [Option C]

## Weights (must sum to 10)
| Criterion | Weight | Assigned by |
|-----------|--------|------------|
| Impact | 3 | CEO |
| Cost | 2 | CFO |
| Risk | 2 | CISO |
| Time-to-value | 2 | COO |
| Reversibility | 1 | CTO |

## Scoring (1=poor, 5=excellent)
| Option | Impact×3 | Cost×2 | Risk×2 | Time×2 | Reversibility×1 | **Total** |
|--------|---------|--------|--------|--------|----------------|----------|
| A |  |  |  |  |  | |
| B |  |  |  |  |  | |
| C |  |  |  |  |  | |

## Winner
**[Option X]** with score [Y/50]

## Sensitivity check
If [criterion] weight changes from [W] to [W+2], winner changes to [Option Z].
→ This means the decision hinges on [what to investigate further].

## Recommendation
[One sentence: what to do and why the matrix supports it]

## Dissent
[Any role that disagrees with weighting or result — document, don't suppress]
```

## Role assignments

- **[[CFO]]** — owns cost and budget criteria weights
- **[[CISO]]** — owns risk criteria weight
- **[[CTO]]** — owns reversibility and technical feasibility
- **[[CoS]]** — runs the matrix and reports winner + sensitivity

## After session

→ [[Synthesis-Protocol]] to finalize decision and write handoff. Store in `03-Brainstorm/sessions/`.
