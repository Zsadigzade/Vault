---
tags: [brainstorm, index, agents]
area: brainstorm
updated: 2026-04-13
tldr: "Pick framework by goal: generate ideas, understand problem, or decide."
---

# Brainstorm Index

## TL;DR

- **Generate ideas on existing thing** → [[SCAMPER]]
- **Understand problem depth** → [[Problem-Tree]] or [[First-Principles]]
- **Discover user needs** → [[Jobs-To-Be-Done]] then [[Double-Diamond]]
- **Multi-perspective on decision** → [[Six-Hats]]
- **Generate from scratch** → [[Idea-Matrix]]
- **Pick between options** → [[Decision-Matrix]] (after [[Evaluation-Rubric]])

---

## Framework selection guide

| Goal | Framework | Roles | Output |
|------|-----------|-------|--------|
| Improve / innovate existing thing | [[SCAMPER]] | Any | YAML idea list |
| Multi-perspective analysis | [[Six-Hats]] | C-suite parallel | Per-hat sections |
| Root cause of recurring problem | [[Problem-Tree]] | COO / CTO / CISO | Tree + leverage point |
| Challenge core assumptions | [[First-Principles]] | CEO / CTO | Assumption audit + rebuild |
| Understand user motivation | [[Jobs-To-Be-Done]] | CPO / CMO | Job statements |
| Full problem → solution cycle | [[Double-Diamond]] | CPO + all | 4-phase document |
| Generate from two dimensions | [[Idea-Matrix]] | CPO / CMO / CEO | Filled matrix |
| Score and select options | [[Decision-Matrix]] | All (role weights) | Scored table + winner |
| Filter ideas before decision | [[Evaluation-Rubric]] | CPO / CTO / CFO | Scored + verdict |
| Merge multiple framework outputs | [[Synthesis-Protocol]] | CoS | Themes + decision |

---

## Recommended sequences

### New product decision
```
Jobs-To-Be-Done → Double-Diamond (D1) → Idea-Matrix → Evaluation-Rubric → Decision-Matrix
```

### Recurring operational problem
```
Problem-Tree → First-Principles → SCAMPER (on the process) → Decision-Matrix
```

### Strategic bet (new market / direction)
```
Six-Hats → First-Principles → Idea-Matrix → Decision-Matrix
```

### Feature prioritization
```
Jobs-To-Be-Done → Evaluation-Rubric → Decision-Matrix
```

---

## Session output location

All brainstorm sessions → `03-Brainstorm/sessions/YYYY-MM-DD-[topic].md`

Use [[Templates/Brainstorm session]] template for new sessions.

---

## Synthesis and evaluation

- **[[Synthesis-Protocol]]** — merge multi-framework outputs into one decision-ready note
- **[[Evaluation-Rubric]]** — filter ideas on 5 dimensions (Desirability, Feasibility, Viability, Evidence, Reversibility)
