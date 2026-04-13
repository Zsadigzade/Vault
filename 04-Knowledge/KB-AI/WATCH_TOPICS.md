---
tags: [kb, ai, learning, automation]
area: knowledge-base
updated: 2026-04-13
tldr: "Topics the server's learning agent monitors and searches autonomously."
watch_topics:
  kb_domains:
    - query: "AI agent frameworks 2025 best practices"
      proposed_path: "04-Knowledge/KB-AI/Agent-Orchestration-Patterns.md"
    - query: "prompt engineering techniques chain of thought 2025"
      proposed_path: "04-Knowledge/KB-AI/Prompt-Engineering-Advanced.md"
    - query: "RAG retrieval augmented generation latest techniques"
      proposed_path: "04-Knowledge/KB-AI/RAG-Knowledge-Retrieval.md"
    - query: "business strategy frameworks latest research"
      proposed_path: "04-Knowledge/KB-Business/Strategy-Frameworks.md"
    - query: "product market fit discovery signals founders"
      proposed_path: "04-Knowledge/KB-Business/Product-Market-Fit-and-Discovery.md"
    - query: "growth loops viral coefficient product-led growth"
      proposed_path: "04-Knowledge/KB-Business/Growth-Loops.md"
    - query: "UI UX design trends mobile 2025"
      proposed_path: "04-Knowledge/KB-Design/Mobile-Design-Principles.md"
    - query: "deep work productivity systems builders developers"
      proposed_path: "04-Knowledge/KB-Productivity/Deep-Work-Newport.md"
    - query: "systems thinking mental models decision making"
      proposed_path: "04-Knowledge/KB-Science/Systems-Thinking-Meadows.md"
    - query: "behavioral economics nudge theory product design"
      proposed_path: "04-Knowledge/KB-Science/Behavior-Model-Fogg.md"

  bruh_stack:
    - query: "Capacitor v8 latest changelog updates"
      proposed_path: "05-Projects/BRUH/reference/10 - Coding Patterns & Preferences.md"
    - query: "Supabase new features realtime postgres 2025"
      proposed_path: "04-Knowledge/KB-Postgres/Realtime & Subscriptions.md"
    - query: "RevenueCat in-app purchase best practices 2025"
      proposed_path: "05-Projects/BRUH/features/Monetization.md"
    - query: "Capgo OTA updates Capacitor live updates"
      proposed_path: "05-Projects/BRUH/features/Capgo OTA.md"
    - query: "React 18 19 performance patterns concurrent features"
      proposed_path: "04-Knowledge/KB-TypeScript/React 18 Concurrent Features.md"
    - query: "Vite build optimization bundle size 2025"
      proposed_path: "04-Knowledge/KB-Performance/Vite Build Optimization.md"
    - query: "Supabase RLS row level security patterns"
      proposed_path: "04-Knowledge/KB-Postgres/RLS Pattern Library.md"
    - query: "mobile app push notifications best practices FCM"
      proposed_path: "05-Projects/BRUH/features/Push Notifications.md"

  ai_tooling:
    - query: "Ollama new models releases benchmarks 2025"
      proposed_path: "04-Knowledge/KB-AI/Local-LLM-Ollama-Patterns.md"
    - query: "Anthropic Claude API new features updates"
      proposed_path: "04-Knowledge/KB-AI/Claude Code CLI Reference.md"
    - query: "Model Context Protocol MCP servers tools 2025"
      proposed_path: "04-Knowledge/KB-AI/MCP Server Patterns.md"
    - query: "multi-agent AI systems orchestration patterns"
      proposed_path: "04-Knowledge/KB-AI/Multi-Agent-System-Design.md"
    - query: "local LLM inference optimization quantization GGUF"
      proposed_path: "04-Knowledge/KB-AI/Local-LLM-Ollama-Patterns.md"
    - query: "LLM benchmark MMLU HumanEval latest models comparison"
      proposed_path: "04-Knowledge/KB-AI/Local-LLM-Ollama-Patterns.md"
    - query: "AI coding assistant tools Cursor Copilot Aider 2025"
      proposed_path: "04-Knowledge/KB-AI/Cursor Tips & Power Features.md"
    - query: "vector databases embeddings semantic search 2025"
      proposed_path: "04-Knowledge/KB-AI/RAG-Knowledge-Retrieval.md"

  competitive_market:
    - query: "social app growth strategies viral retention 2025"
      proposed_path: "04-Knowledge/KB-Business/Growth-Loops.md"
    - query: "mobile app monetization trends in-app purchase subscriptions"
      proposed_path: "04-Knowledge/KB-Business/Pricing-Strategy.md"
    - query: "meme sharing app trends short video social 2025"
      proposed_path: "05-Projects/BRUH/overview/Project Overview.md"
    - query: "app store optimization ASO strategies 2025"
      proposed_path: "04-Knowledge/KB-DevOps/App Store Optimization (ASO).md"
    - query: "mobile user retention churn reduction strategies"
      proposed_path: "04-Knowledge/KB-UX/Social App Engagement Patterns.md"
    - query: "startup growth go to market playbook indie developer"
      proposed_path: "04-Knowledge/KB-Business/Go-To-Market-Channels.md"

  agentic_general:
    - query: "knowledge management personal knowledge base PKM 2025"
      proposed_path: "04-Knowledge/KB-Productivity/PARA-and-CODE-Forte.md"
    - query: "second brain Obsidian knowledge graph automation"
      proposed_path: "04-Knowledge/KB-Productivity/PARA-and-CODE-Forte.md"
    - query: "automation n8n Make workflow no-code tools 2025"
      proposed_path: "04-Knowledge/KB-AI/Agent-Orchestration-Patterns.md"
    - query: "open source AI tools self-hosted LLM stack 2025"
      proposed_path: "04-Knowledge/KB-AI/Local-LLM-Ollama-Patterns.md"
    - query: "cognitive science mental models learning techniques"
      proposed_path: "04-Knowledge/KB-Science/Cognitive-Biases-Overview.md"
    - query: "web scraping data collection ethical legal 2025"
      proposed_path: "04-Knowledge/KB-AI/Agent-Debugging-Strategies.md"
---

# Watch Topics

> **Purpose:** Registry of topics the autonomous learning agent (`scripts/knowledge_update.py`) monitors. Add, remove, or edit queries here to control what the vault learns about.

## TL;DR

- **5 categories:** kb_domains, bruh_stack, ai_tooling, competitive_market, agentic_general
- **Run manually:** `python scripts/knowledge_update.py`
- **By category:** `python scripts/knowledge_update.py --topic ai_tooling`
- **Cooldown:** Each query is skipped for 3 days after being searched (configurable)
- **Results go to:** `06-Inbox/pending/` — review with `/approve-inbox`

## Adding topics

Add entries to the frontmatter YAML above. Format:
```yaml
- query: "search query here"
  proposed_path: "04-Knowledge/KB-Folder/File.md"
```

Or simpler (just a string):
```yaml
- "search query here"
```

## Topic categories

| Category | Purpose | Cadence |
|----------|---------|---------|
| `kb_domains` | Update general knowledge KBs | Weekly |
| `bruh_stack` | Monitor BRUH project tech stack | Weekly |
| `ai_tooling` | Track AI/agent tooling releases | 2x/week |
| `competitive_market` | Market and competitive signals | Weekly |
| `agentic_general` | General agentic AI knowledge | Weekly |

## Confidence thresholds

- `≥ 0.85` → `low_risk: true` (auto-merge eligible)
- `0.55–0.84` → `human_gate: required`
- `< 0.55` → dropped, logged to [[LEARNING_LOG]]
