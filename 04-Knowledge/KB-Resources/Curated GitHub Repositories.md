---
tags: [kb, resources, github]
area: knowledge-base
updated: 2026-04-04
---

# Curated GitHub repositories

> [!note] Verify stars/maintenance before heavy adoption. Prefer **official** org repos.
> [!tip] **For agents:** Use `Repo | What it does | When to use` to pick fast; open upstream docs for API details.

---

## Awesome lists (start here)

| Repo | What it does | When to use |
|------|--------------|-------------|
| [enaqx/awesome-react](https://github.com/enaqx/awesome-react) | Curated React ecosystem links | Discover libs, patterns, examples |
| [lyqht/awesome-supabase](https://github.com/lyqht/awesome-supabase) | Starters, tools, Supabase integrations | Supabase-specific discovery |
| [capawesome-team/awesome-capacitorjs](https://github.com/capawesome-team/awesome-capacitorjs) | Capacitor guides, plugins, tooling | Hybrid/native bridge research |
| [riderx/awesome-capacitor](https://github.com/riderx/awesome-capacitor) | Broader Capacitor + community plugins | Plugin hunting (Capgo-maintained) |
| [aniftyco/awesome-tailwindcss](https://github.com/aniftyco/awesome-tailwindcss) | Tailwind plugins, UI kits, tools | Tailwind ecosystem sweep |

---

## React / UI core

| Repo | What it does | When to use |
|------|--------------|-------------|
| [facebook/react](https://github.com/facebook/react) | React runtime + reconciler | Source of truth |
| [radix-ui/primitives](https://github.com/radix-ui/primitives) | Headless accessible primitives | Building design system on Radix |
| [radix-ui/themes](https://github.com/radix-ui/themes) | Pre-styled Radix-based components | Faster theming than from-scratch primitives |
| [tanstack/query](https://github.com/TanStack/query) | Async/server state for React | Caching, infinite queries, mutations |
| [floating-ui/floating-ui](https://github.com/floating-ui/floating-ui) | Popover/tooltip positioning | Custom overlays; Radix uses this internally |

---

## Animation & motion

| Repo | What it does | When to use |
|------|--------------|-------------|
| [motiondivision/motion](https://github.com/motiondivision/motion) | Motion for React (formerly Framer Motion) | Layout animations, gestures |
| [pmndrs/react-spring](https://github.com/pmndrs/react-spring) | Physics-based spring animations | Alternative motion model |
| [formkit/auto-animate](https://github.com/formkit/auto-animate) | Zero-config list enter/exit | Quick list reorder polish |
| [pmndrs/use-gesture](https://github.com/pmndrs/use-gesture) | Drag/swipe/pinch/scroll gesture hooks | Native-feel mobile swipe interactions |

---

## Design system components

| Repo | What it does | When to use |
|------|--------------|-------------|
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | Copy-paste Radix + Tailwind components | BRUH stack-native; pull exact components without adding a dependency |
| [emilkowalski/vaul](https://github.com/emilkowalski/vaul) | Unstyled drawer/sheet for React | Native-feeling bottom sheets on web/PWA |
| [emilkowalski/sonner](https://github.com/emilkowalski/sonner) | Opinionated toast notifications | Compare with / replace current toast implementation |
| [tailwindlabs/headlessui](https://github.com/tailwindlabs/headlessui) | Headless accessible UI components | Complements Radix; Listbox, Combobox, Disclosure primitives |
| [rsms/inter](https://github.com/rsms/inter) | Inter variable typeface source | BRUH uses Inter; source for WOFF2 subsets + variable font |

---

## Icons & visuals

| Repo | What it does | When to use |
|------|--------------|-------------|
| [lucide-icons/lucide](https://github.com/lucide-icons/lucide) | Feather-style icon set (tree-shakeable) | Consistent iconography (current BRUH default) |
| [phosphor-icons/react](https://github.com/phosphor-icons/react) | 1000+ flexible icons in 6 weights | More variety and weight options than lucide; tree-shakeable |
| [tabler/tabler-icons](https://github.com/tabler/tabler-icons) | 5000+ MIT SVG icons; React package | Large icon variety; good for admin / settings screens |

---

## Forms & validation

| Repo | What it does | When to use |
|------|--------------|-------------|
| [colinhacks/zod](https://github.com/colinhacks/zod) | TypeScript-first schema validation | API/edge fn input, forms |
| [react-hook-form/react-hook-form](https://github.com/react-hook-form/react-hook-form) | Performant form state | Complex forms + zod resolver |
| [faker-js/faker](https://github.com/faker-js/faker) | Fake data generation | Seeds, Storybook, tests |

---

## Utilities (TS/JS)

| Repo | What it does | When to use |
|------|--------------|-------------|
| [date-fns/date-fns](https://github.com/date-fns/date-fns) | Immutable date helpers | Prefer over moment for bundle size |
| [lukeed/clsx](https://github.com/lukeed/clsx) | Conditional `className` join | Tiny class merging |
| [ai/nanoid](https://github.com/ai/nanoid) | Compact unique IDs | Client-side IDs, URLs |
| [gcanti/ts-pattern](https://github.com/gcanti/ts-pattern) | Exhaustive pattern matching | Replace nested switch on unions |
| [remeda/remeda](https://github.com/remeda/remeda) | Functional data utilities (typed) | lodash-style without loose typing |

---

## Media & images

| Repo | What it does | When to use |
|------|--------------|-------------|
| [lovell/sharp](https://github.com/lovell/sharp) | Fast image resize/encode (Node) | Server-side thumbnails, not browser |
| [woltapp/blurhash](https://github.com/woltapp/blurhash) | Compact placeholder hashes | Progressive image UX |
| [ValentinH/react-easy-crop](https://github.com/ValentinH/react-easy-crop) | Crop/zoom UI | Avatar or meme crop flows |

---

## Mobile / hybrid

| Repo | What it does | When to use |
|------|--------------|-------------|
| [ionic-team/capacitor](https://github.com/ionic-team/capacitor) | Native WebView bridge | Core hybrid runtime |
| [Cap-go/capacitor-updater](https://github.com/Cap-go/capacitor-updater) | OTA web bundle updates | Capgo / OTA pipelines |

---

## Supabase & realtime

| Repo | What it does | When to use |
|------|--------------|-------------|
| [supabase/supabase](https://github.com/supabase/supabase) | Monorepo: client, studio, examples | Docs + self-host reference |
| [supabase-community](https://github.com/supabase-community) | Unofficial helpers | Vet each package before adopt |
| [supabase/realtime](https://github.com/supabase/realtime) | Elixir realtime server | Understand channels at source |

---

## Notifications & engagement (evaluate vs BRUH stack)

| Repo | What it does | When to use |
|------|--------------|-------------|
| [novuhq/novu](https://github.com/novuhq/novu) | Open-source notification infrastructure | Multi-channel inbox, workflows |
| [knocklabs/javascript](https://github.com/knocklabs/javascript) | Knock JS/React SDKs (monorepo) | Commercial Knock product integration |

---

## Testing & quality

| Repo | What it does | When to use |
|------|--------------|-------------|
| [vitest-dev/vitest](https://github.com/vitest-dev/vitest) | Vite-native test runner | Unit + component tests |
| [testing-library/react-testing-library](https://github.com/testing-library/react-testing-library) | User-centric React tests | Prefer over shallow enzyme-style |
| [mswjs/msw](https://github.com/mswjs/msw) | API mocking in browser/Node | Integration tests without live API |
| [microsoft/playwright](https://github.com/microsoft/playwright) | E2E browser automation | Critical flows, CI |
| [storybookjs/storybook](https://github.com/storybookjs/storybook) | UI component workshop | Design review, visual regression setup |

---

## Bundler & DX

| Repo | What it does | When to use |
|------|--------------|-------------|
| [vitejs/vite](https://github.com/vitejs/vite) | Dev server + build | BRUH stack default |
| [biomejs/biome](https://github.com/biomejs/biome) | Formatter + linter (Rust) | Faster alternative to ESLint+Prettier (evaluate) |
| [changesets/changesets](https://github.com/changesets/changesets) | Versioning + changelog from PRs | Monorepo or library releases |
| [lint-staged/lint-staged](https://github.com/lint-staged/lint-staged) | Run linters on staged files only | Pre-commit hooks |

---

## Token optimization & AI efficiency

| Repo | What it does | When to use |
|------|--------------|-------------|
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | ~75% output token reduction; caveman prose mode for any AI agent | Active every session in BRUH — see [[caveman]] |
| [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | Curated Cursor / AI rules snippets | Find patterns to reduce context waste + improve rule quality |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MCP reference implementations (filesystem, fetch, etc.) | Patterns for custom tool servers; reduce round-trips |
| [anthropics/courses](https://github.com/anthropics/courses) | Official Anthropic prompt engineering courses | Learn Claude API, tool use, and efficient prompting patterns |

---

## See also

- [[Free Services & SaaS Directory]] · [[Performance & Debugging Tools]] · [[Open Source Social Apps]] · [[AI & Agent Ecosystem]]
