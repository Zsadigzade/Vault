---
tags: [kb, devops, ci, cd]
area: knowledge-base
updated: 2026-04-04
---

# CI/CD pipeline best practices

---

## Speed

| Technique | Detail |
|-----------|--------|
| **Cache** | `node_modules`, Gradle, CocoaPods, derived data |
| **Parallel** | Lint/test/build matrix by platform |
| **Shallow clone** | `fetch-depth` for GitHub Actions when safe |

---

## Reliability

| Technique | Detail |
|-----------|--------|
| **Deterministic** | Lockfiles, pinned action SHAs for security |
| **Fail fast** | Lint before expensive native build |

---

## Secrets

- **Never** echo in logs — [[Secrets Management Guide]]
- **Rotate** keys used in CI

Project: [[Codemagic CI]] · [[Deploy Targets]].

---

## Artifacts

- Store **IPA/APK/AAB** with retention policy
- Upload **source maps** to Sentry in release job — [[Sentry]]

---

## Mobile-specific

- **Code signing** in secure enclave / encrypted env
- **Simulator vs device** tests — choose per cost

---

## See also

- [[Release Management]] · [[Monitoring & Alerting Playbook]]
