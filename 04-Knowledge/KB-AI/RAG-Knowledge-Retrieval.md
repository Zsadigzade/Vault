---
tags: [kb, ai, rag]
area: knowledge-base
updated: 2026-04-13
tldr: "Chunk, embed, retrieve, rerank; hybrid keyword+vector for vault notes."
---

# RAG and knowledge retrieval

## TL;DR

- **Chunking:** semantic or heading-aware for markdown vault notes.
- **Hybrid:** BM25 + embeddings reduces miss rate on exact tokens (e.g. error codes).
- **Rerank** top-k for quality if budget allows.

## Vault alignment

- Prefer reading **[[📚 Knowledge Base]]** hubs + TL;DR sections before full-note load (token discipline).
