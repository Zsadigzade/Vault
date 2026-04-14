---
tags: [reference, dns, infrastructure, cloudflare, vercel]
area: reference
updated: 2026-04-14
---

# DNS Records — bruhsocial.app

Migrated from Netlify NS → **Cloudflare** (Apr 2026). Nameservers: `alexia.ns.cloudflare.com` / `harvey.ns.cloudflare.com`. GoDaddy = registrar only.

> [!warning] All A/CNAME records must be **grey cloud (DNS only)** in Cloudflare — never orange-cloud proxied (breaks Vercel SSL verification).

---

## A / CNAME

| Type | Name | Value |
|------|------|-------|
| A | `bruhsocial.app` | `76.76.21.21` (Vercel) |
| CNAME | `admin.bruhsocial.app` | `a191df88897774c3.vercel-dns-017.com.` |
| CNAME | `analytics.bruhsocial.app` | `c8f692f5cc8b43e2.vercel-dns-017.com.` |
| CNAME | `share.bruhsocial.app` | `cname.vercel-dns.com` |
| CNAME | `www.bruhsocial.app` | `cname.vercel-dns.com` |

---

## MX (email routing)

| Type | Name | Value | Priority |
|------|------|-------|----------|
| MX | `bruhsocial.app` | `inbound-smtp.eu-west-1.amazonaws.com` | 10 |
| MX | `send.bruhsocial.app` | `feedback-smtp.eu-west-1.amazonses.com` | 10 |

---

## TXT (email auth + BIMI)

| Type | Name | Value |
|------|------|-------|
| TXT | `bruhsocial.app` | `v=spf1 include:_spf.resend.com ~all` |
| TXT | `send.bruhsocial.app` | `v=spf1 include:amazonses.com ~all` |
| TXT | `_dmarc.bruhsocial.app` | `v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@bruhsocial.app; sp=quarantine; aspf=s;` |
| TXT | `resend._domainkey.bruhsocial.app` | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmaIsiF4Jrbg5Wo1KH0URg+FsBHKSAFVVIHNi6GOdkm13CmDYSdMDM+Nw0qMgeTQYRC99yWEKRAk6J2GG/f4XX2vYy22jNbd+euN1r3dXK+4qVsi9kk+0fIT/00oNK8OChe2l/eUXZm8es7EHNiA+h/J//FqAjiVn128yEy3DAAQIDAQAB` |
| TXT | `default._bimi.bruhsocial.app` | `v=BIMI1; l=https://bruhsocial.app/bimi-logo.svg;` |

---

## Notes

- **Resend** handles outbound email via `resend._domainkey` DKIM + SPF
- **AWS SES** handles inbound email (`inbound-smtp.eu-west-1.amazonaws.com`)
- `send.bruhsocial.app` subdomain = SES bounce/complaint feedback

---

## See also

- [[Deploy Targets]] · [[🏠 Home]]
