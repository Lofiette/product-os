# TICKETED_MEMORY.md — Ticketed Memory Model

Ticketed memory prevents long-running work from bloating `TASK.md` and `CHRONICLE.md`.

## Source of truth

- `CURRENT.md` is the active control panel.
- `TASK_INDEX.md` is the ticket ledger.
- `tasks/TKT-*.md` contains detailed task context.
- `CHRONICLE.md` is a compact rescue summary only.
- `context/packets/*` stores operation evidence.
- `context/snapshots/*` stores checkpoints.
- `chronicle/*` stores detailed logs.
- `archive/*` stores closed/inactive material.

## Rule

Do not load the whole project memory. Load the smallest packet that can change the next decision.

## Ticket creation triggers

Create a new ticket when work has a distinct deliverable, acceptance criteria, blocker, approval boundary, or subagent/evidence packet. Do not create tickets for tiny notes.

## Active ticket rule

There should be exactly one primary active ticket in `CURRENT.md` and `TASK_INDEX.md`. Secondary linked tickets are allowed only when they block or directly support the active ticket.

## Compatibility

`TASK.md` is a compatibility pointer. It must not contain task details.
