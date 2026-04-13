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
