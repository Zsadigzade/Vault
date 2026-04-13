---
tags: [kb, ux, a11y, wcag, mobile]
area: knowledge-base
updated: 2026-04-04
---

# Accessibility on mobile (WCAG)

---

## Touch targets

- Meet minimum size — [[Mobile Design Principles]]
- **Spacing** between adjacent actions

---

## Screen readers

| Practice | Detail |
|----------|--------|
| **Labels** | `aria-label` on icon-only buttons |
| **Live regions** | `aria-live` for toasts / new messages (polite vs assertive) |
| **Headings** | Logical order for VoiceOver/TalkBack |

---

## Focus management

- **Modal opens** → trap focus; on close return focus to trigger
- **Radix** handles much of this — [[Design Systems & Component Patterns]]

---

## Color & motion

- Don’t rely on color alone — [[Color & Contrast Accessibility]]
- **Reduce motion** — [[Animation & Micro-interactions]]

---

## Forms

- Associate errors with fields (`aria-describedby`) — [[Form Design & Validation]]

---

## Testing

- iOS **VoiceOver**, Android **TalkBack**, plus keyboard where applicable (PWA)

---

## See also

- [[Typography & Readability]] · [[Mobile UX Heuristics]]
