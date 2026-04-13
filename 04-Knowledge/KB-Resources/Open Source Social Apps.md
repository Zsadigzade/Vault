---
tags: [kb, resources, oss, social]
area: knowledge-base
updated: 2026-04-04
---

# Open source social apps & references

> [!note] Use these for **architecture and pattern** study — licenses, scale, and threat models differ from a consumer meme app. Do not copy security-sensitive code without review.

---

## Federated / large-scale social (backend-heavy)

| Project | What it is | What to study |
|---------|------------|----------------|
| [bluesky-social/atproto](https://github.com/bluesky-social/atproto) | Protocol + repos for Bluesky stack | Federation, records, moderation pipelines |
| [bluesky-social/social-app](https://github.com/bluesky-social/social-app) | Bluesky client (React Native) | Mobile social client patterns |
| [mastodon/mastodon](https://github.com/mastodon/mastodon) | Ruby on Rails fediverse server | ActivityPub, timelines, moderation admin |
| [LemmyNet/lemmy](https://github.com/LemmyNet/lemmy) | Rust federated link aggregator | Communities, voting, federation |

---

## Realtime & feeds (building blocks)

| Project | What it is | What to study |
|---------|------------|----------------|
| [supabase/realtime](https://github.com/supabase/realtime) | Elixir Realtime server | Channels, presence — aligns with BRUH stack |
| [getstream/stream-js](https://github.com/GetStream/stream-js) | Official JS SDK for Stream activity feeds | Feed API mental model (commercial backend) |

---

## Chat & community (patterns)

| Project | What it is | What to study |
|---------|------------|----------------|
| [mattermost/mattermost](https://github.com/mattermost/mattermost) | Team chat (Go + React) | Channels, permissions, scaling tradeoffs |
| [RocketChat/Rocket.Chat](https://github.com/RocketChat/Rocket.Chat) | Chat platform | Extensible server, mobile clients |

---

## Scheduling / “product surface” reference (not social graph)

| Project | What it is | What to study |
|---------|------------|----------------|
| [calcom/cal.com](https://github.com/calcom/cal.com) | Scheduling product (Next.js) | Booking UX, org billing hooks, OSS monorepo layout |

---

## Engineering blogs (architecture case studies)

| Source | Focus |
|--------|--------|
| **Instagram Engineering** | Feed ranking, media at scale — high-level posts |
| **Discord Engineering** | Realtime, Elixir/Erlang — infrastructure narratives |
| **Slack Engineering** | Reliability, feature delivery at scale |
| **Twitter / X Engineering** (archives) | Historical timeline/scale posts — verify current URL |

> [!tip] Prefer **recent** posts; older “Twitter scale” articles may describe retired stacks.

---

## Feature-specific search terms (GitHub)

Use these when hunting implementations:

| Topic | Search hints |
|-------|----------------|
| **Infinite scroll + virtualization** | `react-window`, `tanstack-virtual` examples |
| **Moderation queues** | `admin moderation dashboard` + your stack |
| **Push notification server** | `web-push` + `fcm` server samples |
| **Open Graph / share cards** | `@vercel/og`, `satori` examples |

---

## See also

- [[Curated GitHub Repositories]] · [[Social App UI Patterns]] · [[Social App Engagement Patterns]] · [[Realtime & Subscriptions]]
