---
tags: [operations, sentry, errors, monitoring]
area: operations
updated: 2026-04-05
---

# Sentry

---

## Project (EU)

| Key | Value |
|-----|--------|
| **Region** | EU (`de.sentry.io`) |
| **Org slug (API)** | `bruh-social` |
| **Project slug** | `react-native` |
| **API base** | `https://de.sentry.io/api/0/` |

> [!warning] **DSN** and **auth tokens** live in env (e.g. `VITE_SENTRY_DSN`, `SENTRY_AUTH_TOKEN` in `.cursor/.env.mcp.local`) — **do not** paste into chat or commits. Example issue URL pattern: `/api/0/projects/bruh-social/react-native/issues/`.

---

## Client (`src/main.tsx`)

- Initialize only when `VITE_SENTRY_DSN` is set and **`import.meta.env.PROD`**.  
- **ignoreErrors:** e.g. service worker registration noise on localhost.  
- Helpers: `src/lib/errorLogging.ts`, `src/lib/sentryUser.ts`.

---

## Noise filters (examples)

- Clipboard / `readText` errors on Android (PostHog / clipboard experiments).  
- Cached PWA CSP `unsafe-eval` messages from old builds.  
- `submit_report` “Cannot report yourself” — expected.  
- Klipy upstream errors — often downgraded / fallback to GIPHY.

---

## MCP / API checks

Use EU host + org/project **slugs** with token from env — see [[12 - MCP & External APIs]] · [[Agent MCP — live verification]] (proactive MCP use).

---

## Alert rules (deferred on free tier)

- **Product:** Sentry **metric / session / performance** alerts (error spike, crash-free, p95, etc.) often require a **paid plan**. **Deferred** until upgraded.
- **Until then:** triage from **Issues** in `de.sentry.io` and local tail **`node scripts/sentry-tail.js`** (token in env — script header).
- **After upgrade:** step-by-step EU wizard + optional API bootstrap in repo **`scripts/INCIDENT_RUNBOOK.md`** and **`scripts/sentry-bootstrap-alerts.mjs`** (`SENTRY_ALERT_NOTIFY_EMAIL` for metric actions). Project slug stays **`react-native`** (matches `vite.config.ts`).

---

## See also

- [[Security Reference]]
- [[Bug History & Lessons]]
- [[🏠 Home]]
