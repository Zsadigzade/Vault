---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "When I ___, I want to ___, so I can ___."
---

# Jobs To Be Done (agent-executable)

## TL;DR

"When I ___, I want to ___, so I can ___." — frame user need as progress, not feature.

## When to use

Discovery before building. When you don't know why users are (or aren't) adopting something. The insight: people don't buy products, they "hire" them to make progress in a specific situation. Forces you to describe behaviour and context, not demographics.

## Core job statement format

```
When [situation],
I want to [motivation / progress sought],
so I can [outcome / transformation].
```

**Example:** "When I finish a workout, I want to quickly log what I did, so I can track my progress over weeks without it feeling like homework."

## Agent instructions

You are conducting a Jobs-To-Be-Done analysis. Do not suggest features. Map the user's struggle, what they've tried, and what progress they're seeking. Then write 3–5 job statements.

## Discovery interview questions

| Category | Question |
|----------|---------|
| **Context** | Walk me through the last time you struggled with [problem]. What were you doing right before? |
| **Progress sought** | What were you trying to accomplish? What does success look like? |
| **Alternatives tried** | What did you try first? What other tools have you used for this? |
| **Almost worked** | What product came closest? What did it get wrong? |
| **Switch trigger** | What would make you stop using the current solution? |
| **Hiring language** | If you had to describe this product to a friend in one sentence, what would you say? |

## Output template

```yaml
jtbd_analysis:
  subject: "[product / feature / problem area]"
  date: "YYYY-MM-DD"

  job_statements:
    - situation: ""
      motivation: ""
      outcome: ""
      evidence: ""      # what user said or did that surfaces this job
      frequency: ""     # how often does this situation occur?

  key_insight: ""       # one sentence: what surprised you?
  
  anti_jobs:
    - "[thing users DON'T want — what they're trying to avoid]"

  competing_solutions:
    - name: ""
      why_hired: ""
      why_fired: ""
```

## Role assignments

- **[[CPO]]** — primary user; run before any roadmap decision
- **[[CMO]]** — use job statements to write positioning ("we help X do Y")
- **[[CEO]]** — use anti-jobs to find underserved markets

## After session

→ [[Double-Diamond]] to move from job insight to solution space. Link to [[CPO]] output format's Problem section.
