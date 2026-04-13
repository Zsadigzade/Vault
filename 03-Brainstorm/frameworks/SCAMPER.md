---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Substitute Combine Adapt Modify Put Eliminate Reverse — agent fills structured list."
---

# SCAMPER (agent-executable)

## TL;DR

Seven lenses on one artifact. Output YAML or table per lens.

## When to use

Improving or innovating on something that **already exists** — a product, process, feature, workflow, or business model. Not for generating from scratch (use [[Idea-Matrix]] for that). Best in 15-minute focused runs.

## Agent instructions

You are running the SCAMPER framework. Apply each lens to the **subject** provided. Generate 2–3 specific, actionable ideas per lens. Flag your top idea per lens with `★`. No vague generalities.

## The 7 lenses

| Letter | Question | Agent prompt |
|--------|----------|--------------|
| **S** Substitute | What component, step, or rule could be replaced with something different? | Think: materials, people, processes, rules, algorithms |
| **C** Combine | What two elements could merge or integrate to create something new? | Think: features, audiences, channels, time periods |
| **A** Adapt | What exists in another domain, industry, or era that could be adapted here? | Think: biology, gaming, logistics, finance |
| **M** Modify | What could be amplified, shrunk, sped up, slowed down, or reshaped? | Think: frequency, size, colour, form, sequence |
| **P** Put to other use | What could this serve that it wasn't originally designed for? | Think: new audience, new context, new problem |
| **E** Eliminate | What is unnecessary, causing friction, or adding cost without value? | Think: steps, features, approvals, dependencies |
| **R** Rearrange / Reverse | What if the order, roles, or logic were inverted? | Think: onboarding → offboarding, push → pull |

## Output template

```yaml
scamper_session:
  subject: "[describe the thing being analyzed]"
  date: "YYYY-MM-DD"
  agent: "[role running this]"
  ideas:
    substitute:
      - idea: ""
        rationale: ""
        top: false
    combine:
      - idea: ""
        rationale: ""
        top: false
    adapt:
      - idea: ""
        rationale: ""
        top: false
    modify:
      - idea: ""
        rationale: ""
        top: false
    put_to_other_use:
      - idea: ""
        rationale: ""
        top: false
    eliminate:
      - idea: ""
        rationale: ""
        top: false
    rearrange:
      - idea: ""
        rationale: ""
        top: false
  top_picks:
    - lens: ""
      idea: ""
      why_it_wins: ""
```

## Role mapping

| Lens | Best role to run it |
|------|-------------------|
| Substitute | [[CTO]] (technical substitution), [[COO]] (process substitution) |
| Combine | [[CPO]] (feature merging), [[CMO]] (channel + message combination) |
| Adapt | [[CEO]] (cross-industry strategy), [[CMO]] (borrow from adjacent brands) |
| Modify | [[CPO]] (UX scale), [[CTO]] (performance scaling) |
| Put to other use | [[CMO]] (new markets), [[CEO]] (pivot options) |
| Eliminate | [[COO]] (operational waste), [[CFO]] (cost elimination) |
| Rearrange | [[CPO]] (onboarding flow), [[COO]] (process inversion) |

## After session

Run [[Synthesis-Protocol]] on `top_picks` to reach a decision. Store session in `03-Brainstorm/sessions/`.
