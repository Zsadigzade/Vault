---
tags: [kb, security, csp, headers]
area: knowledge-base
updated: 2026-04-04
---

# CSP & HTTP header security

---

## Content-Security-Policy (web / PWA)

| Directive | Typical goal |
|-----------|--------------|
| `default-src 'self'` | Baseline |
| `script-src` | Avoid `'unsafe-inline'`; use nonces/hashes for inline if needed |
| `connect-src` | Allowlist Supabase, analytics, APIs |
| `img-src` | `self` + CDN domains (Giphy, storage) |
| `frame-ancestors` | Mitigate clickjacking |

**Capacitor:** WebView loads bundled assets — CSP still helps for **remote** content and **injected** HTML.

---

## Other headers (hosting)

| Header | Purpose |
|--------|---------|
| **HSTS** | Force HTTPS (`max-age`, `includeSubDomains`) |
| **X-Content-Type-Options: nosniff** | MIME sniffing |
| **Referrer-Policy** | Reduce leakage |
| **Permissions-Policy** | Disable unused APIs |

---

## Mixed content

- Block HTTP resources on HTTPS pages — breaks silently or loudly

---

## Third-party scripts (ads, analytics)

- Ads often need **broader** `script-src` — isolate **ad** WebViews if possible (native AdMob avoids some web CSP pain)

Project: [[Monetization]] (AdMob native).

---

## See also

- [[Security Reference]] (project CSP notes) · [[Dependency & Supply Chain Security]]
