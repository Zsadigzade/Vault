---
tags: [deployment, vercel, cloudflare, capgo, codemagic, ota]
area: deployment
updated: 2026-04-13
---

# Deploy Targets

> [!important] **Netlify fully removed (Apr 2026).** All web properties now on Vercel. DNS on Cloudflare. GoDaddy = registrar only.

## Summary

| Target | Platform | Hosts | Trigger |
|--------|---------|-------|---------|
| Landing | Vercel (`landing`) | `bruhsocial.app`, `share.bruhsocial.app`, `www` | Git push to `main` (auto-deploy) |
| Ops admin | Vercel (`bruh-q86f`) | `admin.bruhsocial.app` | Git push to `main` |
| Analytics dashboard | Vercel (`bruh`) | `analytics.bruhsocial.app` | Git push to `main` |
| OTA update | Capgo | In-app JS bundle | `capgo-push.bat` |
| iOS native | Codemagic | TestFlight → App Store | Git tag `v*` |
| Android native | Manual / Codemagic | Google Play | Manual |

---

## Vercel (Landing)

**Project name**: `landing`
**Project ID**: `prj_QQ75DLUaa5ks1Lcois5CFcm141pQ`
**Source folder**: `landing/` (root directory setting in Vercel)
**Domains**: `bruhsocial.app` · `share.bruhsocial.app` · `www.bruhsocial.app` (→ 301 to apex)
**GitHub**: `Zsadigzade/BRUH` · branch `main` · auto-deploy on push

### Deploy (automatic on push — manual trigger if needed)
```bash
cd landing && npx vercel --prod
```

### Domain Routing (`landing/vercel.json`)
| Path | Serves |
|------|--------|
| `/u/:username/:postId` | `u.html` (200 rewrite — deep link) |
| `/u/:username` | `u.html` (200 rewrite — deep link) |
| `/auth/callback` | `auth/callback.html` (200 rewrite) |
| everything else | static file or `index.html` |

### Service Worker Killer
`landing/sw.js` kills all stale service workers. Served with `Cache-Control: no-store`. `index.html` served with `Clear-Site-Data: "cache", "storage"`.

### DNS Configuration
**DNS**: Cloudflare (`alexia.ns.cloudflare.com` / `harvey.ns.cloudflare.com`)
**Registrar**: GoDaddy (nameservers only — no DNS management there)
Full canonical record set → memory `dns_records.md`

#### Add/edit DNS records
Cloudflare dashboard → `bruhsocial.app` zone, or API:
```bash
curl -X POST \
  -H "Authorization: Bearer <cf_token>" \
  -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"sub","content":"cname.vercel-dns.com","proxied":false,"ttl":3600}' \
  "https://api.cloudflare.com/client/v4/zones/7d072cd53d25db06302fd5f2d3e51143/dns_records"
```
> [!warning] Always set `"proxied": false` for all A/CNAME records pointing to Vercel — orange cloud breaks Vercel SSL verification.

---

## Vercel (Ops Admin + Analytics)

Two projects from GitHub repo `Zsadigzade/BRUH`:

| Project | Root folder | Domain | Build cmd |
|---------|-------------|--------|-----------|
| Ops admin | `admin-web/` | `admin.bruhsocial.app` | `npm run build:admin` |
| Analytics | `dashboard/` | `analytics.bruhsocial.app` | Vercel default |

Auto-deploys on push to `main`.

### Admin Env Vars (Vercel)
```
VITE_SUPABASE_URL
VITE_SUPABASE_ANON_KEY  ← real values, not placeholders
```
Add `https://admin.bruhsocial.app` to Supabase Auth redirect URLs if using OAuth/magic link for ops logins.

### CI/CD (GitHub Actions)

| Workflow | Triggers | Runner detail |
|----------|----------|----------------|
| **`vercel-admin-web.yml`** | `push` to `main` when `admin-web/**`, shared `src/**`, root lockfiles, etc. change | **Node 22**; `actions/checkout` + `setup-node`; job runs from **repo root** |
| **`vercel-dashboard.yml`** | `push` to `main` when `dashboard/**` changes | Same; **`VERCEL_DASHBOARD_PROJECT_ID`** secret (not admin `VERCEL_PROJECT_ID`) |

