#!/usr/bin/env python3
"""
approve_inbox.py — Interactive inbox review and approval

Usage:
  python scripts/approve_inbox.py              # Interactive review (default dry-run)
  python scripts/approve_inbox.py --move       # Actually move approved files
  python scripts/approve_inbox.py --auto-low-risk --move  # Auto-approve low_risk: true items

Reads pending/ items, presents each for human review, then:
  - approve → moves to approved/ (and optionally files to proposed_location)
  - reject  → moves to archive/ with rejection_reason
  - skip    → leaves in pending/ for next review

See 06-Inbox/INBOX_PROTOCOL.md for governance rules.
"""

import os
import sys
import shutil
import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ─── Config ──────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(__file__).parent.parent
INBOX_PENDING = VAULT_ROOT / "06-Inbox" / "pending"
INBOX_APPROVED = VAULT_ROOT / "06-Inbox" / "approved"
INBOX_ARCHIVE = VAULT_ROOT / "06-Inbox" / "archive"
OUTCOMES_LEDGER = VAULT_ROOT / "07-Learning" / "OUTCOMES_LEDGER.md"

# Paths agents can NEVER write to (Tier 3 — hard block)
TIER3_PREFIXES = [
    "00-Brain/VAULT_CONSTITUTION",
    "01-Agents/roles/",
    "00-Brain/HOME",
]

# ─── Frontmatter parsing ──────────────────────────────────────────────────────

def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return fm, body


def update_frontmatter(filepath: Path, updates: dict):
    """Update specific frontmatter fields in a file."""
    fm, body = parse_frontmatter(filepath)
    fm.update(updates)
    new_content = "---\n" + yaml.dump(fm, allow_unicode=True, default_flow_style=False) + "---\n\n" + body
    filepath.write_text(new_content, encoding="utf-8")


# ─── Safety checks ────────────────────────────────────────────────────────────

def is_tier3_path(proposed_location: str) -> bool:
    """Block writes to Tier 3 (brain/constitution/roles) paths."""
    for prefix in TIER3_PREFIXES:
        if proposed_location.startswith(prefix):
            return True
    return False


# ─── Review actions ───────────────────────────────────────────────────────────

def approve_item(item_path: Path, move: bool = False) -> bool:
    """Approve an inbox item — move to approved/ and optionally file."""
    fm, body = parse_frontmatter(item_path)
    proposed_location = fm.get("proposed_location", "")

    # Safety: block Tier 3
    if proposed_location and is_tier3_path(proposed_location):
        print(f"  ⛔ BLOCKED: Proposed location is Tier 3 (read-only): {proposed_location}")
        print(f"     This change requires human direct edit.")
        return False

    if move:
        # Move to approved/
        dest = INBOX_APPROVED / item_path.name
        update_frontmatter(item_path, {"status": "approved", "approved_at": datetime.date.today().isoformat()})
        shutil.move(str(item_path), str(dest))
        print(f"  ✓ Moved to approved/: {item_path.name}")

        # File to proposed location if specified
        if proposed_location:
            target = VAULT_ROOT / proposed_location
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                print(f"  ⚠ Target exists: {proposed_location} — skipping overwrite. Review manually.")
            else:
                update_frontmatter(dest, {"status": "filed", "filed_at": datetime.date.today().isoformat()})
                shutil.copy(str(dest), str(target))
                print(f"  ✓ Filed to: {proposed_location}")
    else:
        print(f"  [DRY-RUN] Would approve and move: {item_path.name}")
        if proposed_location:
            print(f"  [DRY-RUN] Would file to: {proposed_location}")

    log_outcome(item_path.name, "approved", proposed_location)
    return True


def reject_item(item_path: Path, reason: str, move: bool = False):
    """Reject an inbox item — move to archive/."""
    if move:
        dest = INBOX_ARCHIVE / item_path.name
        update_frontmatter(item_path, {
            "status": "rejected",
            "rejection_reason": reason,
            "rejected_at": datetime.date.today().isoformat(),
        })
        shutil.move(str(item_path), str(dest))
        print(f"  ✗ Rejected → archive/: {item_path.name}")
    else:
        print(f"  [DRY-RUN] Would reject: {item_path.name} (reason: {reason})")

    log_outcome(item_path.name, "rejected", reason)


