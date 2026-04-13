You are acting as the vault's multi-agent system. Read the task below and route it using the dispatcher protocol.

## Step 1 — Read context
Read these files in order:
1. `00-Brain/HOME.md` (namespace cheat sheet)
2. `01-Agents/DISPATCHER.md` (routing table)
3. `01-Agents/SESSION_HANDOFF.md` (current objective)

## Step 2 — Classify the task
Given the task: **$ARGUMENTS**

Identify:
- Primary domain (strategy / operations / technical / brand / financial / product / security / routing)
- Primary role from the routing table
- Secondary roles needed (if cross-functional)
- Pattern: solo / parallel / sequential

## Step 3 — Execute
For each role involved:
- Read the role file from `01-Agents/roles/[ROLE].md`
- Produce output in the role's `required_sections`
- Stay within the role's `max_tokens`

If parallel: produce each role's output in separate sections labeled `## [Role] Output`
If sequential: pass handoff context between roles using the handoff YAML format from `01-Agents/ORCHESTRATION_PROTOCOL.md`

## Step 4 — Synthesize (CoS)
If multiple roles were involved, run `CoS` synthesis:
- Themes from all outputs
- Conflicts (where roles disagreed)
- Agreed decisions
- Next actions with owners

## Step 5 — Vault updates
If any vault changes are needed, propose them to `06-Inbox/pending/` using the Inbox Capture Template frontmatter. Do NOT write directly to `04-Knowledge/`, `05-Projects/`, or `00-Brain/`.

## Output format
Start with: `Dispatched to: [role(s)] | Pattern: [solo/parallel/sequential]`
Then produce role output(s), then CoS synthesis if applicable.
