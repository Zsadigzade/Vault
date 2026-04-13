---
tags: [kb, devops, ota, capgo]
area: knowledge-base
updated: 2026-04-04
---

# OTA update strategies

> [!tip] BRUH uses **Capgo** — [[Capgo OTA]] · `CLAUDE.md` for scripts.

---

## Channels

| Channel | Use |
|---------|-----|
| **Production** | All users |
| **Beta** | Testers / internal |
| **Canary** | Small % — pair with analytics |

---

## Rollback

- Keep **prior bundle** available; **force** downgrade path if critical bug
- **Native** binary mismatch — know minimum app version per OTA

---

## Bundle hygiene

- **Smaller JS** = faster download on cellular — [[Bundle Size & Code Splitting]]

---

## Compliance

- Apple **guidelines** on what can change OTA vs requires store update — don’t ship binary-level changes via web OTA

---

## Communication

- **Silent** updates vs **what’s new** modal — balance annoyance vs awareness

---

## See also

- [[Release Management]] · [[Feature Flags & Rollouts]]
