---
tags: [agents, dispatcher, orchestration]
area: agents
updated: 2026-04-13
tldr: "Keyword → C-suite role; solo | parallel | sequential patterns."
---

# Dispatcher — role routing

## Routing table

- **strategy, vision, direction, trade-offs** → [[CEO]]
- **operations, process, execution, cadence** → [[COO]]
- **architecture, technical feasibility, stack** → [[CTO]]
- **brand, marketing, creative, growth loops** → [[CMO]]
- **financial, cost, ROI, runway, unit economics** → [[CFO]]
- **product, features, JTBD, roadmap** → [[CPO]]
- **security, compliance, threat, privacy** → [[CISO]]
- **routing, synthesis, vault hygiene, agendas** → [[CoS]]

## Patterns

- **Solo:** one dominant domain → one role.
- **Parallel:** independent domains → multiple roles → [[CoS]] aggregates (see [[ORCHESTRATION_PROTOCOL]]).
- **Sequential:** dependencies (e.g. strategy → budget → build) → ordered chain with YAML `handoff` object in session note.

## Invocation

- **Cursor / Claude:** read role file under `01-Agents/roles/`; honor `model:` and `endpoint:` (local Ollama vs cloud).
- **Automation:** `vault-automation` `run_workflow.py` uses same table.

## After dispatch

Append outcome summary to [[SESSION_HANDOFF]] or `06-Inbox/pending/` if proposing vault changes.
