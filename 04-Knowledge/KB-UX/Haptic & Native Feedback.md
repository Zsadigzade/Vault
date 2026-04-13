---
tags: [kb, ux, haptics, capacitor]
area: knowledge-base
updated: 2026-04-04
---

# Haptic & native feedback

---

## Capacitor Haptics

| Impact style | Use |
|--------------|-----|
| **Light** | Toggle, small success |
| **Medium** | Button confirm |
| **Heavy** | Rare emphasis (avoid overuse) |

**Guard:** native-only (`Capacitor.isNativePlatform()` pattern in project).

---

## Pairing with UI

- **Visual** state change + optional haptic — never haptic alone for critical feedback
- **Respect** system “disable haptics” / low power mode behavior where exposed

---

## Sound

- Short **UI clicks** optional; default **off** or respect silent mode
- Avoid autoplay audio in WebView without gesture (platform policies)

---

## When **not** to use

- **High-frequency** events (scroll, drag)
- **Error** loops — can feel punitive

---

## See also

- [[Animation & Micro-interactions]] · [[Mobile Design Principles]]
