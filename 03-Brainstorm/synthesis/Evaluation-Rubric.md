---
tags: [brainstorm, synthesis, evaluation, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Score ideas on 5 dimensions before committing. Prevents enthusiasm bias."
---

# Evaluation Rubric (agent-executable)

## TL;DR

- Score ideas on 5 dimensions before committing. Prevents enthusiasm bias.
- Use after any ideation session before [[Decision-Matrix]] for final pick.
- Minimum viable idea: scores 3+ on **Feasibility** and **Evidence** or it goes back to ideation.

## When to use

After generating ideas (SCAMPER, Idea-Matrix, brainstorm session) and before running the [[Decision-Matrix]]. This rubric filters low-quality ideas quickly so you don't waste time scoring 10 options in detail.

## The 5 dimensions

| Dimension | Question | Weight |
|-----------|---------|--------|
| **Desirability** | Do users actually want this? Is there evidence? | 25% |
| **Feasibility** | Can we build/execute this with available resources? | 25% |
| **Viability** | Does this make business sense — does it pay for itself? | 20% |
| **Evidence** | How strong is the signal? (observation > interview > assumption) | 20% |
| **Reversibility** | If wrong, how hard is it to undo? | 10% |

## Scoring guide (1–5 per dimension)

### Desirability
- 5: Multiple users explicitly described this struggle unprompted
- 4: Users confirmed when asked; pattern in support tickets or analytics
- 3: Logical inference from known problems; no direct validation
- 2: Internal assumption; no user signal
- 1: Builds on a contested or disproved assumption

### Feasibility
- 5: Straightforward implementation; team has done similar before
- 4: Technically clear; requires new tooling or one new dependency
- 3: Complex; requires a major technical decision or new expertise
- 2: Significant unknowns; rough estimate only
- 1: Pie-in-the-sky; would require fundamental platform change

### Viability
- 5: Clear revenue path or cost reduction; strong ROI case
- 4: Indirect but credible path to value (retention, CAC reduction, etc.)
- 3: Value is real but hard to measure; strategic bet
- 2: Mostly cost with unclear return
- 1: Negative expected value or high maintenance burden

### Evidence
- 5: Behavioural data (what users did, not said)
- 4: Multiple user interviews with consistent signals
- 3: Single interview or customer support pattern
- 2: Analogous product or competitor data
- 1: Internal team opinion

### Reversibility
- 5: Trivially undoable (feature flag, config change)
- 4: Undoable but requires 1–2 sprints of cleanup
- 3: Partially reversible; some technical debt left behind
- 2: Hard to reverse; affects data model or external contracts
- 1: Irreversible (migrations, public API, published data)

## Output template

```markdown
## Idea under evaluation
[Name and one-sentence description]

## Rubric scores
| Dimension | Score (1–5) | Notes |
|-----------|------------|-------|
| Desirability | | |
| Feasibility | | |
| Viability | | |
| Evidence | | |
| Reversibility | | |

## Weighted total
[Calculate: Desirability×0.25 + Feasibility×0.25 + Viability×0.20 + Evidence×0.20 + Reversibility×0.10]

## Gate check
- Feasibility ≥ 3? [yes/no]
- Evidence ≥ 3? [yes/no]
→ If both yes: proceed to [[Decision-Matrix]]
→ If either no: return to ideation or drop

## Verdict
[Proceed / Needs validation first / Drop + reason]
```

## Role assignments

- **[[CPO]]** — leads Desirability and Evidence scoring
- **[[CTO]]** — leads Feasibility and Reversibility scoring
- **[[CFO]]** — leads Viability scoring
- **[[CoS]]** — aggregates and writes verdict

## See also

→ [[Synthesis-Protocol]] · [[Decision-Matrix]] · [[BRAINSTORM_INDEX]]
