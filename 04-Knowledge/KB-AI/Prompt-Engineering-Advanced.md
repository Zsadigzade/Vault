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

## Techniques Update — 2026-04-13

- **Chain-of-Table** — extends CoT to structured/tabular data; maintains structural integrity across reasoning steps
- **Few-shot prompting** — most reliable baseline; hand-craft diverse examples for consistent output
- **Role-based prompting** — assign domain expert persona; improves precision on specialized tasks
- **Format control** — specify output format (JSON, markdown, list) explicitly to reduce post-processing
- **Zero-shot CoT** — append "Let's think step by step"; works well when examples are expensive to craft
