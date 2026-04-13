---
tags: [kb, ai, cursor, skills, claude-code]
area: knowledge-base
updated: 2026-04-05
---

# Rules & skills authoring

> [!tip] **Cursor** = `.cursor/rules` + Composer. **Claude Code CLI** = `.claude/agents`, `.claude/commands`, `.claude/skills`. Patterns below map to both where applicable.

---

## Cursor Rules (`.cursor/rules`)

| Field | Purpose |
|-------|---------|
| **Description** | When rule applies |
| **Globs** | Path scope |
| **Body** | Short must/never + pointers to docs |

Keep **under ~50–100 lines** — link to vault for depth.

---

## Claude Code — Subagents (`.claude/agents/*.md`)

YAML frontmatter + markdown body. **16 common fields:**

| Field | Type | Notes |
|-------|------|--------|
| `name` | string | Required; lowercase + hyphens |
| `description` | string | When to invoke; use **PROACTIVELY** for auto-invocation |
| `tools` | list / string | Allowlist; omit = inherit all. Supports `Agent(agent_type)` |
| `disallowedTools` | list | Removed from inherited set |
| `model` | string | `haiku`, `sonnet`, `opus`, `inherit` |
| `permissionMode` | string | `default`, `plan`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions` |
| `maxTurns` | int | Cap agentic turns |
| `skills` | list | **Preloaded** skill names (full content injected at start) |
| `mcpServers` | list | Per-agent MCP (names or inline config) |
| `hooks` | object | Scoped lifecycle hooks |
| `memory` | string | `user`, `project`, `local` |
| `background` | bool | Always run as background task |
| `effort` | string | `low`, `medium`, `high`, `max` |
| `isolation` | string | `"worktree"` for temp git worktree |
| `initialPrompt` | string | Auto first turn when agent is main session agent |
| `color` | string | CLI color (e.g. `green`) |

**Gotcha:** Subagents **cannot** spawn other subagents via raw bash — use the **Agent** tool with explicit `subagent_type`.

---

## Claude Code — Skills (`.claude/skills/<name>/SKILL.md`)

**13 frontmatter fields** (overlap with commands):

| Field | Type | Notes |
|-------|------|--------|
| `name` | string | Defaults to folder name; also `/slash` name |
| `description` | string | **Trigger for the model** — when should it fire? Not a generic summary |
| `argument-hint` | string | Autocomplete hint |
| `disable-model-invocation` | bool | `true` = manual only |
| `user-invocable` | bool | `false` = hide from `/` menu (preload-only) |
| `allowed-tools` | string | Fewer permission prompts when active |
| `model` / `effort` | string | Override for this skill |
| `context` | string | `fork` = isolated subagent |
| `agent` | string | Subagent type when `context: fork` |
| `hooks` | object | Scoped hooks |
| `paths` | list / string | Globs — auto-activate only when editing matching files |
| `shell` | string | `bash` (default) or `powershell` (needs `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`) |

**Progressive disclosure:** Use subfolders — `references/`, `scripts/`, `examples/` — keep `SKILL.md` lean; add a **Gotchas** section (highest signal).

**Skill authoring (team tips):** Description = *when to fire*; avoid obvious filler; prefer goals + constraints over rigid step lists; embed scripts so the model composes instead of reinventing boilerplate; optional `` !`command` `` blocks inject live shell output on invocation.

---

## Claude Code — Commands (`.claude/commands/*.md`)

Same frontmatter family as skills, plus **`paths`** for file-scoped auto-load. Use **commands** for repeatable inner-loop workflows (checked into git); use **agents** for isolated compute / specialized tool sets.

---

## Agent Skills (Cursor `SKILL.md` in skills dir)

- **Trigger:** user asks for skill domain (e.g. “create a rule”)
- **Steps:** numbered procedure, pitfalls, examples
- **No secrets** in skill files

---

## Good rule / memory content

> [!tip] **Invariant > essay** — “Never `replies(count)`” beats long PostgREST theory.

---

## Anti-patterns

- Duplicating **`CLAUDE.md`** verbatim in 5 rules — use links
- Conflicting rules — **merge** into one source of truth
- **Vague subagent prompts** — e.g. “launch” misread as bash; be explicit about tools
- **Over-long skills** — split into `references/`; model ignores walls of text
- **Obvious skill text** — focus on what changes default behavior
- **Railroading** — goals + constraints beat 40-step scripts (unless compliance requires it)

---

## Testing rules

- After adding rule: run **one** representative task; verify agent follows constraint

---

## Official built-ins (Claude Code)

- **Agents:** `general-purpose`, `Explore`, `Plan`, `statusline-setup`, `claude-code-guide`
- **Bundled skills:** `simplify`, `batch`, `debug`, `loop`, `claude-api`
- **Installed extras:** [[caveman]] — token compression (`/caveman`, `/caveman-commit`, `/caveman-review`, `/caveman:compress`); hooks in `~/.claude/hooks/`; auto-activates via SessionStart hook

See [[Claude Code CLI Reference]] · [[Agent Orchestration Patterns]].

---

## See also

- [[Memory File Best Practices]] · [[Prompt Patterns for Code]] · [[Context Window Management]]
