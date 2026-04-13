---
tags: [kb, security, capacitor, storage]
area: knowledge-base
updated: 2026-04-04
---

# Secure storage on mobile

---

## Threat model (Capacitor)

- **WebView storage** is app-sandboxed but **not** encryption-at-rest by default for all platforms
- Rooted/jailbroken devices increase exposure — **assume client can be inspected**

> [!warning] **Never** store `service_role`, payment secrets, or admin tokens in Preferences/localStorage.

---

## Capacitor Preferences

| Use | Avoid |
|-----|-------|
| Non-sensitive prefs, feature flags, anon-compatible keys | Long-lived refresh tokens **if** policy requires hardware-backed storage |

Project: `nativeStorage` bridge — [[Startup Sequence & Storage Keys]].

---

## When to use native secure storage

- **Refresh tokens**, biometric-gated secrets — consider **Capacitor Secure Storage** / community plugins with **Keychain/Keystore**
- Evaluate **maintenance** and **platform quirks** (Android Keystore versions)

---

## WebView caveats

- **`localStorage` cleared** on uninstall varies — don’t rely for critical recovery without server
- **Backup:** Android Auto Backup can restore files — flag sensitive files `android:fullBackupContent` exclusions if needed

---

## Encryption

- **App-level encryption** of large local DBs (SQLite) if storing sensitive content offline — use established libs, not DIY AES wrappers

---

## See also

- [[Auth Security Patterns]] · [[Secrets Management Guide]] · [[OWASP Mobile Top 10]] (M9)
