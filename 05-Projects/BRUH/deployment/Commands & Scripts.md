---
tags: [deployment, commands, scripts, windows, cli, vault, obsidian, dataview]
area: deployment
updated: 2026-04-07
---

# Commands & Scripts

> [!tip] **Fast cheat sheet:** [[🏠 Home]] → *Most-Used Commands*. This note adds **Supabase, Vercel, Capgo, Codemagic**, Dataview queries, and Windows `.bat` detail.

## Core Dev Commands

```bash
npm run dev           # local dev server (Vite)
npm run build         # production build → dist/
npm run test          # full Vitest suite (~155 tests)
npm run version:bump  # bump root semver in package.json + package-lock (patch 0–99; 1.0.99 → 1.1.0)
npx vitest run src/test/<file>.test.ts   # targeted single file
npx cap sync          # sync web assets → native (after build)
npx cap open ios      # open Xcode
npx cap open android  # open Android Studio
```

> [!warning] Always use `npx supabase` and `npx vercel` — global CLI installs fail with EPERM on Windows. (`npx netlify` no longer needed — Netlify removed Apr 2026.)

---

## npm: dependency updates (moderate)

Default workflow — **stay on current majors**, refresh minors/patches:

```bash
# Repo root (postinstall runs patch-package)
npx npm-check-updates --target minor -u
npm install

# Optional: repeat in sub-packages
cd dashboard && npx npm-check-updates --target minor -u && npm install
cd ../.cursor && npx npm-check-updates --target minor -u && npm install
```

- Keep root **`package.json` `overrides`** unless **`npm audit`** / release notes justify changing security pins.
- If **`@capacitor-community/admob`** version changes, **`patches/*.patch`** may need regenerating; confirm **`npm install`** postinstall succeeds.
- After dependency changes that touch **`@capacitor/*`**, run **`npx cap sync`** before iOS/Android builds.
- Aggressive pinned **`@latest`** installs: see repo **`update-all-packages.bat.example`** (copy to local **`.bat`** only).

---

## Supabase Commands

```bash
npx supabase login
npx supabase link --project-ref gpainqlxdakaczkgozko

# Migrations
npx supabase migration new <name>
npx supabase db push --yes            # apply local migrations to remote
npx supabase db pull                  # pull remote state to local
npx supabase migration list           # see applied migrations
npx supabase migration repair --status reverted <id>   # fix drift

# Edge functions
npx supabase functions deploy <name>  # deploy single function
npx supabase functions deploy         # deploy all functions
npx supabase functions logs <name>    # view function logs

# Types
npx supabase gen types typescript --project-id gpainqlxdakaczkgozko > src/types/supabase.ts

# Local dev
npx supabase start    # start local Supabase stack
npx supabase stop
```

---

## Landing Deploy (Vercel — was Netlify, removed Apr 2026)

Landing auto-deploys on push to `main`. Manual trigger if needed:
```bash
cd landing && npx vercel --prod
```

DNS is on **Cloudflare** (zone `7d072cd53d25db06302fd5f2d3e51143`). Use Cloudflare dashboard or API — see [[Deploy Targets]] § DNS Configuration.

---

## Capgo OTA

```bash
# OTA push (use the .bat file on Windows — copy from capgo-push.bat.example if yours is old)
capgo-push.bat

# What capgo-push.bat does (template in repo):
# 1. node scripts/bump-package-version.mjs — bumps version + npm install --package-lock-only
#    (bump script silences npm stdout so cmd "for /f" capture stays clean)
# 2. npm run build
# 3. npx @capgo/cli bundle upload … --bundle <newVersion>

# Semver rule: patch is 0–99; 1.0.99 → 1.1.0 — never 1.0.100 / 1.0.101 (see scripts/bruhSemver.mjs, src/test/bruhSemver.test.ts)
# Do NOT use batch PATCH+1 — use bump-package-version.mjs only.

# ⚠️ Does NOT commit or push to git
```

---

## Git Tags (Triggers iOS CI)

```bash
git tag v1.0.68        # Codemagic auto-builds iOS on v* tags
git push origin v1.0.68
# → Codemagic picks up tag → builds → uploads to TestFlight
```

