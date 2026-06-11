# TASK.md — Deprecated Compatibility Pointer

This project uses **ticketed memory**.
`TASK.md` is no longer the source of truth and must stay short.

Read these files instead:

1. `CURRENT.md` — current active state, active ticket, blockers, next operation.
2. `TASK_INDEX.md` — task/ticket ledger.
3. `tasks/<active-ticket>.md` — detailed active task brief.
4. `CHRONICLE.md` — compact rescue summary.

Do not store detailed task state, scope, acceptance criteria, decisions, logs, role plans, or verification history in this file.

If an older instruction asks you to update `TASK.md`, update:

- `CURRENT.md` for active state and next action;
- `TASK_INDEX.md` for ticket list/status changes;
- `tasks/<active-ticket>.md` for detailed task context;
- `CHRONICLE.md` for compact rescue summary.
