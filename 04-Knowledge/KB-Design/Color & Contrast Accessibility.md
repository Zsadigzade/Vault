---
tags: [kb, design, a11y, wcag, color]
area: knowledge-base
updated: 2026-04-04
---

# Color & contrast accessibility

---

## WCAG contrast (quick ref)

| Level | Normal text | Large text (18pt+ or 14pt+ bold) |
|-------|-------------|-----------------------------------|
| **AA** | ≥ 4.5:1 | ≥ 3:1 |
| **AAA** | ≥ 7:1 | ≥ 4.5:1 |

**UI components & graphics:** often aim **3:1** against adjacent colors for boundaries (AA).

Tools: browser DevTools contrast picker, **WebAIM Contrast Checker**.

---

## Dark mode

| Issue | Mitigation |
|-------|------------|
| **Pure #000 + pure #fff** | Harsh; use neutral dark bg + off-white text |
| **Brand colors** | Re-check every brand hue in dark palette |
| **Elevation** | Use lighter surfaces (higher “paper”) instead of only shadows |

See [[Dark Mode Implementation]].

---

## Don’t rely on color alone

- Pair **color** with **icon**, **label**, or **pattern** for states (error, success, online)
- Links: underline or distinct weight — not hue alone

---

## Gradients & “Instagram-style” UI

- Text on gradients: use **scrims** (`bg-black/40`), **text shadow**, or **solid chip** behind text
- Test gradient buttons at **low brightness** outdoor

Project: [[User Preferences & Style]] for brand gradients.

---

## See also

- [[Accessibility on Mobile (WCAG)]] · [[Typography & Readability]]
