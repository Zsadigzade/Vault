---
tags: [brainstorm, synthesis, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Merge multi-framework outputs into one decision-ready note."
---

# Synthesis Protocol (agent-executable)

## TL;DR

- Merge multi-framework outputs into one decision-ready note.
- Run after ≥2 frameworks or parallel role session.
- [[CoS]] runs synthesis by default; [[CEO]] makes final call if roles conflict.

## When to use

After any brainstorm session that used ≥2 frameworks or multiple agent roles (Six Hats, parallel dispatch). Synthesis prevents "analysis paralysis" — it forces convergence and a kill list.

## The 5 synthesis steps

### Step 1 — Collect inputs
List all frameworks run and outputs produced. Don't start synthesizing until all role/framework outputs are in.

### Step 2 — Extract themes
Recurring ideas = signal. An idea that shows up in SCAMPER AND JTBD AND CEO output is worth pursuing.
- Bullet 3–7 recurring themes
- Tag each: `[strong]` (≥3 sources) / `[moderate]` (2 sources) / `[single]` (1 source)

### Step 3 — Surface conflicts
Where did frameworks or roles disagree? Name the tension explicitly. Do not paper over it.
- "CEO sees opportunity; CISO flags high risk" → tension: speed vs security
- "SCAMPER suggests eliminating X; CPO evidence shows X is valued" → tension: efficiency vs user value

### Step 4 — Make the decision
One path. Name it. Assign it to a role for ownership.
- Use [[Decision-Matrix]] if still between ≥2 options after synthesis
- Include the **kill list**: what you are explicitly NOT doing (equally important)

### Step 5 — Define the next experiment
Smallest, cheapest test that validates the core bet.
- Time-boxed
- Falsifiable: define what "doesn't work" looks like before running it

## Output template

```markdown
## Session context
**Frameworks used:** [list]
**Roles involved:** [list]
**Date:** YYYY-MM-DD

## Themes
- [Theme 1] [strong/moderate/single]
- [Theme 2] [strong/moderate/single]
- [Theme 3] [...]

## Conflicts
| Tension | Side A | Side B | Resolution |
|---------|--------|--------|-----------|
| [conflict 1] | | | decided by [role] |

## Decision
**Path chosen:** [one sentence — what we are doing]
**Owner:** [role or person]

**Kill list:**
- [What we are not doing and why]
- [What we considered but rejected]

## Next experiment
**Hypothesis:** We believe [X] will cause [Y], measured by [Z].
**Smallest test:** [What to run and when]
**Budget:** [Time / money]
**Kill signal:** [What result tells us to stop]

## Vault updates proposed
[If vault changes needed → list them as inbox captures or note updates]
```

## Role responsibilities

- **[[CoS]]** — runs synthesis, writes output template
- **[[CEO]]** — resolves unresolvable role conflicts
- **[[CPO]]** — validates decision against user evidence
- **[[CTO]]** — confirms next experiment is technically feasible

## Storage

- Session notes → `03-Brainstorm/sessions/YYYY-MM-DD-[topic].md`
- Vault change proposals → `06-Inbox/pending/` with required frontmatter

## See also

→ [[Evaluation-Rubric]] · [[Decision-Matrix]] · [[BRAINSTORM_INDEX]]
