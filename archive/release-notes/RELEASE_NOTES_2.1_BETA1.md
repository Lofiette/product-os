# Release Notes — Codex Product Team 2.1 beta 1

## Theme

Ticketed Memory & Context Economy Patch.

## Added

- `CURRENT.md` active runtime state.
- `TASK_INDEX.md` ticket ledger.
- `tasks/TKT-*.md` active task briefs.
- `context/packets/`, `context/snapshots/`, `chronicle/`, `archive/`.
- `docs/TICKETED_MEMORY.md`.
- `docs/CONTEXT_BUDGET_POLICY.md`.
- `docs/RUNTIME_LOAD_POLICY.md`.
- `docs/TICKET_LIFECYCLE.md`.
- Skills: `context-prune`, `context-snapshot`, `task-ledger`, `ticket-router`, `memory-integrity-check`.
- `scripts/check-memory-integrity.mjs`.

## Changed

- `TASK.md` is now a deprecated compatibility pointer only.
- `CHRONICLE.md` is now a compact rescue summary.
- Startup reads `CURRENT.md`, `TASK_INDEX.md`, compact `CHRONICLE.md`, and the active ticket, not the whole project memory.
- Subagents should receive bounded task/evidence packets.

## Goal

Reduce context bloat without reducing decision quality.
