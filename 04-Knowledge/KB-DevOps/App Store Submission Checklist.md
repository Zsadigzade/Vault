---
tags: [kb, devops, app-review, stores]
area: knowledge-base
updated: 2026-04-04
---

# App Store submission checklist

---

## Apple (high level)

| Area | Check |
|------|-------|
| **Guideline 2.1** | Performance — no crashes on review device |
| **4.0 Design** | Human Interface Guidelines basics |
| **5.1 Privacy** | Privacy Nutrition Labels match behavior |
| **Payments** | Digital goods use IAP if required — see [[Monetization]] |

Project deep dive: [[App Review History]].

---

## Google Play

| Area | Check |
|------|-------|
| **Data safety** | Accurate collection/encryption declarations |
| **Permissions** | Minimal; justify each |
| **Content rating** | Questionnaire accuracy |

---

## Common rejections

- **Broken** IAP / login on review account
- **Placeholder** content
- **Missing** demo credentials in review notes
- **WebView** apps that are just a thin browser without native value

---

## Checklist (submission day)

- [ ] Version/build numbers bumped
- [ ] **Release notes** human-written
- [ ] **Review notes** with test user + backend flags
- [ ] **Attachments** for complicated login flows

---

## See also

- [[App Store Optimization (ASO)]] · [[OWASP Mobile Top 10]] (M6 — privacy)
