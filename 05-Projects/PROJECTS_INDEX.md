---
tags: [projects, index, agents]
area: projects
updated: 2026-04-13
tldr: "All active projects live here. Each project has its own HOME + CONSTITUTION."
---

# Projects Index

## TL;DR

- Active projects live under `05-Projects/[PROJECT_NAME]/`.
- Each project has its own `HOME.md` (entry hub) and optionally a `reference/CONSTITUTION.md` (project laws).
- Start any project session at the project HOME, not the vault HOME.

## Active projects

| Project | Home | Status | Stack |
|---------|------|--------|-------|
| **BRUH** | [[BRUH_PROJECT_HOME]] | Active (v1.1.17) | React + Capacitor + Supabase |

---

## Starting a new project

1. Run the `new-project-bootstrap` workflow:
   ```
   python scripts/run_workflow.py --id wf-new-project-bootstrap-001
   ```
   Or use the Claude Code slash command: `/new-project`

2. The workflow creates:
   ```
   05-Projects/[NAME]/
   ├── HOME.md              (from Templates/Project Bootstrap)
   ├── overview/
   │   └── Project Overview.md
   ├── reference/
   │   └── CONSTITUTION.md  (project-specific laws)
   └── sessions/
       └── SESSION_HANDOFF.md
   ```

3. Add the project to the table above.

---

## Project folder conventions

| Subfolder | Purpose |
|-----------|---------|
| `overview/` | High-level: what, why, who, current state |
| `architecture/` | How it's built; decisions; INVARIANTS |
| `database/` | Schema, migrations, RPCs |
| `security/` | Threat model, controls, audit history |
| `features/` | Per-feature docs |
| `deployment/` | CI/CD, scripts, environment configs |
| `operations/` | Dashboards, incidents, testing |
| `reference/` | Critical gotchas, coding patterns, tombstones |
| `sessions/` | SESSION_HANDOFF, extended notes |

---

## Multi-project agent routing

When working across projects, [[CoS]] loads:
1. Vault `HOME.md`
2. `PROJECTS_INDEX.md` (this file)
3. Target project `HOME.md`

Never load two project CONSTITUTIONs simultaneously — laws may conflict.

---

## _vendor/

`05-Projects/_vendor/` — imported external content (submodules, cloned repos used as reference). See [[GIT_IMPORT_PROTOCOL]] for how to add vendor content.
