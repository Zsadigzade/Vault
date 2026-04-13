---
tags: [kb, ai, ollama, local-llm]
area: knowledge-base
updated: 2026-04-13
tldr: "Pull models, quantize tradeoffs, context limits, API parity with OpenAI shape."
---

# Local LLM and Ollama patterns

## TL;DR

- **Hardware:** VRAM bounds model size; quantize (Q4/Q5) for speed/size tradeoff.
- **Context:** respect window; summarize long docs before stuffing.
- **API:** Ollama OpenAI-compatible `/v1/chat/completions` for tooling reuse.

## Ops

- Pin model tags in prod (`model:7b` not floating `latest`).
- VPS: TLS + auth in front of Ollama; never public `:11434`.

## Role wiring

- See `01-Agents/roles/*.md` `endpoint:` + `model:`.
