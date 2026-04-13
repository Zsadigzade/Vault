---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Parallel perspectives; map hats to C-suite where useful."
---

# Six Thinking Hats (agent-executable)

## TL;DR

Parallel perspectives; map hats to C-suite roles for multi-agent session.

## When to use

Complex decisions where one analytical mode dominates and blinds the group. Forces emotional, risk, and creative views even when culture defaults to pure logic. Run when a team is stuck or polarized.

## Hat-to-role mapping

| Hat | Focus | Role | What to produce |
|-----|-------|------|----------------|
| **White** | Facts only. No opinions. | [[CTO]] | Data, metrics, knowns, unknowns list |
| **Red** | Gut feeling. No justification required. | [[CMO]] | "This feels..." statements, instinctive reactions |
| **Black** | Devil's advocate. Risks only. | [[CISO]] | What goes wrong, why this fails |
| **Yellow** | Benefits only. Optimistic. | [[CEO]] | Why this works, upside cases |
| **Green** | New ideas. Wild options. No criticism. | [[CMO]] / [[CPO]] | Alternative approaches, creative leaps |
| **Blue** | Process management. | [[CoS]] | Structure the session, call transitions, synthesize |

## Agent instructions

Blue hat ([[CoS]]) opens and closes. All other hats run in **parallel** unless you have a single agent — in that case run them sequentially, clearly labelled. Blue hat synthesizes at the end.

**Rule:** When wearing a hat, **stay in that hat**. No Black hat thinking during Yellow, no facts during Red.

## Output template

```markdown
### White Hat — Facts
- Known: [fact]
- Unknown / need to find out: [gap]

### Red Hat — Instinct
- [Gut feeling without justification]

### Black Hat — Risks
- [Risk 1: scenario and consequence]
- [Risk 2: ...]

### Yellow Hat — Benefits
- [Benefit 1: why this succeeds]
- [Benefit 2: ...]

### Green Hat — Alternatives
- [Alternative 1 — wild ok]
- [Alternative 2 — ...]

### Blue Hat — Synthesis (CoS)
**Key tension:** [where Black and Yellow conflict]
**What we learned from Red:** [unexpected instinct]
**Recommended next step:** [one action]
```

## Sequencing for multi-agent run

1. CoS (Blue) opens: frames question, assigns hats
2. CTO (White), CISO (Black), CEO (Yellow), CMO (Red + Green) — **parallel**
3. CoS (Blue) synthesizes: themes → conflicts → recommendation
4. Store in `03-Brainstorm/sessions/` (dated note)

## After session

→ [[Synthesis-Protocol]] for final decision if multiple options remain.
