---
tags: [kb, security, npm, supply-chain]
area: knowledge-base
updated: 2026-04-04
---

# Dependency & supply chain security

---

## Lockfiles

| Practice | Why |
|----------|-----|
| **Commit** `package-lock.json` / `pnpm-lock.yaml` | Reproducible installs |
| **CI** `npm ci` | Fails on lock mismatch — catches drift |

---

## Auditing

```bash
npm audit
npm audit fix   # review — not all “fixes” are safe major bumps
```

Pair with **Dependabot** / **Renovate** PRs; merge on green tests.

---

## New dependencies checklist

1. **Maintenance** — last publish, issues, bus factor
2. **Transitive weight** — `npm ls <pkg>`
3. **Alternatives** — can you use platform API?

---

## Typosquatting & install scripts

- Review **`postinstall`** scripts on new packages
- Pin **GitHub tarball** deps carefully

---

## SBOM & compliance

- Export SBOM for enterprise / App Store questionnaires where required

---

## See also

- [[Security Scanning & Audit Tools]] · [[OWASP Mobile Top 10]] (M2)
