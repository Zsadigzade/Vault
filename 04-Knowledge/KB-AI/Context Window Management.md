---
tags: [kb, ai, context, tokens, claude-code]
area: knowledge-base
updated: 2026-04-13
---

# Context window management

---

## Budgeting

| High value | Low value (often) |
|------------|-------------------|
| Files you will **edit** | Entire `node_modules` |
| **Tests** that fail | Generated build artifacts |
| **Error** message + stack top | Whole chat history |

---

## Progressive disclosure

1. Start with **index** ([[Agent Quick Reference]], [[📚 Knowledge Base]])
2. Open **one** KB note for the task
3. Pull **repo files** after hypothesis

---

## Claude Code — session hygiene

- **Manual `/compact` around ~50%** context — avoid the “agent dumb zone” (degraded quality when context is overstuffed)
- **`/clear`** — hard reset when switching unrelated tasks
- **`/rewind` / Esc-Esc** — undo bad turns or file state; faster than arguing in the same polluted thread
- **Break work** so subtasks finish **under ~50%** of a single window when possible
- **Context fork** — skills/commands with `context: fork` run in isolated subagent; main thread sees **outcomes**, not every tool call

---

## Test-time compute

- Separate context windows for **implement** vs **review** — same model can catch bugs it introduced in another window

---

## Summarization

- For long threads: **bullet summary** of decisions + open questions before continuing
- Paste **structured** context (tables, file paths) vs prose walls

---

## Attachments

- **Screenshots** for UI bugs; **redact** PII
- **Logs** — trim to relevant window

---

## Anti-patterns

- Dumping **entire** SQL schema when changing one policy — link file + line range instead
- **Compaction errors** — temporarily switch to a **larger context model**, then `/compact`
- Pushing the same derailed conversation — **rewind** or **new session**

---

## See also

- [[Prompt Patterns for Code]] · [[Cursor Tips & Power Features]] · [[Rules & Skills Authoring]]
- Quick table: [[Token & context habits — compact]]
- Token compression: [[caveman]] — `/caveman [lite|ultra]`, `/caveman:compress <file>` — [[Curated GitHub Repositories]] § Token optimization
