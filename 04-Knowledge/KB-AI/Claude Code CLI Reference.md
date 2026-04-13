---
tags: [kb, ai, claude-code, cli]
area: knowledge-base
updated: 2026-04-05
---

# Claude Code CLI reference

> Condensed from [CLI reference](https://code.claude.com/docs/en/cli-reference) and community best-practice summaries. **Verify** against current docs if behavior changes.

---

## Session management

| Flag | Short | Description |
|------|-------|-------------|
| `--continue` | `-c` | Continue most recent conversation in cwd |
| `--resume` | `-r` | Resume by ID/name or picker |
| `--from-pr` | | Resume sessions linked to a GitHub PR |
| `--fork-session` | | New session ID when resuming |
| `--session-id` | | Fixed UUID for session |
| `--no-session-persistence` | | No persistence (print mode) |
| `--remote` | | New web session on claude.ai |
| `--teleport` | | Resume web session in local terminal |

---

## Model & configuration

| Flag | Description |
|------|-------------|
| `--model` | Alias (`sonnet`, `opus`, `haiku`) or full model ID |
| `--fallback-model` | Fallback when default overloaded (print mode) |
| `--betas` | Beta headers (API key users) |

---

## Permissions & security

| Flag | Description |
|------|-------------|
| `--dangerously-skip-permissions` | Skip **all** prompts — avoid; use `/permissions` allowlists |
| `--allow-dangerously-skip-permissions` | Enable bypass as an option without activating |
| `--permission-mode` | `default`, `plan`, `acceptEdits`, `bypassPermissions`, … |
| `--allowedTools` | Tools without prompt (permission rule syntax) |
| `--disallowedTools` | Removed from model context |
| `--tools` | Restrict built-in tools (`""` = none) |
| `--permission-prompt-tool` | MCP tool for permission prompts (non-interactive) |

Prefer **wildcard allow rules** in team `settings.json` (e.g. `Bash(npm run *)`) over global bypass.

---

## Output & headless

| Flag | Description |
|------|-------------|
| `--print` / `-p` | Non-interactive / SDK-style |
| `--output-format` | `text`, `json`, `stream-json` |
| `--input-format` | `text`, `stream-json` |
| `--json-schema` | Validated JSON (print) |
| `--verbose` | Verbose logging |

**SDK startup:** `--bare` can speed cold start when you explicitly pass `--system-prompt`, `--mcp-config`, `--settings` (load only what you need).

---

## System prompt

| Flag | Description |
|------|-------------|
| `--system-prompt` | Replace default system prompt |
| `--system-prompt-file` | Load from file (print) |
| `--append-system-prompt` | Append text |
| `--append-system-prompt-file` | Append file (print) |

---

## Agents & workspace

| Flag | Description |
|------|-------------|
| `--agent` | Main session uses named agent from `.claude/agents/` |
| `--agents` | Inline JSON agent definitions |
| `--teammate-mode` | `auto`, `in-process`, `tmux` |
| `--add-dir` | Extra working directories (+ permissions) |
| `--worktree` / `-w` | Isolated git worktree session |

---

## MCP & plugins

| Flag | Description |
|------|-------------|
| `--mcp-config` | JSON file or string for MCP servers |
| `--strict-mcp-config` | Only these MCP servers |
| `--plugin-dir` | Extra plugin directory (repeatable) |

---

## Budget & limits (print mode)

| Flag | Description |
|------|-------------|
| `--max-budget-usd` | Stop after spend cap |
| `--max-turns` | Cap agentic turns |

---

## Integration

| Flag | Description |
|------|-------------|
| `--chrome` | Chrome integration |
| `--no-chrome` | Disable Chrome |
| `--ide` | Auto-connect single IDE |

---

## Init & debug

| Flag | Description |
|------|-------------|
| `--init` | Run init hooks + interactive |
| `--init-only` | Init hooks then exit |
| `--maintenance` | Maintenance hooks then exit |
| `--debug` | Debug categories e.g. `api,hooks` |

---

## Settings override

| Flag | Description |
|------|-------------|
| `--settings` | Path or JSON string |
| `--setting-sources` | `user`, `project`, `local` |
| `--disable-slash-commands` | Disable skills + slash commands |

---

## Subcommands

| Command | Purpose |
|---------|---------|
| `claude` | Interactive REPL |
| `claude "query"` | REPL with initial prompt |
| `claude agents` | List agents |
| `claude auth` | Auth management |
| `claude doctor` | Diagnostics |
| `claude install` | Native build install/switch |
| `claude mcp` | MCP add/remove/list/get/enable |
| `claude plugin` | Plugins |
| `claude remote-control` | Remote control sessions |
| `claude setup-token` | Long-lived token |
| `claude update` / `upgrade` | Update CLI |

---

## Environment variables (startup shell)

| Variable | Notes |
|----------|--------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `=1` experimental agent teams |
| `CLAUDE_CODE_TMPDIR` | Temp dir override |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `=1` extra directory CLAUDE.md loading |
| `DISABLE_AUTOUPDATER` | `=1` disable auto-update |
| `USE_BUILTIN_RIPGREP` | `=0` use system ripgrep |
| `CLAUDE_BASH_NO_LOGIN` | `=1` skip login shell for Bash tool |

Many more are configurable via `settings.json` **`env`** key — see [Settings](https://code.claude.com/docs/en/settings).

---

## Interactive commands (sample)

`/plan`, `/compact`, `/clear`, `/rewind`, `/permissions`, `/mcp`, `/agents`, `/skills`, `/doctor`, `/context`, `/usage`, `/model`, `/effort`, `/security-review` (see built-in list in [slash commands](https://code.claude.com/docs/en/slash-commands)).

---

## See also

- [[Agent Orchestration Patterns]] · [[Rules & Skills Authoring]] · [[Memory File Best Practices]]
