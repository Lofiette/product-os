# CHRONICLE.md — Compact Rescue Summary

Keep this file short. It is a rescue summary, not a full log.
Move detailed logs into `chronicle/` and evidence into `context/packets/`.

## Context rescue summary

No active product task has been briefed yet. The project now uses ticketed memory: `CURRENT.md` points to the active ticket, `TASK_INDEX.md` tracks tickets, and `tasks/TKT-*.md` stores detailed task briefs.

## Current state

- Active ticket: `TKT-000`
- Phase: Intake / routing
- Next action: read `CURRENT.md`, load the active ticket, and run intake.

## Latest important decisions

| Decision | Reason | Impact |
|---|---|---|
| Use ticketed memory | Prevent `TASK.md` / `CHRONICLE.md` context bloat | Active details move into `tasks/TKT-*.md` |
| Keep `TASK.md` as shim only | Avoid breaking legacy references | Old instructions redirect to current memory files |

## Active blockers

- No user task is briefed yet.

## Next action

Use `ticket-router` and `task-intake` to create or update the active ticket.

## Detailed logs

- Detailed session logs belong in `chronicle/`.
- Evidence packets belong in `context/packets/`.
- Snapshots belong in `context/snapshots/`.

## Subagent completion summary

No real subagents have been spawned yet.
