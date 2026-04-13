#!/usr/bin/env python3
"""
knowledge_update.py — Autonomous web learning agent for the vault

Reads watch topics from 04-Knowledge/KB-AI/WATCH_TOPICS.md,
searches the web using Brave Search, Perplexity, and/or SearxNG,
summarizes findings, and proposes updates to 06-Inbox/pending/.

Usage:
  python scripts/knowledge_update.py                    # Full run (all topics)
  python scripts/knowledge_update.py --topic bruh_stack # One category
  python scripts/knowledge_update.py --dry-run          # Print without writing
  python scripts/knowledge_update.py --max-per-run 5    # Limit topics processed

Environment variables (set in .env or shell):
  BRAVE_SEARCH_API_KEY    — Brave Search API key
  PERPLEXITY_API_KEY      — Perplexity API key
  SEARXNG_URL             — SearxNG instance URL (default: http://localhost:8888)
  VAULT_ROOT              — override vault root (default: parent of scripts/)
"""

import gzip
import os
import sys
import json
import re
import datetime
import hashlib
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ─── Config ──────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", Path(__file__).parent.parent))
WATCH_TOPICS_FILE = VAULT_ROOT / "04-Knowledge" / "KB-AI" / "WATCH_TOPICS.md"
INBOX_PENDING = VAULT_ROOT / "06-Inbox" / "pending"
OUTCOMES_LEDGER = VAULT_ROOT / "07-Learning" / "OUTCOMES_LEDGER.md"
LEARNING_LOG = VAULT_ROOT / "07-Learning" / "LEARNING_LOG.md"

BRAVE_API_KEY = os.environ.get("BRAVE_SEARCH_API_KEY", "")
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:8888")

# Minimum confidence to propose to inbox
MIN_CONFIDENCE = 0.35

# Deduplicate: skip topics searched within this many days
SEARCH_COOLDOWN_DAYS = 3

# ─── Frontmatter helpers ─────────────────────────────────────────────────────

