#!/usr/bin/env python3
"""
vault_health.py — Generate vault health report and propose to inbox

Usage:
  python scripts/vault_health.py             # Full health check, propose to inbox
  python scripts/vault_health.py --print     # Print report without writing to inbox
  python scripts/vault_health.py --summaries-only  # Only regenerate namespace summaries

Checks:
  - Orphan notes (no incoming or outgoing links)
  - Stale notes (updated > 90 days ago)
  - Inbox backlog count and oldest item age
  - Role file freshness (should be updated at least every 30 days)
  - Workflow last-run status
  - Total note counts per namespace
"""

import os
import sys
import re
import datetime
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ─── Config ──────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(__file__).parent.parent
INBOX_PENDING = VAULT_ROOT / "06-Inbox" / "pending"
VAULT_HEALTH_FILE = VAULT_ROOT / "07-Learning" / "VAULT_HEALTH.md"
OUTCOMES_LEDGER = VAULT_ROOT / "07-Learning" / "OUTCOMES_LEDGER.md"
ROLES_DIR = VAULT_ROOT / "01-Agents" / "roles"
WORKFLOWS_DIR = VAULT_ROOT / "02-Workflows" / "triggers"
SUMMARIES_DIR = VAULT_ROOT / "07-Learning" / "summaries"

STALE_DAYS = 90
ROLE_STALE_DAYS = 30

EXCLUDED_DIRS = {".git", ".obsidian", "attachments", "scripts"}
EXCLUDED_FILES = {".gitkeep"}

# ─── Helpers ──────────────────────────────────────────────────────────────────

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


def all_md_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob("*.md"):
        if any(part in EXCLUDED_DIRS for part in p.parts):
            continue
        if p.name in EXCLUDED_FILES:
            continue
        files.append(p)
    return files


def extract_links(text: str) -> set[str]:
    """Extract [[wikilinks]] and [text](paths) from markdown."""
    wikilinks = set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text))
    mdlinks = set(re.findall(r'\[(?:[^\]]+)\]\(([^)]+)\)', text))
    return wikilinks | mdlinks


def namespace_from_path(filepath: Path) -> str:
    rel = filepath.relative_to(VAULT_ROOT)
    return str(rel.parts[0]) if rel.parts else "root"


# ─── Health checks ────────────────────────────────────────────────────────────

def check_stale_notes(all_files: list[Path]) -> list[dict]:
    stale = []
    cutoff = datetime.date.today() - datetime.timedelta(days=STALE_DAYS)
    for f in all_files:
        fm, _ = parse_frontmatter(f)
        updated_raw = fm.get("updated")
        if not updated_raw:
            continue
        try:
            updated = datetime.date.fromisoformat(str(updated_raw))
            if updated < cutoff:
                days_old = (datetime.date.today() - updated).days
                stale.append({"file": str(f.relative_to(VAULT_ROOT)), "days_old": days_old, "updated": str(updated)})
        except Exception:
            pass
    return sorted(stale, key=lambda x: x["days_old"], reverse=True)


def check_orphans(all_files: list[Path]) -> list[str]:
    """Find notes with no outgoing links (rough approximation of orphans)."""
    orphans = []
    for f in all_files:
        _, body = parse_frontmatter(f)
        links = extract_links(body)
        if not links and f.stat().st_size > 100:  # ignore tiny files
            orphans.append(str(f.relative_to(VAULT_ROOT)))
    return orphans


def check_inbox_backlog() -> dict:
    items = [p for p in INBOX_PENDING.glob("*.md") if p.name != ".gitkeep"]
    if not items:
        return {"count": 0, "oldest_days": 0}
    oldest_days = 0
    for item in items:
        fm, _ = parse_frontmatter(item)
        created_raw = fm.get("created")
        if created_raw:
            try:
                created = datetime.date.fromisoformat(str(created_raw))
                days = (datetime.date.today() - created).days
                oldest_days = max(oldest_days, days)
            except Exception:
                pass
    return {"count": len(items), "oldest_days": oldest_days}


def check_role_freshness() -> list[dict]:
    stale_roles = []
    cutoff = datetime.date.today() - datetime.timedelta(days=ROLE_STALE_DAYS)
    for role_file in ROLES_DIR.glob("*.md"):
        fm, _ = parse_frontmatter(role_file)
        updated_raw = fm.get("updated")
        if updated_raw:
            try:
                updated = datetime.date.fromisoformat(str(updated_raw))
                if updated < cutoff:
                    stale_roles.append({"role": role_file.stem, "updated": str(updated)})
            except Exception:
                pass
    return stale_roles


def check_workflow_status() -> list[dict]:
    results = []
    for wf_file in WORKFLOWS_DIR.glob("*.workflow.md"):
        fm, _ = parse_frontmatter(wf_file)
        results.append({
            "id": fm.get("workflow_id", wf_file.stem),
            "status": fm.get("execution", {}).get("status", "unknown"),
            "last_run": fm.get("execution", {}).get("last_run", "never"),
        })
    return results


