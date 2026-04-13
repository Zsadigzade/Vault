---
tags: [brainstorm, framework, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Diverge → converge twice (discover + deliver)."
---

# Double Diamond (agent-executable)

## TL;DR

Diverge → converge twice: first discover the right problem, then design the right solution.

## When to use

Anytime you're solving for users or customers. Starting with "build X" skips Diamond 1. The most common failure in product work is building the right solution to the wrong problem. Diamond 1 prevents that.

## The model (IDEO / UK Design Council)

```
Discover → Define → Develop → Deliver
    ◇◇◇        ◆        ◇◇◇       ◆
  (wide)    (narrow)  (wide)  (narrow)
```

## Agent instructions

You are running the Double Diamond. Do not jump to solutions before completing Diamond 1. Each phase has a distinct output — produce them in order.

## Diamond 1 — Right problem

### Phase 1A: Discover (diverge)
Explore the problem space widely. No judgement.
- Who is affected? Who are the stakeholders?
- What context does this happen in?
- What's the full range of things that could be going wrong?
- What do users/customers actually do today?

### Phase 1B: Define (converge)
Narrow to the problem worth solving.
- Write one **problem statement** (Point of View format): "[User] needs [need] because [insight]"
- Define **success signal**: what changes in measurable behaviour if solved?
- Confirm with [[CPO]] and [[CEO]] before proceeding.

## Diamond 2 — Right solution

### Phase 2A: Develop (diverge)
Generate multiple solution approaches. Wild ideas welcome.
- Sketch 3–5 distinct approaches (not variations of the same thing)
- For each: what's the core bet? What breaks if wrong?
- Run [[SCAMPER]] or [[Idea-Matrix]] here if stuck

### Phase 2B: Deliver (converge)
Select and commit.
- Score approaches using [[Decision-Matrix]]
- Pick one; document what was killed and why
- Define milestones and first experiment

## Output template

```markdown
## Diamond 1 — Problem

### Discover (diverge)
**Stakeholders affected:**
- [stakeholder 1]

**Problem space observations:**
- [observation 1]
- [observation 2]

### Define (converge)
**Problem statement:**
[User] needs [need] because [insight].

**Success signal:**
[Measurable behaviour that changes if this is solved]

---

## Diamond 2 — Solution

### Develop (diverge)
**Approach A:** [brief description]
**Approach B:** [brief description]
**Approach C:** [brief description]

### Deliver (converge)
**Chosen approach:** [which one and why]
**Kill list:** [what was rejected and why — important for future reference]
**First milestone:** [what ships first]
**First experiment:** [smallest test of the core bet]
```

## Role assignments

- Diamond 1: [[CPO]] (discovery), [[CMO]] (user context), [[CoS]] (facilitation)
- Diamond 2: [[CTO]] (solution feasibility), [[CFO]] (cost of approaches), [[CISO]] (security angle)

## After session

→ [[Synthesis-Protocol]] to finalize. Store in `03-Brainstorm/sessions/`.