def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}, ""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    return fm, parts[2].strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def topic_hash(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()[:8]


# ─── Watch topics loading ─────────────────────────────────────────────────────

def load_watch_topics() -> dict[str, list[dict]]:
    """Load topics from WATCH_TOPICS.md frontmatter."""
    fm, _ = parse_frontmatter(WATCH_TOPICS_FILE)
    return fm.get("watch_topics", {})


def was_recently_searched(query: str) -> bool:
    """Check if a query was recently processed (cooldown period)."""
    h = topic_hash(query)
    state_file = VAULT_ROOT / "07-Learning" / ".search_state.json"
    if not state_file.exists():
        return False
    try:
        state = json.loads(state_file.read_text())
        last_run = state.get(h)
        if last_run:
            last_dt = datetime.date.fromisoformat(last_run)
            return (datetime.date.today() - last_dt).days < SEARCH_COOLDOWN_DAYS
    except Exception:
        pass
    return False


def mark_searched(query: str):
    """Record that a query was just searched."""
    h = topic_hash(query)
    state_file = VAULT_ROOT / "07-Learning" / ".search_state.json"
    try:
        state = json.loads(state_file.read_text()) if state_file.exists() else {}
    except Exception:
        state = {}
    state[h] = datetime.date.today().isoformat()
    state_file.write_text(json.dumps(state, indent=2))


# ─── Search backends ─────────────────────────────────────────────────────────

def search_brave(query: str, count: int = 5) -> list[dict]:
    """Search using Brave Search API. Returns list of {title, url, description}."""
    if not BRAVE_API_KEY:
        return []
    try:
        url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count={count}&text_decorations=false"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY,
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            data = json.loads(raw)
            results = data.get("web", {}).get("results", [])
            return [{"title": r.get("title", ""), "url": r.get("url", ""), "description": r.get("description", "")} for r in results]
    except Exception as e:
        print(f"  [Brave] Error: {e}")
        return []


def search_perplexity(query: str) -> dict:
    """Research using Perplexity API. Returns {summary, citations}."""
    if not PERPLEXITY_API_KEY:
        return {}
    try:
        payload = json.dumps({
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a research assistant. Provide a concise, factual summary with key points. Focus on recent developments (last 6 months if applicable). Include specific details, not generalities."},
                {"role": "user", "content": f"What are the latest developments, best practices, and key insights about: {query}? Summarize in 3-5 bullet points."},
            ],
            "max_tokens": 600,
            "return_citations": True,
        }).encode()
        req = urllib.request.Request(
            "https://api.perplexity.ai/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            citations = data.get("citations", [])
            return {"summary": content, "citations": citations}
    except Exception as e:
        print(f"  [Perplexity] Error: {e}")
        return {}


def search_searxng(query: str, count: int = 5) -> list[dict]:
    """Search using self-hosted SearxNG instance."""
    try:
        url = f"{SEARXNG_URL}/search?q={urllib.parse.quote(query)}&format=json&language=en&safesearch=0&engines=google,bing,duckduckgo"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            results = data.get("results", [])[:count]
            return [{"title": r.get("title", ""), "url": r.get("url", ""), "description": r.get("content", "")} for r in results]
    except Exception as e:
        print(f"  [SearxNG] Error: {e}")
        return []


def multi_search(query: str) -> dict:
    """Run all available search backends and merge results."""
    print(f"  Searching: {query}")
    results = {
        "query": query,
        "perplexity": {},
        "brave": [],
        "searxng": [],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Perplexity — best quality, use first
    if PERPLEXITY_API_KEY:
        results["perplexity"] = search_perplexity(query)
        time.sleep(0.5)  # rate limit

    # Brave
    if BRAVE_API_KEY:
        results["brave"] = search_brave(query, count=5)
        time.sleep(0.3)

    # SearxNG — always try (self-hosted fallback)
    results["searxng"] = search_searxng(query, count=5)

    return results


# ─── Result scoring and synthesis ────────────────────────────────────────────

def score_results(search_results: dict) -> float:
    """Score result quality 0.0–1.0."""
    score = 0.0
    if search_results.get("perplexity", {}).get("summary"):
        score += 0.5
    if len(search_results.get("brave", [])) >= 3:
        score += 0.25
    if len(search_results.get("searxng", [])) >= 3:
        score += 0.15
    citations = search_results.get("perplexity", {}).get("citations", [])
    if citations:
        score += 0.1
    return min(score, 1.0)


def synthesize_results(query: str, topic_meta: dict, search_results: dict) -> str:
    """Build markdown content for the inbox note."""
    lines = [f"# Knowledge update: {query}", ""]

    # Perplexity summary (best quality)
    plex = search_results.get("perplexity", {})
    if plex.get("summary"):
        lines += ["## Summary (Perplexity)", ""]
        lines.append(plex["summary"])
        lines.append("")

    # Top web results
    brave = search_results.get("brave", [])
    searxng = search_results.get("searxng", [])
    all_results = brave[:3] + searxng[:2]
    seen_urls = set()
    if all_results:
        lines += ["## Top sources", ""]
        for r in all_results:
            url = r.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            title = r.get("title", url)
            desc = r.get("description", "")
            lines.append(f"- [{title}]({url})")
            if desc:
                lines.append(f"  > {desc[:150]}")
        lines.append("")

    # Citations from Perplexity
    citations = plex.get("citations", [])
    if citations:
        lines += ["## Citations", ""]
        for c in citations[:5]:
            lines.append(f"- {c}")
        lines.append("")

    # Proposed additions
    proposed_path = topic_meta.get("proposed_path", "")
    if proposed_path:
        lines += [f"## Proposed addition to", f"`{proposed_path}`", ""]
        lines.append("Review above findings and add relevant sections or update existing content.")
        lines.append("")

    lines += [
        "---",
        f"*Generated by knowledge_update.py at {search_results['timestamp']}*",
    ]
    return "\n".join(lines)


# ─── Inbox proposal ───────────────────────────────────────────────────────────

def propose_to_inbox(query: str, topic_meta: dict, search_results: dict, confidence: float, dry_run: bool = False):
    """Write a structured inbox capture note."""
    today = datetime.date.today().isoformat()
    slug = slugify(query)
    h = topic_hash(query)
    filename = f"learn-{today}-{h}-{slug[:30]}.md"
    dest = INBOX_PENDING / filename

    proposed_path = topic_meta.get("proposed_path", "04-Knowledge/KB-AI/WATCH_TOPICS.md")
    category = topic_meta.get("category", "knowledge")
    citations = search_results.get("perplexity", {}).get("citations", [])
    primary_url = citations[0] if citations else (search_results.get("brave") or [{}])[0].get("url", "")

    frontmatter = {
        "inbox_id": f"learn-{today}-{h}",
        "status": "pending",
        "proposed_location": proposed_path,
        "confidence": round(confidence, 2),
        "source_agent": "knowledge_update.py",
        "source_url": primary_url,
        "retrieved_at": today,
        "low_risk": confidence >= 0.85,
        "human_gate": "optional" if confidence >= 0.85 else "required",
        "rationale": f"Autonomous web research: {query}",
        "search_query": query,
        "category": category,
        "created": today,
    }

    body = synthesize_results(query, topic_meta, search_results)
    content = "---\n" + yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False) + "---\n\n" + body

    if dry_run:
        print(f"  [DRY-RUN] Would write: {filename} (confidence: {confidence:.2f})")
        return

    dest.write_text(content, encoding="utf-8")
    print(f"  → Proposed: {filename} (confidence: {confidence:.2f})")


# ─── Learning log ─────────────────────────────────────────────────────────────

def append_learning_log(category: str, query: str, confidence: float, proposed: bool):
    today = datetime.datetime.now().isoformat()
    status = "proposed" if proposed else "skipped (low confidence)"
    entry = f"\n## {today} | {category}\n- query: `{query}`\n- confidence: {confidence:.2f}\n- status: {status}\n"
    if LEARNING_LOG.exists():
        with open(LEARNING_LOG, "a", encoding="utf-8") as f:
            f.write(entry)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous vault learning agent")
    parser.add_argument("--topic", help="Only process this topic category (e.g. bruh_stack)")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing to inbox")
    parser.add_argument("--max-per-run", type=int, default=20, help="Max topics to process per run")
    parser.add_argument("--force", action="store_true", help="Ignore cooldown, re-search recent topics")
    args = parser.parse_args()

    if not WATCH_TOPICS_FILE.exists():
        print(f"ERROR: Watch topics file not found: {WATCH_TOPICS_FILE}")
        print("Create 04-Knowledge/KB-AI/WATCH_TOPICS.md with watch_topics frontmatter.")
        sys.exit(1)

    watch_topics = load_watch_topics()
    if not watch_topics:
        print("No watch_topics found in WATCH_TOPICS.md frontmatter.")
        sys.exit(1)

    # Filter by --topic flag
    if args.topic:
        watch_topics = {k: v for k, v in watch_topics.items() if k == args.topic}
        if not watch_topics:
            print(f"Category '{args.topic}' not found. Available: {list(load_watch_topics().keys())}")
            sys.exit(1)

    # Check API keys
    available = []
    if PERPLEXITY_API_KEY:
        available.append("Perplexity")
    if BRAVE_API_KEY:
        available.append("Brave")
    available.append("SearxNG")
    print(f"Search backends: {', '.join(available)}")
    print(f"Vault: {VAULT_ROOT}\n")

    processed = 0
    proposed = 0

    for category, topics in watch_topics.items():
        if processed >= args.max_per_run:
            break
        print(f"\n[{category}]")

        for topic_entry in topics:
            if processed >= args.max_per_run:
                break

            # Support both string and dict entries
            if isinstance(topic_entry, str):
                query = topic_entry
                topic_meta = {"category": category}
            else:
                query = topic_entry.get("query", "")
                topic_meta = {**topic_entry, "category": category}

            if not query:
                continue

            # Cooldown check
            if not args.force and was_recently_searched(query):
                print(f"  [skip] {query} (searched recently)")
                continue

            # Search
            search_results = multi_search(query)
            confidence = score_results(search_results)
            mark_searched(query)
            processed += 1

            # Propose if above threshold
            if confidence >= MIN_CONFIDENCE:
                propose_to_inbox(query, topic_meta, search_results, confidence, dry_run=args.dry_run)
                append_learning_log(category, query, confidence, proposed=True)
                proposed += 1
            else:
                print(f"  [low confidence: {confidence:.2f}] {query}")
                append_learning_log(category, query, confidence, proposed=False)

            time.sleep(1)  # be polite to APIs

    # Outcomes ledger
    now = datetime.datetime.now().isoformat()
    entry = (
        f"\n## Knowledge update — {now}\n"
        f"- topics_processed: {processed}\n"
        f"- proposals_created: {proposed}\n"
        f"- dry_run: {args.dry_run}\n"
    )
    if not args.dry_run and OUTCOMES_LEDGER.exists():
        with open(OUTCOMES_LEDGER, "a", encoding="utf-8") as f:
            f.write(entry)

    print(f"\n✓ Done: {processed} topics searched, {proposed} inbox proposals created")


if __name__ == "__main__":
    main()
