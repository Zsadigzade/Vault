---
tags: [meta, git, vendors, agents]
area: meta
updated: 2026-04-13
tldr: "Submodule, sparse mirror, or shallow clone snapshot into inbox."
---

# Git import protocol

## TL;DR

Three supported ways to pull external repos into the vault without manual paste.

## 1) Git submodule (active tracking)

- Path: `05-Projects/_vendor/<repo-name>/`
- Command: `git submodule add <url> "05-Projects/_vendor/<repo-name>"`
- Use when you need **pinned SHA** and occasional `git pull` inside submodule.

## 2) Sparse checkout (read-only reference)

- Clone with `--filter=blob:none` + sparse-checkout for `/docs` only.
- Good for large monorepos where you only want documentation.

## 3) Shallow snapshot → inbox

- `git clone --depth 1 <url> /tmp/x && copy docs → vault`
- Write summary note in `06-Inbox/pending/upstream-snapshot-YYYY-MM-DD.md` with **LICENSE** pointer and **commit SHA**.

## Policy

- **No secrets** from cloned `.env` into vault.
- Prefer **inbox first** for synthesized notes; promote after batch review.

## See also

- [[External Git playbooks — README index]]
