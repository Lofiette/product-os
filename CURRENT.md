# CURRENT.md — Active Runtime State

This is the first file to read after `AGENTS.md`.
It is a compact control panel, not a full project diary.

## Active ticket

- Current ticket: `TKT-000`
- Ticket file: `tasks/TKT-000-intake.md`
- Status: `Intake`
- Current phase: `Briefing / routing`
- Work mode: `TBD`
- Complexity tier: `TBD`
- Orchestration mode: `TBD`

## Current objective

Run intake, decide whether to continue `TKT-000` or create a new task ticket, then propose the smallest useful role/skill/orchestration plan.

## Must load next

- `TASK_INDEX.md`
- `tasks/TKT-000-intake.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/LANGUAGE_POLICY.md`

Load `docs/QUESTION_TREE.md` only if structured intake is needed.

## Current blockers

- No user task has been briefed yet.

## Next operation

Use `ticket-router` and `task-intake` to create or update an active ticket before any implementation.

## Runtime context budget

| Category | Current state | Default policy |
|---|---|---|
| Active ticket | `tasks/TKT-000-intake.md` | load |
| Closed tickets | none | do not load |
| Chronicle summary | `CHRONICLE.md` | load compact summary only |
| Detailed session logs | `chronicle/` | do not load by default |
| Evidence packets | `context/packets/` | load only for active operation |
| Snapshots | `context/snapshots/` | load only for resume/recovery |
| Archive | `archive/` | never load by default |
| Full playbooks | not loaded | load only for selected active roles |
| Full skill docs | not loaded | load only when selected for operation |

## Do not load by default

- all tickets;
- closed tickets;
- `chronicle/*` detailed logs;
- `context/snapshots/*` old snapshots;
- `archive/*`;
- release notes;
- self-audit reports;
- full role/method libraries.

## Update rules

- Update `CURRENT.md` when the active ticket, next action, blockers, phase, or orchestration mode changes.
- Update `TASK_INDEX.md` when tickets are created, closed, blocked, or re-prioritized.
- Update the active `tasks/TKT-*.md` for scope, acceptance criteria, decisions, role/skill plan, and evidence links.
- Keep `CHRONICLE.md` short. Move detailed logs into `chronicle/`.
