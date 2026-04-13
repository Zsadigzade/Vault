#!/usr/bin/env python3
"""
run_workflow.py — Execute vault workflows defined in 02-Workflows/triggers/

Usage:
  python scripts/run_workflow.py --id wf-inbox-triage-001
  python scripts/run_workflow.py --list
  python scripts/run_workflow.py --id wf-inbox-triage-001 --dry-run

Reads YAML frontmatter from workflow files and dispatches steps to LLM endpoints
based on the role's model: and endpoint: fields in 01-Agents/roles/.

Compatible with: Ollama (local), Claude API, OpenAI API.
"""

import os
import sys
import re
import json
import argparse
import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ─── Config ──────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = VAULT_ROOT / "02-Workflows" / "triggers"
ROLES_DIR = VAULT_ROOT / "01-Agents" / "roles"
INBOX_PENDING = VAULT_ROOT / "06-Inbox" / "pending"
OUTCOMES_LEDGER = VAULT_ROOT / "07-Learning" / "OUTCOMES_LEDGER.md"

# ─── YAML frontmatter parsing ─────────────────────────────────────────────────

def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return fm, body


def find_workflow(workflow_id: str) -> Path | None:
    """Find a workflow file by its workflow_id."""
    for wf_file in WORKFLOWS_DIR.glob("*.workflow.md"):
        fm, _ = parse_frontmatter(wf_file)
        if fm.get("workflow_id") == workflow_id:
            return wf_file
    return None


def list_workflows() -> list[dict]:
    """List all available workflows."""
    workflows = []
    for wf_file in sorted(WORKFLOWS_DIR.glob("*.workflow.md")):
        fm, _ = parse_frontmatter(wf_file)
        workflows.append({
            "id": fm.get("workflow_id", "unknown"),
            "name": wf_file.stem,
            "trigger": fm.get("trigger", {}).get("type", "?"),
            "schedule": fm.get("trigger", {}).get("schedule", ""),
            "status": fm.get("execution", {}).get("status", "idle"),
        })
    return workflows


# ─── Role loading ──────────────────────────────────────────────────────────────

def load_role(role_name: str) -> dict:
    """Load a role's frontmatter from 01-Agents/roles/."""
    role_file = ROLES_DIR / f"{role_name}.md"
    if not role_file.exists():
        raise FileNotFoundError(f"Role file not found: {role_file}")
    fm, _ = parse_frontmatter(role_file)
    return fm


# ─── LLM dispatch ─────────────────────────────────────────────────────────────

def invoke_role(role_name: str, task: str, context: str = "", dry_run: bool = False) -> str:
    """Invoke a role's LLM with a task. Returns the response text."""
    role = load_role(role_name)
    model = role.get("model", "ollama/llama3.3")
    endpoint = role.get("endpoint", "http://localhost:11434")
    temperature = role.get("temperature", 0.3)
    max_tokens = role.get("output_format", {}).get("max_tokens", 800)

    system_prompt = build_system_prompt(role)

    if dry_run:
        print(f"  [DRY-RUN] Would invoke {role_name} ({model}) at {endpoint}")
        print(f"  [DRY-RUN] Task: {task[:100]}...")
        return f"[DRY-RUN response from {role_name}]"

    # Ollama
    if model.startswith("ollama/") or "localhost:11434" in endpoint:
        return call_ollama(endpoint, model.replace("ollama/", ""), system_prompt, task, context, temperature, max_tokens)

    # Claude
    if "anthropic.com" in endpoint or model.startswith("claude"):
        return call_claude(model, system_prompt, task, context, max_tokens)

    # OpenAI
    if "openai.com" in endpoint or model.startswith("gpt"):
        return call_openai(model, system_prompt, task, context, temperature, max_tokens)

    raise ValueError(f"Unknown endpoint/model combination: {endpoint} / {model}")


def build_system_prompt(role: dict) -> str:
    """Build system prompt from role definition."""
    name = role.get("role_name", role.get("role", "Agent"))
    domains = ", ".join(role.get("owns_domains", []))
    scope = role.get("decision_scope", {}).get("owns", [])
    required_sections = role.get("output_format", {}).get("required_sections", [])
    return (
        f"You are the {name}. "
        f"Your domains: {domains}. "
        f"Your decision scope: {', '.join(scope)}. "
        f"Structure your response with these sections: {', '.join(required_sections)}. "
        f"Propose any vault updates by describing them — do not write files directly."
    )


