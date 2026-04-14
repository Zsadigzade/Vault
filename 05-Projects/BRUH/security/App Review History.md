---
tags: [security, apple, app-review, compliance, eula]
area: security
updated: 2026-04-14
---

# App Review History

---

## Resubmission 2026-04-14 — ✅ IN REVIEW

All rejection items resolved. Submitted 2026-04-14.

### Rejection 2 (2026-04-05) — resolved

| Guideline | Issue | Fix |
|-----------|-------|-----|
| **3.1.2(c)** | Privacy Policy URL missing in ASC; EULA missing | Privacy Policy URL set to `https://share.bruhsocial.app/privacy.html`; EULA pasted from `docs/APP_STORE_EULA_FULL_TEXT.txt` into ASC License Agreement field |
| **2.1(b)** | IAP not responsive; Paid Apps Agreement missing | Colleague signed agreement + added bank account 2026-04-14; IAP tested in sandbox — confirmed working |

### Rejection 1 (2026-03-25) — resolved

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

## Human checklist (ASC) — ✅ ALL DONE 2026-04-14

- [x] Privacy Policy field = `https://share.bruhsocial.app/privacy.html` ✅  
- [x] Terms / EULA = `docs/APP_STORE_EULA_FULL_TEXT.txt` pasted into ASC License Agreement field ✅  
- [x] Review notes: test account **`applereview`** / **`BruhReview2026!`** in App Review Information ✅  
- [x] Screen recording of Terms + Privacy from subscription flow sent in reply ✅  
- [x] IAP tested in sandbox — working after Paid Apps Agreement activated ✅  
- [x] Screenshots uploaded (iPhone 6.5") ✅

---

## Related memory in repo

- `memory/apple_app_review_remediation.md`  
- `memory/ios_ipad_splash_launch.md`  
- `memory/launch_prep.md` (ASC app id, product ids)

---

## Apple Guidelines — notable 2025 updates

- **May 1, 2025**: guidelines updated for compliance with US court decision — buttons, external links, and alternative payment methods now allowed in specific regions/categories
- **Nov 13, 2025**: further revisions for updated policies + clarification (no specific public detail)
- **Upcoming (Guideline 5.1.1)**: apps allowing account creation must allow data deletion — already implemented in BRUH
- **iOS 26**: new design rollout — review UI against new HIG when released
- Sources: [apple.com/news May 2025](https://developer.apple.com/news/?id=9txfddzf), [Nov 2025](https://developer.apple.com/news/?id=ey6d8onl), [upcoming requirements](https://developer.apple.com/news/upcoming-requirements/)

---

## See also

- [[Launch Checklist]]
- [[Monetization]]
- [[Startup Sequence & Storage Keys]]
- [[iOS & Android]]
- [[🏠 Home]]
