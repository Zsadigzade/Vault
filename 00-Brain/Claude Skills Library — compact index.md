---
tags: [meta, agents, skills, git, agent:router]
area: meta
status: active
updated: 2026-04-13
---

# Claude Skills Library — finding `SKILL.md`

> **Deprecated:** giant path table (vault bundle) **removed** — folder `claude-skills-main/` no longer in vault.

## Quick lookup

1. **GitHub (no clone):** [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) → search repo for **`SKILL.md`** or browse folders (`engineering/`, `marketing-skill/`, …).
2. **Local clone:** see [[Claude Skills Library (local)]] — then Cursor / IDE **search in files** `SKILL.md`.
3. **Regenerate a path list (optional):** from clone root:
   ```powershell
   Get-ChildItem -Recurse -Filter SKILL.md | ForEach-Object { $_.FullName }
   ```

## See also

- [[Claude Skills Library (local)]] · [[External Git playbooks — README index]] · [[MOC — Third-party tools & playbooks]]
