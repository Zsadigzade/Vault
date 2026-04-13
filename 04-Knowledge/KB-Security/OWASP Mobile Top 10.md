---
tags: [kb, security, owasp, mobile]
area: knowledge-base
updated: 2026-04-04
---

# OWASP Mobile Top 10 (2024)

> [!note] Official reference: [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10). Below: **M1–M10** with **Capacitor + React + Supabase** angles.

---

## M1 — Improper credential usage

| Risk | Mitigation |
|------|------------|
| Hardcoded API keys in JS bundle | **Never** ship secrets in client; use env at **build** for public anon keys only |
| Embedded admin tokens | Server-side / Edge Functions only |

---

## M2 — Inadequate supply chain security

| Risk | Mitigation |
|------|------------|
| Compromised npm packages | Lockfile, `npm audit`, Dependabot/Renovate, review new deps |

See [[Dependency & Supply Chain Security]].

---

## M3 — Insecure authentication / authorization

| Risk | Mitigation |
|------|------------|
| Client-only “is admin” flags | Enforce on **server** (RLS, RPC `SECURITY DEFINER` with checks) |
| Broken session handling | Align with Supabase session refresh; don’t roll crypto ad hoc |

Project: [[Authentication]] · [[Security Reference]].

---

## M4 — Insufficient input/output validation

| Risk | Mitigation |
|------|------------|
| XSS in WebView | Sanitize rich text; CSP; avoid `dangerouslySetInnerHTML` |
| SQL injection | Parameterized queries (PostgREST/Supabase client — no string concat) |
| Command injection in Edge | Validate/sanitize inputs; no shell |

---

## M5 — Insecure communication

| Risk | Mitigation |
|------|------------|
| Cleartext HTTP | HTTPS only; **certificate pinning** rarely needed for SPAs — focus on correct URLs |
| Mixed content | Block in production |

---

## M6 — Inadequate privacy controls

| Risk | Mitigation |
|------|------------|
| Over-collection | Minimize PII; document in privacy policy / App Store labels |
| Logs leaking PII | Scrub Sentry/console |

---

## M7 — Insufficient binary protections

| Risk | Mitigation |
|------|------------|
| Reverse engineering | Assume **client is untrusted**; secrets & rules live server-side |
| Debug builds in store | Release signing, strip debug symbols where appropriate |

---

## M8 — Security misconfiguration

| Risk | Mitigation |
|------|------------|
| Open CORS / wildcard origins | Lock Edge Function CORS to known origins |
| Default credentials | Rotate Supabase keys; restrict dashboard access |

---

## M9 — Insecure data storage

| Risk | Mitigation |
|------|------------|
| Sensitive data in `localStorage` | Prefer native **Preferences** / Keychain for tokens where applicable |
| World-readable app files | OS-level; avoid logging secrets |

See [[Secure Storage on Mobile]].

---

## M10 — Insufficient cryptography

| Risk | Mitigation |
|------|------------|
| Custom ciphers | Use platform / library defaults (TLS, Supabase Auth) |
| Weak randomness | Use crypto APIs for tokens server-side |

---

## See also

- [[Supabase Security Hardening]] · [[API Security & Rate Limiting]] · [[Secrets Management Guide]]
- [[Dependency & Supply Chain Security]]
