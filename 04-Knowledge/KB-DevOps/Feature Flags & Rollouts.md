---
tags: [kb, devops, feature-flags, experimentation]
area: knowledge-base
updated: 2026-04-04
---

# Feature flags & rollouts

---

## Use cases

| Flag type | Example |
|-----------|---------|
| **Release** | Hide unfinished UI |
| **Ops kill switch** | Disable payments provider |
| **Experiment** | A/B paywall copy |

---

## Storage

| Client flag | Server flag |
|-------------|-------------|
| Fast; can be tampered | Authoritative for **money** + **security** |

> [!warning] **Never** gate **authorization** with client-only flags.

---

## PostHog

- Feature flags + experiments — EU endpoint for BRUH

---

## Cleanup

- **Remove** dead flags — debt accumulates fast

---

## OTA synergy

- Ship **flagged** UI via Capgo; enable remotely when ready — [[OTA Update Strategies]]

---

## See also

- [[Monitoring & Alerting Playbook]] · [[Release Management]]