---

## Windows `.bat` Script System

> [!important]
> - All `*.bat` files are **gitignored** (except `android/gradlew.bat`)
> - Committed templates: `*.bat.example` in repo root + `scripts/*.bat.example`
> - Copy to use: `copy capgo-push.bat.example capgo-push.bat`
> - Never commit `.bat` files (they may embed keys or device paths)

### Key `.bat` Files

| File | Purpose |
|------|---------|
| `capgo-push.bat` | OTA update push — **`node scripts\bump-package-version.mjs`** (BRUH semver) + build + upload; re-copy from **`capgo-push.bat.example`** if the local file used naive `PATCH+1` |
| `installation.bat` | Full local setup / dependency install |
| `scripts/load-local-api-env.bat` | Loads `CAPGO_API_KEY` from `.cursor/.env.mcp.local` |
| `scripts/vault-backup.bat` | Robocopy mirror of Obsidian vault → dated backup (copy from `.example`) |
| `scripts/vault-search.bat` | Full-text search in vault via `rg` (optional) |
| `scripts/session-start.bat` | Open vault + `SESSION_HANDOFF` / `🏠 Home` in Obsidian |
| `scripts/health-check.bat` | Repo: migration list + `npm audit` + tests (slow; optional) |

### `CAPGO_API_KEY` Resolution
1. Windows User environment variable (if set — overrides everything)
2. `.cursor/.env.mcp.local` loaded by `scripts/load-local-api-env.bat`
3. `secrets.local.env` at repo root (optional alternative)

---

## Testing

```bash
# Full suite — run when user asks or for broad/risky changes
npm run test

# Targeted (during development iteration)
npx vitest run src/test/auth.test.ts
npx vitest run src/test/posts.test.ts
npx vitest run src/test/<file>.test.ts

# Watch mode
npx vitest src/test/<file>.test.ts
```

**Global mocks** (`src/test/setup.ts`): `@capacitor/core`, Supabase client, PostHog, nativeStorage

**All component tests**: Use `renderWithProviders` from `src/test/testUtils.tsx` (not bare `render`)

---

## Version Bumping

App version lives in `package.json`. Capgo OTA push bumps it automatically via `capgo-push.bat` (must call **`scripts/bump-package-version.mjs`** — see [[Capgo OTA]]). For native store releases, manually bump before tagging.

Format: `major.minor.patch` with **patch 0–99** only (BRUH rule); next after `1.0.99` is `1.1.0`, not `1.0.100`.

---

## Obsidian vault — PowerShell (CLI)

> [!tip] **Vault path:** `C:\Users\zsadi\Desktop\Vault\First Vault` — adjust `$vault` if yours differs. Run in **PowerShell**. Skip `.obsidian` by filtering paths.

Set once per session:

```powershell
$vault = "C:\Users\zsadi\Desktop\Vault\First Vault"
$md = Get-ChildItem -Path $vault -Filter *.md -Recurse -File |
  Where-Object { $_.FullName -notmatch '[\\/]\.obsidian[\\/]' }
```

### Stats & inventory

**Total note count**

```powershell
$md.Count
```

**Notes per top-level folder** (immediate parent of each `.md`)

```powershell
$md | Group-Object { $_.Directory.Name } | Sort-Object Count -Descending |
  Format-Table Name, Count -AutoSize
```

**Largest / smallest notes (bytes)**

```powershell
$md | Sort-Object Length -Descending | Select-Object -First 15 Name, @{N='KB';E={[math]::Round($_.Length/1KB,1)}}, FullName
$md | Sort-Object Length | Select-Object -First 15 Name, @{N='KB';E={[math]::Round($_.Length/1KB,1)}}, FullName
```

**Recently modified (last 7 days)**

```powershell
$cutoff = (Get-Date).AddDays(-7)
$md | Where-Object { $_.LastWriteTime -ge $cutoff } |
  Sort-Object LastWriteTime -Descending |
  Select-Object LastWriteTime, Name, DirectoryName
```

**Total words (rough)**

