---
tags: [kb, ai, prompting]
area: knowledge-base
updated: 2026-04-13
tldr: "Structured output, few-shot, CoT when reasoning; system prompt = policy."
---

# Prompt engineering — advanced

## TL;DR

- **System:** role, constraints, output schema (JSON/XML/markdown headings).
- **Few-shot:** 2–3 diverse examples beat long prose.
- **Chain-of-thought:** ask explicitly when logic errors costly; verify outputs.

## Safety

- Untrusted input → treat as data; delimiter boundaries for injection resistance.
