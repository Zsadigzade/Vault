---
tags: [security, payments, revenuecat, webhook]
area: security
updated: 2026-04-03
---

# Payment Webhook Security

> [!note] Edge function: `supabase/functions/revenuecat-webhook`. Consumer purchases: [[Monetization]].

---

## Authentication

| Mechanism | Detail |
|-----------|--------|
| **Authorization header** | Compared timing-safely to **`REVENUECAT_WEBHOOK_SECRET`** (same value as RC dashboard webhook token). Accepts **raw token** or **`Bearer <token>`**. |
| **HMAC** | **Optional** — if **`REVENUECAT_WEBHOOK_VERIFICATION_SECRET`** set, validate `X-RevenueCat-Signature`. Many setups use Authorization only. |
| **Hybrid REST verify** | Uses **`REVENUECAT_SECRET_KEY`**; **fail-closed** if missing on paths that require verify. |
| **Non-UUID `app_user_id`** | Return **200** + skip body — avoids infinite RC retries for anonymous / wrong-app IDs. |

---

## Processing

- **Zod** body validation.  
- **Idempotency:** `webhook_events` unique `event_id`, retention window.  
- **Rate limits:** IP / user buckets via DB RPCs (`check_and_increment_rate_limit` pattern).  
- **EXPIRATION → grace:** `newStatus` must be **`expired`** (not `null`) so **48h grace** logic runs.  
- **Timing-safe compare:** `_shared/timingSafeEqual` — not raw `===` for secrets.

---

## RLS / self-serve premium

- Users cannot `UPDATE` their own `subscription_status` from client — server/webhook only.  
- **Fraud / audit:** `subscription_fraud_signals`, `subscription_changes` — see admin **Fraud** / **Audit** tabs ([[Dashboards]]).

---

## Required / optional secrets

| Secret | Required? |
|--------|-----------|
| `REVENUECAT_WEBHOOK_SECRET` | Yes — matches RC Authorization |
| `REVENUECAT_SECRET_KEY` | Yes — hybrid verify |
| `REVENUECAT_WEBHOOK_VERIFICATION_SECRET` | No — HMAC layer only |

---

## See also

- [[Security Reference]]
- [[Monetization]]
- [[Edge Functions]]
- [[Database Reference]]
- [[Bug History & Lessons]] (RC V2 revert, timing attacks)
- [[🏠 Home]]