```powershell
($md | ForEach-Object { (Get-Content $_.FullName -Raw) -split '\s+' | Where-Object { $_ } }).Count
```

### Search & discovery

**Full-text search** (built-in; slow on huge vaults)

```powershell
$md | Select-String -Pattern "getUserId" -SimpleMatch |
  Select-Object Path, LineNumber, Line
```

**Faster search** — if [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) is on `PATH`:

```powershell
rg -n "getUserId" -g "*.md" -g "!**/.obsidian/**" $vault
```

**Tags in YAML frontmatter** (lines starting with `tags:`)

```powershell
$md | Select-String -Pattern '^tags:\s*\[([^\]]+)\]' |
  ForEach-Object { $_.Matches.Groups[1].Value -split ',' } |
  ForEach-Object { $_.Trim() } | Where-Object { $_ } |
  Group-Object | Sort-Object Count -Descending | Format-Table Name, Count
```

### Wiki-links — extract, broken check, orphans

> [!note] **Heuristic:** Matches `[[Target]]` and `[[Target|alias]]`. Resolves **by file base name** (e.g. `[[Authentication]]` → `Authentication.md`). Does not model every Obsidian path alias; use Graph / backlinks to validate edge cases.

**Build name → paths map + all link targets**

```powershell
$nameToPaths = @{}
foreach ($f in $md) {
  $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
  if (-not $nameToPaths.ContainsKey($base)) { $nameToPaths[$base] = [System.Collections.ArrayList]@() }
  [void]$nameToPaths[$base].Add($f.FullName)
}
$allTargets = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($f in $md) {
  $raw = Get-Content $f.FullName -Raw
  foreach ($m in [regex]::Matches($raw, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')) {
    $t = $m.Groups[1].Value.Trim()
    $leaf = ($t -split '/|\\')[-1]
    [void]$allTargets.Add($leaf)
  }
}
```

**Potentially broken links** (target base name has no `.md` in vault)

```powershell
$broken = foreach ($t in $allTargets) {
  if (-not $nameToPaths.ContainsKey($t)) { $t }
}
$broken | Sort-Object
```

**Approximate orphans** (no incoming `[[...]]` to that note’s base name from any other file)

```powershell
$orphans = foreach ($f in $md) {
  $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
  $refsFromOthers = 0
  foreach ($g in $md) {
    if ($g.FullName -eq $f.FullName) { continue }
    $raw = Get-Content $g.FullName -Raw
    if ($raw -match ('\[\[' + [regex]::Escape($base) + '(\||\])')) { $refsFromOthers++ }
  }
  if ($refsFromOthers -eq 0) {
    [PSCustomObject]@{ Orphan = $base; Path = $f.FullName }
  }
}
$orphans | Sort-Object Orphan | Format-Table -AutoSize
```

> [!tip] Orphans list includes **hubs** only linked from outside the vault or via non-`[[wiki]]` references — treat as a **hint**, not ground truth.

---

## Obsidian — shortcuts & command palette

> [!tip] Baseline shortcuts also live in [[How to Use This Vault]].

| Action | Shortcut / how |
|--------|----------------|
| Quick switcher | `Ctrl+O` |
| Vault search | `Ctrl+Shift+F` |
| Graph | `Ctrl+G` |
| **Command palette** | `Ctrl+P` |
| Toggle edit / preview | `Ctrl+E` |
| Toggle left sidebar | `Ctrl+\` |
| Toggle right sidebar | `Ctrl+Shift+\` |
| Open link in new pane | `Ctrl+Click` on `[[link]]` |
| New tab from link | `Ctrl+Shift+Click` (if supported by theme) |
| Follow link under cursor | `Ctrl+Enter` (default editor) |
| Create note from unresolved `[[link]]` | `Alt+Enter` or click while holding modifier per Obsidian version |
| Back / forward | `Alt+←` / `Alt+→` |
| Daily note | `Ctrl+Shift+D` (if **Daily notes** enabled) |
| Settings | `Ctrl+,` |
| Developer tools | `Ctrl+Shift+I` |

**Command palette (typed) — useful strings**

- `Backlinks: Open` — backlink pane for current note
- `Outline: Open` — heading outline
- `Global search: Open` — same as `Ctrl+Shift+F`
- `Templates: Insert` — core Templates plugin
- `Open graph view` — local graph for current note

---

## Obsidian — Dataview snippets

> [!important] Requires community plugin **Dataview**. Paste each snippet into a note inside a fenced code block whose language is `dataview` (three backticks, then `dataview`, then the query, then three backticks).

**Recently updated (7 days)**

```dataview
TABLE file.mtime AS Modified
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

