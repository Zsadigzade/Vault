---
tags: [deployment, windows, setup, local-dev, bat-files, environment]
area: deployment
updated: 2026-04-03
---

# Windows Setup & Local Development

> [!important] This project is Windows-native and requires `.bat` scripts. **Never commit `.bat` files** — use `.bat.example` templates.

---

## Initial Setup (New Machine)

### 1. Clone & Dependencies

```bash
git clone https://github.com/Zsadigzade/BRUH.git
cd BRUH
npm install
cd .cursor && npm install && cd ..
```

### 2. Copy `.bat` Script Templates

All `.bat` files are **gitignored**. Copy templates to use them:

```bash
# Repo root
copy capgo-push.bat.example capgo-push.bat
copy installation.bat.example installation.bat

# Scripts directory
copy scripts\load-local-api-env.bat.example scripts\load-local-api-env.bat
```

### 3. Set Up Environment Files

#### `.cursor/.env.mcp.local` (Cursor MCP + Capgo API key)

```env
CAPGO_API_KEY=your_capgo_api_key_here
GITHUB_OWNER=Zsadigzade
GITHUB_TOKEN=your_github_token_here
POSTHOG_PERSONAL_API_KEY=your_posthog_key_here
SUPABASE_ACCESS_TOKEN=your_supabase_token_here
```

This file:
- Is **gitignored** (same as `.cursor/mcp.json`)
- Loaded by `scripts/load-local-api-env.bat`
- Used by Capgo scripts and MCP services
- **Never commit this file**

#### `secrets.local.env` (Optional alternate for Capgo API key)

If you prefer not to use `.cursor/.env.mcp.local`:

```env
CAPGO_API_KEY=your_capgo_api_key_here
```

**Resolution order:**
1. Windows User env var (if set) — overrides everything
2. `.cursor/.env.mcp.local`
3. `secrets.local.env`

### 4. Supabase & Netlify Auth

```bash
# Login to Supabase (stores token in ~/.supabase)
npx supabase login

# Link project (one-time)
npx supabase link --project-ref gpainqlxdakaczkgozko

# Verify connection
npx supabase projects list
```

```bash
# Login to Netlify (stores token in %APPDATA%\Netlify\Config\config.json)
npx netlify login

# Verify connection
npx netlify status
```

---

## Running Locally

### Dev Server

```bash
npm run dev
# → Vite dev server on localhost:5173
# → React app hot-reloads
# → Supabase API available via VITE_SUPABASE_URL
```

### Capacitor Native (iOS/Android)

```bash
# Build web app
npm run build

# Sync to native projects
npx cap sync

# Open Xcode (iOS)
npx cap open ios

# Open Android Studio (Android)
npx cap open android
```

### Tests

```bash
# Full test suite (~155 tests)
npm run test

# Single file (while iterating)
npx vitest run src/test/auth.test.ts

# Watch mode
npx vitest src/test/auth.test.ts
```

---

## `.bat` Script Usage

### `capgo-push.bat`

Pushes an OTA (Over-The-Air) update via Capgo:

```bash
capgo-push.bat
```

**What it does:**
1. Loads `CAPGO_API_KEY` from `.cursor/.env.mcp.local` (via `scripts/load-local-api-env.bat`)
2. Bumps `package.json` patch version
3. `npm run build` (production Vite build)
4. `npx cap sync` (sync to native)
5. Uploads bundle to Capgo

**⚠️ Important:**
- Does **NOT** commit or push git
- Commit the version bump manually when ready
- Do not use if app binary is on native stores — coordinate release timing

**Troubleshooting:**
- `CAPGO_API_KEY not found` → Check `.cursor/.env.mcp.local` or Windows env vars
- `--ignore-metadata-check` flag: append if node_modules versions differ locally (safe if change is JS-only)

### `installation.bat`

Full local setup (rarely needed):

```bash
installation.bat
```

Sets up Node, npm dependencies, and Supabase link. **Use once on a new machine.**

### `scripts/load-local-api-env.bat`

Helper script that loads `CAPGO_API_KEY` from `.cursor/.env.mcp.local`. Called by other `.bat` files automatically.

---

## Debugging Locally

### Console Logs

```bash
npm run dev
# → Browser DevTools (F12) → Console tab
```

### Capacitor Logs (Native)

**iOS (Xcode):**
```
Xcode → View → Debug Area → Console tab
```

**Android (Android Studio):**
```
Android Studio → View → Tool Windows → Logcat
# Filter: "CordovaWebView" for web logs
```

### Supabase Logs

```bash
# Edge function logs
npx supabase functions logs <function-name>

# Realtime events
npx supabase projects list
# → Open project URL → go to Data Explorer
```

---

## Environment Variables

### `.env.local` (Vite)

Located at repo root for dev server:

```env
VITE_SUPABASE_URL=https://gpainqlxdakaczkgozko.supabase.co
VITE_SUPABASE_ANON_KEY=<publish_anon_key>
VITE_POSTHOG_KEY=<posthog_key>
VITE_POSTHOG_HOST=https://eu.posthog.com
VITE_SENTRY_DSN=<sentry_dsn>
```

**⚠️ Never commit real keys** — `.env.local` is gitignored. Use `.env.example` for reference.

### Windows User Environment Variables

Accessible system-wide. Set via `setx` (permanent) or in PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("CAPGO_API_KEY", "value", "User")
```

---

## Git Workflow on Windows

### Never `cmd.exe` for git

Always use Git Bash (comes with Git for Windows):

```bash
# Configure Git Bash as default terminal
# Windows Terminal → Settings → Default Profile → "Git Bash"
```

### Committing

**⚠️ Never auto-commit.** Always explicit:

```bash
git status
git add src/components/Foo.tsx
git commit -m "fix: improve button styling"
# ← Wait for user to git push
```

### Version Tags (Triggers iOS CI)

```bash
# Create tag (auto-builds iOS in Codemagic)
git tag v1.0.68
git push origin v1.0.68
```

---

## Troubleshooting

### `npm ERR! EPERM: operation not permitted`

Global CLI tools fail on Windows. **Always use `npx`:**

```bash
npx supabase login
npx netlify login
```

### Port 5173 Already in Use

```powershell
# Find process using port
netstat -ano | findstr :5173

# Kill by PID
taskkill /PID <pid> /F
```

### Capacitor Sync Fails

```bash
# Clean rebuild
rm -r node_modules android/app/build ios/Pods
npm install
npm run build
npx cap sync
```

### `.bat` File Won't Run

```bash
# Execution policy issue
powershell -ExecutionPolicy Bypass -File capgo-push.bat

# Or set permanently (PowerShell as Admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## See also

- [[Commands & Scripts]]
- [[Deploy Targets]]
- [[Capgo OTA]]
- [[Critical Gotchas]]
- [[🏠 Home]]
