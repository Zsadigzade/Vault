---
tags: [operations, tools, github-education, devtools, services]
area: operations
updated: 2026-04-14
---

# Developer Tools & GitHub Education

> [!success] **All services below are ACTIVE and enabled.** AI agents may use, query, and reference them whenever relevant — no need to ask before using.

---

## Active Services

### Must-Have (fills real gaps)

| Service | Purpose | Plan | Notes |
|---------|---------|------|-------|
| **Sentry** | Error tracking, session replays, crash reports | GitHub Education student plan — 50K errors / 500 replays free | EU region (`de.sentry.io`) · org `bruh-social` · project `react-native` · detail: [[Sentry]] |
| **BrowserStack** | Real iOS + Android device testing (no simulator) | Free Automate Mobile — 1yr GitHub Education | Direct BRUH use — test on real devices; Automate supports Appium/WebDriver |
| **Appfigures** | App Store + Play analytics: downloads, ratings, ASO trends | Free 1yr GitHub Education | Live app metrics; use for store performance, keyword tracking |
| **Doppler** | Centralized secrets management (replaces scattered `.env.mcp.local` / env vars) | Free Team — GitHub Education | CLI at `~/.doppler-cli/doppler`; project `bruh`; envs `prd` + `dev`; 38 secrets; Codemagic token `codemagic-ci-2` |

### Should-Have (zero-effort wins)

| Service | Purpose | Plan | Notes |
|---------|---------|------|-------|
| **Codecov** | Coverage reporting on ~161 Vitest tests; CI integration | GitHub Education | Connect to `Zsadigzade/BRUH`; upload token in CI (Codemagic) |
| **POEditor** | Localization pipeline for i18n — proper translator workflow | Free Plus 1yr GitHub Education | i18n already exists in repo; POEditor gives structured key management + export |
| **Imgbot** | Auto-optimizes images in repo via PRs — zero effort | GitHub Education (free) | Runs automatically on push; submits optimization PRs |
| **CodeScene** | Tech debt analysis, code quality, hotspot detection on private repo | 6mo free GitHub Education | Project `79074`; 10 files refactored on `copilot/current-version-20260413` |
| **GitLens** | Git blame / history / codelens in VS Code | Free 6mo GitHub Education | VS Code extension; use for authorship + history while editing |
| **Termius** | SSH client for mobile — connects to DO vault server | Free Pro GitHub Education | DO server: `46.101.161.176` · `root` + `id_ed25519` · detail: [[DO Vault Server]] |

---

## Doppler Details

```bash
# CLI location
~/.doppler-cli/doppler

# Fetch secrets for local dev
doppler run --project bruh --config dev -- npm run dev
```

| Key | Value |
|-----|-------|
| Project | `bruh` |
| Environments | `prd`, `dev` |
| Secret count | 38 |
| Codemagic token name | `codemagic-ci-2` |

> [!note] Doppler is the long-term replacement for secrets currently in `.cursor/.env.mcp.local` and Windows env vars. Migrate incrementally — no hard cutover date yet.

---

## BrowserStack Details

- Use **Automate** (not Live) for programmatic test runs
- Combine with Vitest + Appium for end-to-end native testing
- Key scenarios: deep link handling, keyboard behavior, ad rendering on real iOS/Android

---

## Appfigures

- Tracks App Store (iOS) + Google Play (Android) downloads, ratings, reviews, and ASO keyword ranks
- Useful for post-launch monitoring: spot rating drops, track install velocity, compare version performance

---

## Codecov Setup (TODO)

1. Add `CODECOV_TOKEN` to Codemagic `secrets` group
2. Add coverage upload step to Codemagic workflow after `npm run test`
3. Badge in `README.md`

---

## See also

- [[Sentry]]
- [[DO Vault Server]]
- [[Testing]]
- [[Codemagic CI]]
- [[12 - MCP & External APIs]]
- [[🏠 Home]]
