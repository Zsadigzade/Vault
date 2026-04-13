---
tags: [security, apple, app-review, compliance, eula]
area: security
updated: 2026-04-03
---

# App Review History

---

## Guidelines addressed (2026-04)

| Guideline | Topic | Mitigation |
|-----------|--------|------------|
| **3.1.2(c)** | Subscriptions metadata | In-app subscription UI shows **title, length, price**; links to Terms + Privacy via `src/lib/user/links.ts` → `https://share.bruhsocial.app/terms.html`, `privacy.html`. |
| **2.1(a)** | White screen / post-splash | Native first paint: `vite.config.ts` **native-first-paint**; `index.html` boot splash; `LaunchScreen.storyboard` **`#0c0a0f`**; splash gated on **`nativeStorageReady`** + `BRUH_NATIVE_STORAGE_READY_EVENT`. |

---

## Repo artifacts

| File | Purpose |
|------|---------|
| `docs/APP_STORE_EULA_FULL_TEXT.txt` | Paste into ASC **License Agreement** when full text required |
| `landing/terms.html` | Public terms — keep **`<!-- terms-revision: ... -->`** in sync with git |
| `landing/privacy.html` | Public privacy |

**Canonical URLs for ASC / in-app:** `share.bruhsocial.app` HTML pages (Netlify `landing/`).

---

## Human checklist (ASC)

- [ ] Privacy Policy field = live `privacy.html` URL (verify 200 after deploy).  
- [ ] Terms / EULA = custom text file, standard Apple EULA, or `terms.html` per rules.  
- [ ] Review notes: test account **`applereview`** / **`BruhReview2026!`** (rotate if policy changes).  
- [ ] Resubmission: screen recording opening Terms + Privacy from subscription flow.

---

## Related memory in repo

- `memory/apple_app_review_remediation.md`  
- `memory/ios_ipad_splash_launch.md`  
- `memory/launch_prep.md` (ASC app id, product ids)

---

## See also

- [[Launch Checklist]]
- [[Monetization]]
- [[Startup Sequence & Storage Keys]]
- [[iOS & Android]]
- [[🏠 Home]]
