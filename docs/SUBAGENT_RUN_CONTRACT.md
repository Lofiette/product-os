# SUBAGENT_RUN_CONTRACT.md

Subagents are useful only when they produce independent, bounded evidence. A spawned role is not a badge of quality by itself.

## Default rule

Prefer the cheapest execution mode that can still produce a reliable result.

- Tiny/Fast Lane: main thread or role simulation.
- Standard UI review: review packet first, then at most one or two spawned reviewers if independent judgment is needed.
- Complex/high-risk: spawned subagents allowed, but each must have a bounded task, explicit evidence requirements, and a stop condition.

## Mandatory run contract

Before spawning any real subagent, define:

| Field | Required content |
|---|---|
| Agent ID | Exact `.codex/agents/<role_id>.toml` name only |
| Operation | Planning / review / audit / implementation / handoff |
| Input packet | Specific files, screenshots, URL, docs, or review packet |
| Read/write | Read-only by default; write permission must be explicit |
| Skills | 1–4 skills maximum unless user approves more |
| Output | Strict artifact schema, max findings, verdict |
| Evidence | File/path/screenshot/DOM/console/DS-source evidence |
| Stop condition | Return compact result; do not expand scope or ask broad questions |

## Bounded output

Every spawned reviewer must return:

```markdown
## Agent result
Agent ID:
Operation:
Verdict: PASS / PASS WITH WARNINGS / BLOCKED / INSUFFICIENT EVIDENCE
Top findings: max 5
Evidence:
Required fixes:
Open blockers:
```

## Anti-hang instructions

Spawned agents must not perform broad repo exploration unless explicitly assigned `repo-recon`. They must not load all playbooks, all skills, or all docs. If required evidence is missing, return `INSUFFICIENT EVIDENCE` with the missing evidence list instead of continuing to search indefinitely.

## UI review default

For current-page UI review, do not spawn multiple full role-specific subagents before creating a `UI Review Packet`. First collect URL, screenshot/render notes, changed files, DS mode, component sources, console errors, and known constraints. Then spawn only the minimum reviewers needed.
