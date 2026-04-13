---
tags: [meta, agents, skills, git, external, agent:router]
area: meta
status: active
updated: 2026-04-13
---

# Claude Skills Library (Git — no vault copy)

> The **`claude-skills-main/`** folder was **removed from the vault** (2026-04-13). Playbooks stay **upstream**; agents read **`SKILL.md` from a local clone** or the GitHub UI.

## Upstream repository

| Item | Link |
|------|------|
| **Repo** | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| **README** | [github.com/alirezarezvani/claude-skills/blob/main/README.md](https://github.com/alirezarezvani/claude-skills/blob/main/README.md) |
| **License** | MIT |

**No API key** for reading public GitHub. **Optional:** Claude Code marketplace — `/plugin marketplace add alirezarezvani/claude-skills` (full package with non-markdown assets).

## Recommended local clone (Cursor / agents `Read`)

```powershell
cd $env:USERPROFILE\Desktop
git clone https://github.com/alirezarezvani/claude-skills.git
```

Default path after clone: **`%USERPROFILE%\Desktop\claude-skills`** (repo root contains domain folders + `SKILL.md` files nested inside).

- **Find a playbook:** search repo for `SKILL.md` (VS Code / Cursor search, or GitHub `t` → search file).
- **BRUH Cursor rule:** `.cursor/rules/claude-skills-library-router.mdc` — must match **your** clone path if you change the default.

## BRUH-only skills (in repo, not vault)

`BRUH/.claude/skills/` — e.g. `capacitor-native`, `supabase-patterns` — ship with the app repo.

## See also

- [[Claude Skills Library — compact index]] — how to locate `SKILL.md` without the old path table
- [[MOC — Third-party tools & playbooks]]
- [[External Git playbooks — README index]]
- [[Agent Quick Reference]]