def count_by_namespace(all_files: list[Path]) -> dict[str, int]:
    counts = defaultdict(int)
    for f in all_files:
        ns = namespace_from_path(f)
        counts[ns] += 1
    return dict(sorted(counts.items()))


# ─── Report generation ────────────────────────────────────────────────────────

def generate_report(all_files: list[Path]) -> str:
    today = datetime.date.today().isoformat()
    stale = check_stale_notes(all_files)
    orphans = check_orphans(all_files)
    inbox = check_inbox_backlog()
    roles = check_role_freshness()
    workflows = check_workflow_status()
    ns_counts = count_by_namespace(all_files)

    lines = [
        f"# Vault Health Report — {today}",
        "",
        "## Summary",
        f"- Total notes: {len(all_files)}",
        f"- Stale notes (>{STALE_DAYS}d): {len(stale)}",
        f"- Orphan notes (no links): {len(orphans)}",
        f"- Inbox pending: {inbox['count']} (oldest: {inbox['oldest_days']}d ago)",
        f"- Stale role files (>{ROLE_STALE_DAYS}d): {len(roles)}",
        "",
        "## Notes by namespace",
        "",
        "| Namespace | Count |",
        "|-----------|-------|",
    ]
    for ns, count in ns_counts.items():
        lines.append(f"| `{ns}` | {count} |")

    if stale:
        lines += [
            "",
            f"## Stale notes (>{STALE_DAYS} days)",
            "",
            "| File | Days old | Last updated |",
            "|------|---------|-------------|",
        ]
        for item in stale[:20]:  # cap at 20
            lines.append(f"| `{item['file']}` | {item['days_old']} | {item['updated']} |")
        if len(stale) > 20:
            lines.append(f"| ... and {len(stale) - 20} more | | |")

    if orphans:
        lines += [
            "",
            "## Orphan notes (no outgoing links)",
            "",
        ]
        for o in orphans[:15]:
            lines.append(f"- `{o}`")

    if roles:
        lines += [
            "",
            "## Stale role files",
            "",
        ]
        for r in roles:
            lines.append(f"- `{r['role']}` — last updated {r['updated']}")

    lines += [
        "",
        "## Workflow status",
        "",
        "| Workflow | Status | Last run |",
        "|----------|--------|---------|",
    ]
    for wf in workflows:
        lines.append(f"| `{wf['id']}` | {wf['status']} | {wf['last_run']} |")

    lines += [
        "",
        "---",
        "",
        "*Generated by `scripts/vault_health.py`*",
    ]

    return "\n".join(lines)


def propose_to_inbox(report: str):
    """Write health report to inbox as a low-risk pending item."""
    today = datetime.date.today().isoformat()
    inbox_id = f"health-{today}"
    filename = f"health-report-{today}.md"
    dest = INBOX_PENDING / filename

    frontmatter = {
        "inbox_id": inbox_id,
        "status": "pending",
        "proposed_location": "07-Learning/VAULT_HEALTH.md",
        "confidence": 1.0,
        "source_agent": "vault_health.py",
        "low_risk": True,
        "human_gate": "optional",
        "rationale": "Automated vault health metrics snapshot",
        "created": today,
    }

    content = "---\n" + yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False) + "---\n\n" + report
    dest.write_text(content, encoding="utf-8")
    print(f"Health report proposed to inbox: {dest.name}")
    print("Review with: python scripts/approve_inbox.py")


def generate_summaries(all_files: list[Path]):
    """Generate per-namespace summary stubs (token-efficient overviews)."""
    ns_files = defaultdict(list)
    for f in all_files:
        ns = namespace_from_path(f)
        ns_files[ns].append(f)

    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    for ns, files in ns_files.items():
        summary_path = SUMMARIES_DIR / f"{ns}-summary.md"
        today = datetime.date.today().isoformat()

        tldr_lines = []
        for f in sorted(files)[:10]:
            fm, _ = parse_frontmatter(f)
            tldr = fm.get("tldr", "")
            if tldr:
                tldr_lines.append(f"- `{f.name}`: {tldr}")

        content = (
            f"---\ngenerated: {today}\nnamespace: \"{ns}\"\nnote_count: {len(files)}\n---\n\n"
            f"# {ns} — Summary\n\n"
            f"**Notes:** {len(files)}\n\n"
            + ("\n".join(tldr_lines) if tldr_lines else "*No TL;DRs found — add `tldr:` to frontmatter.*")
            + "\n"
        )
        summary_path.write_text(content, encoding="utf-8")
        print(f"  Summary written: {summary_path.name}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Vault health check and reporting")
    parser.add_argument("--print", action="store_true", help="Print report to stdout, don't write to inbox")
    parser.add_argument("--summaries-only", action="store_true", help="Only regenerate namespace summaries")
    args = parser.parse_args()

    all_files = all_md_files(VAULT_ROOT)
    print(f"Found {len(all_files)} markdown files in vault.\n")

    if args.summaries_only:
        print("Generating namespace summaries...")
        generate_summaries(all_files)
        return

    report = generate_report(all_files)

    if args.print:
        print(report)
        return

    propose_to_inbox(report)


if __name__ == "__main__":
    main()