**Critical:** Vercel project **Root Directory** is already `admin-web` or `dashboard`. Do **not** set `working-directory:` to those folders in the workflow — CLI cwd would double the path (`admin-web/admin-web` / `dashboard/dashboard`) and fail.

**Dashboard job:** optional secret preflight step; deploy uses **`npx vercel deploy --prod`** (remote build on Vercel). See repo `scripts/INCIDENT_RUNBOOK.md` for secret setup notes.

---

## Capgo OTA

**App ID**: `com.bruh.app`
**Dashboard**: `https://web.capgo.app`
**Auth header**: raw API key in `authorization` — **NO `Bearer` prefix** (Bearer → `invalid_apikey`)

### Push Flow (`capgo-push.bat`)
```
1. Load env (scripts/load-local-api-env.bat → CAPGO_API_KEY from .cursor/.env.mcp.local)
2. Bump package.json patch version
3. npm run build (production Vite build)
4. npx cap sync
5. npx @capgo/cli bundle upload --apikey $CAPGO_API_KEY [--ignore-metadata-check]
```

> [!warning] `capgo-push.bat` does **NOT** commit or push to git. OTA and git are separate. Commit the version bump manually when ready.

**`--ignore-metadata-check`**: Use when local `node_modules` versions differ from channel baseline after Capacitor/plugin upgrades (safe when store binary already matches or change is JS-only).

### Version Sync Rule
> [!warning] NEVER manually upload to Capgo without bumping `package.json` first.
`__APP_VERSION__` is set from `npm_package_version` at Vite build time. Mismatch → Admin OTA display shows wrong version.

### capacitor.config.ts Capgo Settings
```ts
plugins: {
  CapacitorUpdater: {
    appId: "com.bruh.app",   // ← Capgo App ID (different from iOS bundle ID)
    autoUpdate: true,
    appReadyTimeout: 45000,  // 45s — prevents rollback on slow devices
  }
}
```

### Force OTA (Admin → Overview tab)
```
Admin clicks "Force Update"
  → AdminFeatureFlags.tsx: getSession() → if no access_token → refreshSession()
  → supabase.functions.invoke("capgo-proxy", { body: { minUpdateVersion }, headers: { Authorization: `Bearer ${accessToken}` } })
  → capgo-proxy edge fn: is_admin() check → POST https://api.capgo.app/channel/
  → Capgo forces all devices to update
```

**`capgo-proxy` config.toml**: `verify_jwt = false` (edge fn handles its own auth via `is_admin()`).

### Bundle Upload Endpoint
```
POST https://api.capgo.app/channel/
body: { version, app_id, channel: "production", disableAutoUpdateUnderNative: true }
```

---

## Codemagic CI (iOS)

### Trigger
Auto-builds on git tags matching `v*`:
```bash
git tag v1.0.68
git push origin v1.0.68
# → Codemagic: build → sign → upload to TestFlight
# → Manual: submit from App Store Connect
```

### Required Secrets in Codemagic
| Secret | Status |
|--------|--------|
| Code signing certificate | ✅ Uploaded |
| Provisioning profile | ✅ Uploaded |
| `CM_KEYSTORE_PASSWORD` | ⚠️ Pending (Android) |
| `CM_KEY_ALIAS` | ⚠️ Pending (Android) |
| `CM_KEY_PASSWORD` | ⚠️ Pending (Android) |

**Android**: Manual-only (Codemagic does not auto-trigger Android builds).

---

## Supabase Edge Functions Deploy

```bash
# Deploy single function
npx supabase functions deploy <function-name> --project-ref gpainqlxdakaczkgozko

# Deploy all
npx supabase functions deploy

# List deployed
npx supabase functions list
```

After changing `supabase/config.toml` (e.g. `verify_jwt`), redeploy affected function.

---

## See also

- [[Commands & Scripts]] · [[Capgo OTA]] · [[Codemagic CI]]
- [[MOC — BRUH product]] · [[🏠 Home]] · [[SITEMAP]]