def call_ollama(endpoint: str, model: str, system: str, user: str, context: str, temperature: float, max_tokens: int) -> str:
    try:
        import urllib.request
        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": f"{context}\n\n{user}" if context else user},
            ],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }).encode()
        req = urllib.request.Request(
            f"{endpoint.rstrip('/')}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["message"]["content"]
    except Exception as e:
        return f"[Ollama error: {e}]"


def call_claude(model: str, system: str, user: str, context: str, max_tokens: int) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "[ERROR: ANTHROPIC_API_KEY env var not set]"
    try:
        import urllib.request
        payload = json.dumps({
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": f"{context}\n\n{user}" if context else user}],
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except Exception as e:
        return f"[Claude error: {e}]"


def call_openai(model: str, system: str, user: str, context: str, temperature: float, max_tokens: int) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "[ERROR: OPENAI_API_KEY env var not set]"
    try:
        import urllib.request
        payload = json.dumps({
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": f"{context}\n\n{user}" if context else user},
            ],
        }).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OpenAI error: {e}]"


# ─── Workflow execution ────────────────────────────────────────────────────────

def execute_workflow(workflow_id: str, dry_run: bool = False):
    wf_file = find_workflow(workflow_id)
    if not wf_file:
        print(f"ERROR: Workflow '{workflow_id}' not found in {WORKFLOWS_DIR}")
        sys.exit(1)

    fm, _ = parse_frontmatter(wf_file)
    steps = fm.get("steps", [])
    name = fm.get("workflow_id", workflow_id)

    print(f"\n{'='*60}")
    print(f"Workflow: {name}")
    print(f"Steps: {len(steps)}")
    print(f"Dry-run: {dry_run}")
    print(f"{'='*60}\n")

    context = {}
    results = []

    for step in steps:
        step_id = step.get("id", "?")
        step_name = step.get("name", step_id)
        agent = step.get("agent", "CoS")
        action = step.get("action", "")
        params = step.get("params", {})
        output_var = step.get("output_var", f"result_{step_id}")
        condition = step.get("condition", None)

        print(f"[{step_id}] {step_name} ({agent})")

        # Evaluate condition
        if condition:
            print(f"  Condition: {condition} — skipping evaluation in this version")

        # Build task description from step
        task = f"Action: {action}\nParams: {json.dumps(params, indent=2)}\nContext vars: {list(context.keys())}"

        # Invoke role
        response = invoke_role(agent, task, dry_run=dry_run)
        context[output_var] = response
        results.append({"step": step_id, "agent": agent, "output_var": output_var, "response": response})
        print(f"  → {output_var}: {str(response)[:80]}...")

    # Log to outcomes ledger
    log_outcome(workflow_id, len(steps), dry_run)

    print(f"\n✓ Workflow '{workflow_id}' complete ({len(steps)} steps)")
    return results


def log_outcome(workflow_id: str, steps_run: int, dry_run: bool):
    """Append a run entry to the outcomes ledger."""
    now = datetime.datetime.now().isoformat()
    entry = (
        f"\n## Run: {workflow_id} — {now}\n"
        f"- steps_run: {steps_run}\n"
        f"- dry_run: {dry_run}\n"
        f"- status: {'dry-run' if dry_run else 'completed'}\n"
    )
    if not dry_run and OUTCOMES_LEDGER.exists():
        with open(OUTCOMES_LEDGER, "a", encoding="utf-8") as f:
            f.write(entry)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run vault automation workflows")
    parser.add_argument("--id", help="Workflow ID to run (e.g. wf-inbox-triage-001)")
    parser.add_argument("--list", action="store_true", help="List all available workflows")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without calling LLMs or writing files")
    args = parser.parse_args()

    if args.list:
        workflows = list_workflows()
        print(f"\n{'ID':<35} {'Trigger':<10} {'Schedule':<20} {'Status'}")
        print("-" * 80)
        for wf in workflows:
            print(f"{wf['id']:<35} {wf['trigger']:<10} {wf['schedule']:<20} {wf['status']}")
        return

    if args.id:
        execute_workflow(args.id, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
