# CHRONICLE.md

## Compact rescue summary

This workspace uses local ignored Codex runtime memory.

Current active task: `TKT-002 — Product Knowledge Onboarding`.

Transition: `TKT-001 — Stabilize local Codex runtime` is Done. `TKT-002` is In progress and is the current task.

The goal is to prepare bounded Product Knowledge Onboarding before product discovery. Codex should not use root `TASK.md` or root `CHRONICLE.md` as active working memory by default.

Current safety state:

- Project code must not be changed unless explicitly approved.
- Tracked project files must not be changed by default.
- Broad external modules must not be inspected by default.
- Codex must report what files it loaded before acting.
- Real subagents require explicit approval before spawning.

Next step:

Request explicit approval for the next onboarding phase before reading project files or running discovery.
