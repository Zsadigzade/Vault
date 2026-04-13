# Caveman — Token Compression System

**Source:** https://github.com/JuliusBrussee/caveman  
**Local reference copies (playbooks):** `~/.claude/skills/caveman/SKILL.md` and related `caveman-*` skills under `~/.claude/skills/`  
**Purpose:** Cuts ~65-75% output tokens while keeping full technical accuracy. Agent speaks like caveman.

> No full upstream clone in this vault — use GitHub or local install paths above. Hub: [[MOC — Third-party tools & playbooks]].

---

## What's Installed

| Target | Location | Status |
|--------|----------|--------|
| Claude Code hooks | `~/.claude/hooks/caveman-*.js` | ✅ Installed |
| Claude Code skills | `~/.claude/skills/caveman*/SKILL.md` | ✅ Installed |
| Claude Code settings | `~/.claude/settings.json` — SessionStart + UserPromptSubmit hooks + statusline | ✅ Wired |
| Cursor (BRUH) | `BRUH/.cursor/rules/caveman.mdc` (`alwaysApply: true`) | ✅ Installed |

---

## Claude Code Usage

Auto-activates every session via SessionStart hook. Statusline shows `[CAVEMAN]` / `[CAVEMAN:ULTRA]` etc.

| Command | What |
|---------|------|
| `/caveman` | Activate full mode (default) |
| `/caveman lite` | Drop filler, keep grammar |
| `/caveman ultra` | Max compression, arrows for causality |
| `/caveman wenyan` | Classical Chinese 文言文 mode |
| `/caveman-commit` | Terse Conventional Commits, ≤50 char subject |
| `/caveman-review` | One-line PR comments: `L42: 🔴 bug: user null. Add guard.` |
| `/caveman:compress <file>` | Compress .md file to caveman prose (~46% input token savings) |
| `/caveman-help` | Quick-reference card |
| `stop caveman` | Deactivate |

---

## Cursor Usage

`caveman.mdc` has `alwaysApply: true` — auto-active in all Cursor sessions in BRUH repo.
Same commands work on-demand. No slash-command system in Cursor, but mode switching works via natural language.

---

## Other Agents

For Windsurf, Cline, Copilot, or any other agent — use the always-on snippet:

```
Terse like caveman. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop caveman" / "normal mode".
```

Add to agent's system prompt, rules file, or `.clinerules/caveman.md`.

---

## Hook Architecture (Claude Code)

```
SessionStart hook → ~/.claude/.caveman-active (writes mode)
UserPromptSubmit hook → reads /caveman commands → updates flag file
caveman-statusline.ps1 → reads flag → outputs [CAVEMAN:MODE] badge
```

Config file (optional): `%APPDATA%\caveman\config.json` → `{ "defaultMode": "lite" }`
Env var override: `CAVEMAN_DEFAULT_MODE=ultra`

---

## Caveman-Compress

Compresses CLAUDE.md / memory .md files to caveman prose to save input tokens on every session load.

```
/caveman:compress CLAUDE.md
```

Saves backup as `CLAUDE.original.md`. Only modifies prose — code blocks, URLs, paths, commands untouched.
Python 3.10+ required for CLI compress; scripts ship with upstream repo / plugin install — not duplicated in vault.

---

## Source Files (Single Source of Truth — upstream repo layout)

| File | Controls |
|------|----------|
| `skills/caveman/SKILL.md` | Behavior, intensity levels, wenyan, auto-clarity |
| `rules/caveman-activate.md` | Always-on auto-activation rule body |
| `skills/caveman-commit/SKILL.md` | Commit message behavior |
| `skills/caveman-review/SKILL.md` | Code review comment behavior |
| `caveman-compress/SKILL.md` | Compression behavior |

Same files mirrored under `~/.claude/skills/` when installed via Claude Code.
