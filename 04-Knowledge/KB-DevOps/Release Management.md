---
tags: [kb, devops, release, versioning]
area: knowledge-base
updated: 2026-04-04
---

# Release management

---

## Versioning

| Scheme | Notes |
|--------|-------|
| **SemVer** `MAJOR.MINOR.PATCH` | Communicates breaking vs fix |
| **Build numbers** | Monotonic per store (iOS CFBundleVersion, Android `versionCode`) |

---

## Changelog

- **User-facing** “What’s New” ≠ internal commit log
- Call out **migration** steps for self-host ops if any

---

## Branches

| Flow | When |
|------|------|
| **Trunk-based** + short PRs | Small team velocity |
| **Release branch** | Store submission freeze window |

---

## Hotfix

- Branch from **tag**; cherry-pick; fast-track CI; **post-mortem** if sev-1

---

## Native vs OTA

- **Native** release for permissions, plugins, URL schemes
- **OTA** for JS/CSS — [[OTA Update Strategies]]

---

## Communication

- **Status page** / Discord for long outages — [[Incident Response & Debugging]]

---

## See also

- [[CI-CD Pipeline Best Practices]] · [[App Store Submission Checklist]]
