# Codex Product Team 2.0

A role-skill orchestration framework for Codex that simulates or spawns a product team depending on task complexity.

## Start

1. Open this folder in Codex.
2. Paste `FIRST_PROMPT.md`.
3. Answer the intake questions.
4. Review the proposed roles, skills, and orchestration mode.
5. Approve real subagent spawn or ask for cheaper simulation mode.

## Key ideas

- Roles own decisions and artifacts.
- Skills are reusable methods.
- Custom agents are spawnable role executors.
- Real subagents run only after explicit approval.
- UI work requires design recon and design-system compliance when relevant.
- Design systems may be absent, emerging, component-based, documented, or governed.

## Important files

- `AGENTS.md` — core runtime rules.
- `TASK.md` — current task source of truth.
- `CHRONICLE.md` — compact continuity memory.
- `docs/SUBAGENT_ORCHESTRATION.md` — real subagent rules.
- `docs/ROLE_SKILL_ARCHITECTURE.md` — role/skill model.
- `docs/DESIGN_SYSTEM_MODES.md` — how to handle no DS vs rich DS folders.
- `docs/DESIGN_RECON.md` — how to discover design system and UI patterns.
- `docs/UI_QUALITY_GATES.md` — blocking UI quality checks.

## 2.0 beta 1

This beta hardens operational UI workflows, module design handoff, production readiness, DS enforcement scripts, and explicit spawned/simulated execution transparency. See `docs/RELEASE_NOTES_2.0_BETA1.md`.
