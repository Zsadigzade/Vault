---
tags: [kb, supabase, storage]
area: knowledge-base
updated: 2026-04-04
---

# Supabase Storage patterns

---

## Buckets

- **Public** vs **private** — default deny for user content if sensitive

---

## Policies

- **Path conventions** — `userId/uuid-filename` — easier RLS-style storage rules
- Test **unauthorized** upload/download

---

## Signed URLs

- **Short TTL** for private reads
- **Regenerate** on permission change if cached clientside

---

## Transforms

- Image **resize** at edge — [[Image & Media Optimization]]

---

## Upload flow

| Client direct | Via Edge |
|---------------|----------|
| Faster UX | Centralized virus scan / moderation |

---

## Cleanup

- **Lifecycle** deletes for abandoned uploads (cron job)

---

## See also

- [[Supabase Security Hardening]] · [[API Security & Rate Limiting]]
