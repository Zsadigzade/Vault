---
tags: [kb, ai, memory, documentation, claude-code]
area: knowledge-base
updated: 2026-04-05
---

# Memory file best practices

---

## Layering

| Layer | Content |
|-------|---------|
| **Index** | Short pointers — `MEMORY.md`, [[🏠 Home]] |
| **Topic files** | Deep dives — database, security, launch |
| **Repo** | `CLAUDE.md` — commands, non-negotiables |

> [!tip] **Low token index + deep files** beats one giant scroll.

---

## What to put in memory

| Include | Exclude |
|---------|---------|
| Invariants (“never X”) | Secrets, tokens, passwords |
| Command cheat sheets | One-off chat noise |
| Service URLs & regions | Speculation about prod state |
| “When to read what” tables | Huge stack traces |

---

## Claude Code — how `CLAUDE.md` loads

Two mechanisms ([official memory docs](https://code.claude.com/docs/en/memory)):

| Mechanism | Direction | When loaded |
|-----------|-----------|-------------|
| **Ancestor** | **Up** cwd → filesystem root | **At session start** — every `CLAUDE.md` on path |
| **Descendant** | **Down** into subdirs | **Lazy** — only when you read/edit files under that subtree |

**Implications:**

- **Siblings never load** — working in `frontend/` does not load `backend/CLAUDE.md`.
- **Monorepo:** Put **shared** conventions in **root** `CLAUDE.md`; put **package-specific** rules in `packages/foo/CLAUDE.md` (loads when touching `foo/`).
- **Global:** `~/.claude/CLAUDE.md` can apply to **all** Claude Code sessions.

**BRUH:** Single app root is fine; optional future `admin-web/CLAUDE.md`, `dashboard/CLAUDE.md` if those trees need isolated instructions.

---

## Size & structure

- Target **&lt; ~200 lines per `CLAUDE.md` file** for reliable adherence (team guidance from Claude Code maintainers). Split overflow into `.claude/rules/` or linked docs.
- **After every correction:** end with “update `CLAUDE.md` / vault so this mistake doesn’t repeat” — compounding quality.
- **Long files:** wrap critical domain blocks in conditional emphasis (e.g. XML-style `<important if="touching auth">…</important>` patterns discussed in community posts) so critical rules stay salient.

---

## `.cursor/rules`

- **Actionable** bullets; link to vault notes for narrative
- **Glob** scope when rule is file-specific (`*.sql`, `supabase/**`)
- Harness-enforced behavior where possible (permissions, format hooks) beats “NEVER do X” prose alone

---

## `.claude/rules` (Claude Code)

Split large instructions into project-scoped markdown under `.claude/rules/` — loaded as organized rules alongside `CLAUDE.md`.

---

## Drift control

- Date **`updated`** in frontmatter when changing facts
- **Decision log** for “why” — [[Decision Log]] (project)
- **Constitution / immutable laws** — separate file; do not let casual edits weaken non-negotiables ([[CONSTITUTION]])

---

## “Any dev can run tests first try”

If a new contributor cannot run `npm run test` / `npm run build` from your memory alone, the onboarding section is **under-specified** — add exact commands, env prerequisites, and Windows vs Mac notes.

---

## See also

- [[Context Window Management]] · [[Rules & Skills Authoring]] · [[Agent Quick Reference]] · [[Claude Code CLI Reference]]
- Compress memory files: [[caveman]] → `/caveman:compress CLAUDE.md` — saves ~46% input tokens on load
