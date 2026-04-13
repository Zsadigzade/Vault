---
tags: [kb, ai, multi-agent]
area: knowledge-base
updated: 2026-04-13
tldr: "Dispatcher, handoffs, synthesis, token caps — match vault DISPATCHER."
---

# Multi-agent system design

## TL;DR

- **Router/dispatcher** chooses specialists; avoid everyone reading full context.
- **Handoff object** carries decisions + open questions only.
- **Aggregator** ([[CoS]]) enforces brevity.

## Vault implementation

- [[DISPATCHER]] · [[ORCHESTRATION_PROTOCOL]] · role files in `01-Agents/roles/`.

## Orchestration Patterns — 2026-04-13

- **Deterministic orchestration** — next agent defined in workflow code, not decided by agents; more reliable for production
- **Structured outputs** — use typed schemas for inter-agent data; inspect programmatically before passing
- **Azure multi-agent** — task delegation + response aggregation with enterprise-grade reliability
- **OpenAI Agents SDK** — `handoff` primitive for agent-to-agent transfer; built-in tracing
- Source: [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [OpenAI SDK](https://openai.github.io/openai-agents-python/multi_agent/)
