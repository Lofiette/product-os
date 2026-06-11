---
name: task-ledger
description: Create, update, close, archive, and re-prioritize ticketed-memory tasks while keeping TASK_INDEX.md and CURRENT.md consistent.
---

# task-ledger

Use whenever a ticket is created, moved, closed, archived, or re-prioritized.

## Process
1. Read `CURRENT.md` and `TASK_INDEX.md`.
2. Decide whether the work needs a new ticket or belongs in the active ticket.
3. Create/update `tasks/TKT-*.md` using the task-ticket template.
4. Update `TASK_INDEX.md` status/current flags.
5. Update `CURRENT.md` if the active ticket changes.
6. Do not put detailed task data into `TASK.md`.

## Output
- Ticket created/updated.
- Status changes.
- Active ticket.
- Next action.
