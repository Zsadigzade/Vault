---
tags: [kb, resources, ai, mcp, cursor]
area: knowledge-base
updated: 2026-04-12
---

# AI & agent ecosystem

> [!warning] **Tokens & secrets.** Do not paste API keys into vault notes or agent chats. Prefer MCP host / OS keychain / CI secrets.

---

## MCP servers (repos & docs)

| Resource | What it does | When to use |
|----------|----------------|-------------|
| [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) | Supabase DB, migrations, Edge Functions, advisors | Schema-aware agent sessions |
| [Supabase MCP docs](https://supabase.com/docs/guides/getting-started/mcp) | Hosted MCP, OAuth, `read_only` params | Dashboard setup |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | GitHub API via MCP | Issues, PRs, code search from agent |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Reference implementations (filesystem, fetch, etc.) | Patterns for custom MCP |

> [!tip] **Postgres MCP:** search for community servers (e.g. read-only SQL) if you need generic Postgres without Supabase — **vet** permissions before connecting to prod.

---

## Cursor & rules discovery

| Resource | What it does | When to use |
|----------|----------------|-------------|
| [cursor.directory](https://cursor.directory/) | Community rules, prompts, MCP ideas | Starting point for `.cursor/rules` patterns |
| [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | Curated rule snippets | Copy ideas — adapt to your stack |
| Repo **`.cursor/rules`** | Project-specific always-on constraints | BRUH canonical agent behavior |

---

## Agent skills (Cursor)

| Resource | What it does | When to use |
|----------|----------------|-------------|
| Cursor **Skills** (`SKILL.md`) | Procedural playbooks the agent can load | Repeatable workflows (deploy, triage) |
| [[Rules & Skills Authoring]] | Vault guidance | Authoring conventions |
| [[caveman]] | Token compression for Claude Code + Cursor; ~75% fewer output tokens | Active every session — cuts cost + speeds responses |

### Claude Skills (Git — not in vault)

| Resource | What it does | When to use |
|----------|----------------|-------------|
| [[Claude Skills Library (local)]] | **Clone** [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) locally — read nested `SKILL.md` | Non-BRUH workflows; full tools/manifests → Claude marketplace |
| [[Claude Skills Library — compact index]] | How to **find** `SKILL.md` (search / PowerShell list) | No path table anymore |
| [[External Git playbooks — README index]] | Repo + README links | Quick orientation |
| BRUH `claude-skills-library-router.mdc` | Cursor rule: default clone `Desktop\claude-skills` | Same routing from BRUH workspace |

**Claude Code:** `/plugin marketplace add alirezarezvani/claude-skills` for complete packages (details in [[Claude Skills Library (local)]]).

---

## Prompt & review patterns

| Pattern | Notes |
|---------|--------|
| **Invariant first** | State non-negotiables (RLS, auth, keyboard) before asking for edits |
| **Scope bound** | List files/folders; avoid whole-repo dumps |
| **Test command** | Ask for `npx vitest run <path>` after risky changes |
| **Security pass** | Dedicated prompt: secrets, SSRF, authz — see [[AI-Assisted Code Review]] |

---

## AI coding assistants (compare mentally)

| Tool | Notes |
|------|--------|
| **Cursor** | IDE-integrated agent, rules, MCP |
| **Claude Code** | Terminal/agent workflows; `CLAUDE.md` project memory |
| **GitHub Copilot** | Inline + chat in VS Code ecosystem |

> [!note] Same project can use **multiple** assistants; keep **one** source of truth for invariants ([[Memory File Best Practices]], [[🏠 Home]]).

---

## Context optimization

| Resource / practice | Notes |
|-------------------|--------|
| [[Context Window Management]] | Token budget, what to paste |
| [[MCP Server Patterns]] | Small tool outputs, pagination |
| **Changelog discipline** | `Vault Updates Summary` / ADRs — agents catch up faster |

---

## See also

- [[Cursor Tips & Power Features]] · [[Prompt Patterns for Code]] · [[MCP Server Patterns]] · [[12 - MCP & External APIs]]
