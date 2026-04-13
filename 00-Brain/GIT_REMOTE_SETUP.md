---
tags: [meta, git, agents, agent:hub]
area: meta
updated: 2026-04-13
tldr: "Private remote for vault; optional Git LFS for large attachments."
---

# Git remote and backup (vault)

## TL;DR

- Use **private** GitHub or GitLab repo as source of truth.
- Run `git init` once (done if `.git` exists); add remote; push `main`.
- Large binaries in `attachments/` → consider **Git LFS** (see below).

## First-time remote

```bash
cd "path/to/First Vault"
git status
git remote add origin git@github.com:YOUR_USER/your-vault-repo.git
git branch -M main
git add -A
git commit -m "chore: vault second-brain structure"
git push -u origin main
```

## Git LFS (optional)

If `attachments/` grows past ~50MB or has video/audio:

```bash
git lfs install
git lfs track "*.png" "*.jpg" "*.jpeg" "*.webp" "*.gif" "*.mp4" "*.zip"
git add .gitattributes
```

## VPS sync

Automation clone uses same remote URL (deploy key or PAT with repo scope). See `vault-automation` repo `docs/VPS_HARDENING.md`.