# ─── Logging ──────────────────────────────────────────────────────────────────

def log_outcome(filename: str, action: str, detail: str):
    now = datetime.datetime.now().isoformat()
    entry = f"\n## Inbox review: {filename} — {now}\n- action: {action}\n- detail: {detail}\n"
    if OUTCOMES_LEDGER.exists():
        with open(OUTCOMES_LEDGER, "a", encoding="utf-8") as f:
            f.write(entry)


# ─── Main review loop ─────────────────────────────────────────────────────────

def review_item(item_path: Path, move: bool, auto_low_risk: bool) -> str:
    """Present one item for review. Returns: approved / rejected / skipped."""
    fm, body = parse_frontmatter(item_path)

    print(f"\n{'─'*60}")
    print(f"File:       {item_path.name}")
    print(f"Status:     {fm.get('status', '?')}")
    print(f"Agent:      {fm.get('source_agent', '?')}")
    print(f"Confidence: {fm.get('confidence', '?')}")
    print(f"Location:   {fm.get('proposed_location', 'not specified')}")
    print(f"Rationale:  {fm.get('rationale', '?')}")
    print(f"Low risk:   {fm.get('low_risk', False)}")
    if fm.get("source_url"):
        print(f"Source URL: {fm.get('source_url')}")

    # Auto-approve low-risk items if flag set
    if auto_low_risk and fm.get("low_risk") is True:
        print("  → Auto-approving (low_risk: true)")
        approve_item(item_path, move=move)
        return "approved"

    print(f"\n{'─'*40}")
    print("Content preview:")
    preview = body[:400].replace("\n", "\n  ")
    print(f"  {preview}")
    if len(body) > 400:
        print(f"  ... ({len(body) - 400} more chars)")

    print(f"\n{'─'*40}")
    print("[a]pprove  [r]eject  [s]kip  [q]uit")
    choice = input("Choice: ").strip().lower()

    if choice == "a":
        approve_item(item_path, move=move)
        return "approved"
    elif choice == "r":
        reason = input("Rejection reason: ").strip() or "Rejected by human review"
        reject_item(item_path, reason, move=move)
        return "rejected"
    elif choice == "q":
        print("Exiting review.")
        sys.exit(0)
    else:
        print("  → Skipped")
        return "skipped"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Review and approve vault inbox items")
    parser.add_argument("--move", action="store_true", help="Actually move files (default: dry-run)")
    parser.add_argument("--auto-low-risk", action="store_true", help="Auto-approve items with low_risk: true")
    parser.add_argument("--sort-by-confidence", action="store_true", default=True, help="Review highest-confidence items first")
    args = parser.parse_args()

    if not args.move:
        print("DRY-RUN mode (use --move to actually move files)\n")

    # Collect pending items (skip .gitkeep)
    items = [p for p in INBOX_PENDING.glob("*.md") if p.name != ".gitkeep"]

    if not items:
        print("No pending items in inbox.")
        return

    # Sort by confidence descending
    if args.sort_by_confidence:
        def get_confidence(p):
            fm, _ = parse_frontmatter(p)
            return float(fm.get("confidence", 0))
        items = sorted(items, key=get_confidence, reverse=True)

    print(f"Found {len(items)} pending item(s).")

    stats = {"approved": 0, "rejected": 0, "skipped": 0}

    for item in items:
        result = review_item(item, move=args.move, auto_low_risk=args.auto_low_risk)
        stats[result] = stats.get(result, 0) + 1

    print(f"\n{'='*40}")
    print(f"Review complete: {stats['approved']} approved, {stats['rejected']} rejected, {stats['skipped']} skipped")


if __name__ == "__main__":
    main()