**Notes with `status: active`**

```dataview
LIST
FROM ""
WHERE status = "active"
SORT file.name ASC
```

**Group notes by `area` (frontmatter)**

```dataview
TABLE rows.file.link AS Notes
FROM ""
WHERE area
GROUP BY area
SORT area ASC
```

**KB folders — note counts**

```dataview
TABLE length(rows) AS Notes
FROM ""
WHERE startswith(file.folder, "KB ")
GROUP BY file.folder
SORT file.folder ASC
```

**Zero backlinks (orphan hint)**

```dataview
TABLE length(file.inlinks) AS Inlinks
FROM ""
WHERE length(file.inlinks) = 0 AND !contains(file.path, "Templates")
SORT file.path ASC
```

**`SESSION_HANDOFF` last modified**

```dataview
TABLE file.mtime AS "Last modified"
FROM "01-Agents"
WHERE file.name = "SESSION_HANDOFF"
```

**Tag frequency**

```dataview
TABLE length(rows) AS Count
FROM ""
FLATTEN file.tags AS tag
WHERE tag
GROUP BY tag
SORT length(rows) DESC
```

---

## BRUH repo — diagnostics & housekeeping

> [!warning] Run from repo root: `C:\Users\zsadi\Desktop\BRUH`. Use **`npx supabase`** / **`npx vercel`** on Windows.

### Database & Supabase

```bash
npx supabase migration list
npx supabase db diff          # if linked; schema drift vs local migrations
```

**Edge functions (local folder names)**

```powershell
# PowerShell (repo root)
Get-ChildItem .\supabase\functions -Directory | ForEach-Object Name
```

```bat
REM cmd.exe (repo root)
dir /b supabase\functions
```

> [!tip] **Live inventory / advisors:** Supabase Dashboard → **Edge Functions**; **Advisors** (security + performance). MCP `list_edge_functions` when available in Cursor.

### Dependencies & audit

```bash
npm audit --audit-level=high
npm outdated
```

### Build / bundle size (after build)

```bash
npm run build
```

Then in **PowerShell** (folder size of `dist/`):

```powershell
Get-ChildItem .\dist -Recurse -File | Measure-Object -Property Length -Sum |
  Select-Object @{N='dist_MB';E={[math]::Round($_.Sum/1MB,2)}}, Count
```

### Code markers & size (PowerShell from repo root)

```powershell
rg -n "TODO|FIXME|HACK" --glob "*.{ts,tsx,js,jsx}" .
```

```powershell
Get-ChildItem .\src -Recurse -Include *.ts,*.tsx |
  Get-Content | Measure-Object -Line
```

### Tests

```bash
npm run test
npx vitest run src/test/<file>.test.ts
```

### Git

```bash
git status -sb
git log -10 --oneline
git tag -l "v*"
```

```powershell
# Sorted version tags (PowerShell)
git tag -l 'v*' | ForEach-Object { $_.Trim() } | Sort-Object { [version]($_.TrimStart('v')) }
```

---

## Automation templates (repo)

See **Windows `.bat` Script System** above. Copy from `scripts/*.bat.example`:

| Template | After copy |
|----------|------------|
| `scripts/vault-backup.bat.example` | `vault-backup.bat` — set `VAULT_DIR` and `BACKUP_PARENT` inside |
| `scripts/vault-search.bat.example` | `vault-search.bat` — optional `RG_PATH`; pass search term as arg |
| `scripts/session-start.bat.example` | `session-start.bat` — set `OBSIDIAN_EXE` and vault URI or path |
| `scripts/health-check.bat.example` | `health-check.bat` — runs from repo root; optional `SKIP_TEST=1` |
