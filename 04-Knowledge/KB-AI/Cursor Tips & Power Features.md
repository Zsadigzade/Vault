---
tags: [kb, ai, cursor, ide, claude-code]
area: knowledge-base
updated: 2026-04-14
---

# Cursor tips & power features

---

## Context @-mentions

| Mention | Use |
|---------|-----|
| **@Files** | Pin exact files to context |
| **@Folder** | Wider scope — watch token budget |
| **@Codebase** | Semantic search — good for “where is X?” |
| **@Docs** | Official docs indexing when available |
| **@Web** | Fresh facts — APIs, deprecations |

---

## Composer / Agent

- **Multi-file edits** — state invariants first (“don’t break RLS”, “keep native keyboard mode”)
- **Plan mode** — large refactors, auth, payments, migrations; align before edits
- **Verification-first** — give the agent a **feedback loop** (run tests, hit health URL, use MCP). Quality often **2–3×** when it can verify

---

## Plan-mode-first workflow (Claude Code–aligned)

- Pour effort into the **plan** so implementation can be one-shot
- Optional: one session for plan, another for execute — fresh context
- If implementation drifts, **switch back to plan** — don’t push through confusion

---

## Prompting patterns

- **Challenge:** “Grill me on these changes; don’t open a PR until I pass.” / “Prove this works” + diff vs `main`
- **Reset mediocre fixes:** “Knowing what you know now, scrap this and implement the elegant solution.”
- **Reduce ambiguity** — detailed specs beat vague “fix auth”

---

## Delegation & parallelism

- **Subagents / Task tool** — offload search or review so the main context stays clean
- **“Use subagents”** — explicit nudge to throw more compute at hard problems
- Multiple terminals / worktrees — isolate parallel streams (see [[Agent Orchestration Patterns]])

---

## Debugging & UX

- **Screenshots** for UI bugs (redact PII)
- **Browser / Playwright MCP** — console and network visibility
- **Long-running commands** — background terminal for streaming logs
- **Voice dictation** — faster, often richer prompts (Cursor / OS / Claude Code `/voice`)

---

## Output & learning

- **Explanatory / Learning** output styles (where available) — “why” behind changes while exploring a codebase
- **ASCII diagrams** — protocols, data flow, folder intent

---

## Rules

- Repo **`.cursor/rules`** — always-on constraints (see [[Memory File Best Practices]])
- **Skills** — procedural how-tos — [[Rules & Skills Authoring]]

---

## shadcn/ui MCP (official)

- **Install / merge config:** `npx shadcn@latest mcp init --client cursor` (from project root — same place as `components.json` when using shadcn CLI).
- **Wiring:** adds **`shadcn`** to **`.cursor/mcp.json`** — `command` **`npx`**, **`args`:** `shadcn@latest`, `mcp` (see [[12 - MCP & External APIs]]).
- **Cursor:** **Settings → MCP** — toggle **shadcn** on; **green dot** = server up. **Restart Cursor** after changing `mcp.json`.
- **Use:** ask agent to list registry components, add primitives (button, dialog, card), scaffold blocks — tools read **live registry** + project config.
- **Docs:** [shadcn MCP](https://ui.shadcn.com/docs/mcp).

---

## Diffs & review

- Read full diff before accept — especially **SQL migrations** and **auth**
- Use **partial accept** when mixing good + bad hunks

---

## Keyboard workflow

- **Cmd/Ctrl+K** inline, **Cmd/Ctrl+L** chat — muscle memory saves time

---

## AI Coding Tools Comparison — 2026-04-14

- **The quartet** (Cursor best practice): MCPs + Rules (`.cursor/rules/*.mdc`) + Memories + Auto-run — configure all four at project start for full context control
- **Cursor Enterprise**: global model access controls, MCP controls, system-level agent rules; supports OpenAI/Anthropic/Gemini/xAI
- **GitHub Copilot** ranked best overall for most developers in 2025 (artificialanalysis.ai + thedroidsonroids.com benchmarks) — most consistent, fewer context-loss issues
- **Cursor weakness**: context forgetting between sessions — project structure / prior work lost (Reddit r/ChatGPTCoding, Feb 2025)
- **BYOM support**: Cline, Continue, Aider, Goose support bring-your-own-model; Copilot does not
- Source: [artificialanalysis.ai coding agents](https://artificialanalysis.ai/agents/coding), [Cursor complete guide 2025](https://medium.com/@hilalkara.dev/cursor-ai-complete-guide-2025-real-experiences-pro-tips-mcps-rules-context-engineering-6de1a776a8af)

---

## See also

- [[Context Window Management]] · [[Prompt Patterns for Code]] · [[Agent Debugging Strategies]] · [[Claude Code CLI Reference]] · [[12 - MCP & External APIs]]
