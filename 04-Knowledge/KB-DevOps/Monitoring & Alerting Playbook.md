---
tags: [kb, devops, monitoring, sentry]
area: knowledge-base
updated: 2026-04-05
---

# Monitoring & alerting playbook

---

## Error tracking (Sentry)

| Practice | Detail |
|----------|--------|
| **Release health** | Track crash-free sessions per release |
| **Fingerprinting** | Group related errors; avoid noise |
| **Breadcrumbs** | Navigation + key UI actions |

Project: [[Sentry]].

**BRUH (2026-04):** Full **Sentry alert rules** (metric / session / performance thresholds) **deferred** until a **paid** Sentry tier; until then use Issues + `scripts/sentry-tail.js`. Runbook for after upgrade: repo `scripts/INCIDENT_RUNBOOK.md`.

---

## Product analytics (PostHog)

- **EU** region for this project — `eu.posthog.com`
- **Funnels** for onboarding, posting, paywall

Project: [[Analytics Dashboard]].

---

## Uptime

- **Synthetic** checks for API + landing + critical Edge Functions
- **BRUH:** Supabase **`health-check`** edge function — `GET https://gpainqlxdakaczkgozko.supabase.co/functions/v1/health-check` — expect **200** + JSON `"status":"ok"` (and optional keyword check in UptimeRobot). Full steps: repo `scripts/INCIDENT_RUNBOOK.md`.

---

## Alerting

| Good alert | Bad alert |
|------------|-----------|
| **SLO breach** — error rate &gt; X for 10m | Every single 404 |
| **Actionable** owner | “Something happened” |

---

## Runbooks

- Link **dashboards** + **rollback** steps — [[Incident Response & Debugging]]

---

## See also

- [[Feature Flags & Rollouts]] · [[CI-CD Pipeline Best Practices]]
