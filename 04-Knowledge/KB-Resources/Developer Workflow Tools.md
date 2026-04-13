---
tags: [kb, resources, devtools, cli]
area: knowledge-base
updated: 2026-04-04
---

# Developer workflow tools

> [!tip] **For agents:** Prefer **repo-documented** commands (`package.json` scripts) over global CLI assumptions on Windows.

---

## CLI — general

| Tool | What it does | When to use |
|------|--------------|-------------|
| [GitHub CLI `gh`](https://cli.github.com/) | PRs, issues, releases from terminal | Review/merge without full web UI |
| [ripgrep `rg`](https://github.com/BurntSushi/ripgrep) | Fast code search | Faster than IDE search on huge trees |
| [`jq`](https://jqlang.org/) | JSON filter/transform | Pipe API/MCP JSON in scripts |
| [`bat`](https://github.com/sharkdp/bat) | Syntax-highlighted `cat` | Read files in terminal |
| [`fzf`](https://github.com/junegunn/fzf) | Fuzzy finder | Shell history, file pickers |
| [lazygit](https://github.com/jesseduffield/lazygit) | TUI for Git | Stage/commit/rebase quickly |

---

## Node / JS versions

| Tool | What it does | When to use |
|------|--------------|-------------|
| [fnm](https://github.com/Schniz/fnm) | Fast Node version manager | Windows-friendly alternative to nvm |
| [nvm](https://github.com/nvm-sh/nvm) | Node version switch | Unix/mac default for many teams |

---

## API testing (Postman alternatives)

| Tool | What it does | When to use |
|------|--------------|-------------|
| [Bruno](https://www.usebruno.com/) | Git-friendly API collections | Store requests beside repo |
| [Hoppscotch](https://hoppscotch.io/) | Browser HTTP client | Quick probes without install |

---

## Database clients

| Tool | What it does | When to use |
|------|--------------|-------------|
| **Supabase Studio** | Table editor, SQL, logs | First stop for Supabase projects |
| [DBeaver](https://dbeaver.io/) | Universal SQL client | Raw SQL, ER diagrams |
| [pgAdmin](https://www.pgadmin.org/) | Postgres admin | Deep server admin |

---

## VS Code / Cursor extensions (stack-aligned)

| Extension area | Examples / notes |
|----------------|------------------|
| **TypeScript** | Built-in TS — enable strict in `tsconfig` |
| **Tailwind** | Tailwind CSS IntelliSense |
| **ESLint** | Project ESLint flat config |
| **Vitest** | Vitest runner integration |
| **Git** | GitLens (blame/history) — optional |

> [!note] Pin versions in **workspace recommendations** (`.vscode/extensions.json`) if the team should stay aligned.

---

## Git hygiene

| Practice / tool | Notes |
|-----------------|--------|
| **Conventional Commits** | Machine-readable history; works with changelog tools |
| [commitlint](https://github.com/conventional-changelog/commitlint) | Enforce message format in CI |
| [git-cliff](https://github.com/orhun/git-cliff) | Changelog from conventional commits | Release notes |

---

## Windows terminal tips

| Tip | Notes |
|-----|--------|
| **Windows Terminal** | Tabs, panes, Unicode — default shell PowerShell |
| **WSL2** | Use when Unix-native scripts/docs assume bash |
| **Repo rule** | BRUH: use `npx supabase` / `npx netlify` — global CLI can EPERM on Windows |

---

## Agent output compression

| Tool | What it does | When to use |
|------|--------------|-------------|
| [[caveman]] | Cuts ~75% agent output tokens; `/caveman`, `/caveman-commit`, `/caveman-review`, `/caveman:compress` | Active via SessionStart hook — just use it |

---

## See also

- [[📚 Knowledge Base]] · [[CI-CD Pipeline Best Practices]] · [[Performance & Debugging Tools]] · [[caveman]]
