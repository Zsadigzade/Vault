---
tags: [kb, design, social, ux, feeds]
area: knowledge-base
updated: 2026-04-04
---

# Social app UI patterns

---

## Feed cards

| Element | Pattern |
|---------|---------|
| **Identity** | Avatar + display name + optional @handle |
| **Timestamp** | Relative (“2m”) with absolute `title` tooltip |
| **Media** | Fixed aspect or skeleton; tap to expand / detail |
| **Actions** | Like, comment, share — consistent order per row |

Performance: [[List Virtualization]] · [[Image & Media Optimization]].

---

## Stories / ephemeral UI

- **Progress** indicators at top; swipe to dismiss
- **Preload** next segment; handle **fail** with retry chip

---

## Reactions & composer

- **Quick reactions** row — don’t block primary content
- **Composer:** sticky above keyboard (project: [[Keyboard & Layout]] for Capacitor)

---

## Profiles

- **Header** collage or cover + avatar overlap
- **Tabs:** posts / media / replies — lazy load tab panels

---

## Share & deep links

- Consistent **OG** / preview behavior on web; native **share sheet** on iOS/Android

Project: [[Deep Links & PWA]] · [[Share Card System]].

---

## Empty & error states

See [[Error State Design]] · [[Loading & Skeleton States]].

---

## See also

- [[Feed & Infinite Scroll Patterns]] · [[Social App Engagement Patterns]] · [[Animation & Micro-interactions]]
- [[Developer design inspiration & motion tools]] — web / motion references (Godly, React Bits, Spline, …)
- [[Mobile Design Principles]] · [[Design Systems & Component Patterns]]
- Repos: [shadcn-ui/ui](https://github.com/shadcn-ui/ui) · [emilkowalski/vaul](https://github.com/emilkowalski/vaul) — [[Curated GitHub Repositories]]
