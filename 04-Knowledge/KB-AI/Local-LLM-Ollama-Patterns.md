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

## Model Landscape — 2026-04-13

- **Llama 4 Scout** — 93.2% on VQA (2026 benchmark); multimodal; Ollama supported
- **DeepSeek-R1** — approaches GPT-4 level reasoning; best open reasoning model 2025
- **Mistral Small 3** — new benchmark for sub-7B category; strong for edge/local use
- **qwen2.5-coder:1.5b** — fits in 4GB RAM; good for code summarization tasks on CPU

## Quantization Guide — 2026-04-13

- **GGUF** — CPU-optimized format; K-Quants (Q4_K_M best quality/size tradeoff), I-Quants for importance-matrix
- **AWQ** — activation-aware quantization; better quality than GPTQ at same bit-width
- **GPTQ** — GPU-focused; faster inference on CUDA but needs VRAM
- **Practical rule**: Q4_K_M for 4-8GB RAM; Q5_K_M if 10GB+; Q8_0 for near-lossless quality

## Benchmarks (Feb 2026)

- Gemini 3.1 Pro: 94.3% MMLU | Claude Opus 4.6: 91.3% | Qwen3.5-plus: 88.4% | GPT-5.3 Codex: 81%
- Source: [lxt.ai benchmarks](https://www.lxt.ai/blog/llm-benchmarks/)
