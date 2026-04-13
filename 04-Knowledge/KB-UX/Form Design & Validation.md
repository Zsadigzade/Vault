---
tags: [kb, ux, forms, validation]
area: knowledge-base
updated: 2026-04-04
---

# Form design & validation

---

## Mobile keyboards

| Field type | Input |
|------------|-------|
| Email | `type="email"` |
| Phone | `type="tel"` |
| Username | `autoComplete="username"` |
| New password | `autoComplete="new-password"` |

---

## Validation timing

| Strategy | When |
|----------|------|
| **On blur** | First touch — reduce aggression |
| **On submit** | Always final gate |
| **Inline async** | Username availability — debounce |

---

## Errors

- **Per-field** message below input; preserve user input on failure
- **Summarize** at top for long forms (with anchor links)

---

## Security UX

- **Mask** passwords with show/hide toggle
- Don’t **block paste** on password fields (accessibility + password managers)

---

## Performance

- **Debounce** validation that hits server — [[Network & Caching Strategies]]

---

## See also

- [[Error State Design]] · [[Accessibility on Mobile (WCAG)]]
