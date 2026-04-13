---
tags: [reference, tombstones, anti-patterns, graveyard]
area: reference
status: stable
updated: 2026-04-05
---

# Tombstones & anti-patterns (graveyard)

> [!important] **Before suggesting a “new” approach**, check this note. Entries are **removed or failed** paths; reintroducing them wastes time or breaks production.

---

## Infrastructure & webhooks

| What died | Why | Do not |
|-----------|-----|--------|
| Supabase **Database Webhooks** UI for push / secret-bearing triggers | Dashboard truncated `WEBHOOK_SECRET` JSON → `22P02`, rolled back INSERTs (2026-03-22) | Recreate push triggers in Dashboard UI |
| RevenueCat **V2** verify URL with current secret key format | Incompatible; webhook reverted to V1-style verification | Switch webhook verification to V2 without explicit key + docs audit |
| `netlify api createDnsRecord` CLI | Repeated 422 / broken for this workflow | Use Netlify REST API for DNS (see [[12 - MCP & External APIs]]) |

---

## Client & platform

| What died | Why | Do not |
|-----------|-----|--------|
| `Keyboard.resize: 'body'` | Reflowed shell; broke keyboard UX (2026-03-28) | Re-enable body resize for “quick fix” |
| `adjustPan` / `adjustResize` for this app | Conflicts with manual `--kbd-h` architecture | Change AndroidManifest soft input mode casually |
| `Capacitor.isPluginAvailable("NativeAd")` for “is native ad available” | Returned true on Android when not meaningful | Use platform checks aligned with current `admob.ts` patterns |
| `canvas.toBlob` for posting card critical path | Android WebView release latency (100–500ms scheduling) | Replace `toDataURL` encode path with `toBlob` without measuring |
| Consumer **admin** inside main app bundle | Removed; ops admin is `admin-web/` | Re-inline heavy admin into consumer app |
| **Hide this meme** + **Hidden GIFs & stickers** settings | Removed from client (2026-04-05); localStorage list + `hidden_memes` sync code deleted; **DB table may still exist** | Rebuild hide/unhide UX without a product decision; assume settings route `/settings/hidden-gifs` |

---

## Security & auth (rejected patterns)

| What died | Why | Do not |
|-----------|-----|--------|
| `is_admin(p_auth_id uuid)` | Allowed admin UUID enumeration (2026-03-28) | Reintroduce arbitrary UUID probe helpers |
| Open-ended `users` SELECT for clients | Data exposure risk | Bypass helper RPCs for admin lookups |

---

## Git & repo hygiene

| What died | Why | Do not |
|-----------|-----|--------|
| GCP service account key committed | Scrubbed; key must rotate | Re-commit service account JSON to repo |
| Root junk assets / scripts (cleaned 2026-03-29) | Noise and accidental leaks | Dump large binaries into repo root |

---

## Add a tombstone

When a feature or library is **removed on purpose**, add a row: **what**, **why killed**, **date**, **never again**. Link to [[Bug History & Lessons]] or [[Decision Log]] if narrative exists.

---

## See also

- [[Bug History & Lessons]] · [[Critical Gotchas]] · [[Decision Log]]
- [[CONSTITUTION]] · [[INVARIANTS]] · [[🏠 Home]]
