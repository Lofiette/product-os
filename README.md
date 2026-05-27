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

## 2.0 beta 4

This beta hardens operational UI workflows, module design handoff, production readiness, DS enforcement scripts, and explicit spawned/simulated execution transparency. See `docs/RELEASE_NOTES_2.0_BETA2.md`.


## 2.0 beta 4 highlights

- Added Team Culture Layer.
- Added Taste Profile, good/bad examples, Taste Calibration, and Taste Review.
- Added Anticipation Branch for proactive suggestions requiring human confirmation.
- Added Agent Naming Policy to prevent aliases/codenames in spawned-agent summaries.
- Added creative tension review for controlled design/product improvement.


## Taste, culture, and anticipation

Beta 2 adds an operational culture layer, taste calibration/review, example-driven taste boards, controlled creative tension, and expectation anticipation proposals. These are gates and artifacts, not roleplay. Scope-changing anticipation proposals require user approval.

Agent reporting uses exact role IDs only. Any UI-generated personal thread labels are ignored.

## 2.0 beta 4 focus

Beta 4 adds Reference Fidelity and Design Source Authority. If a user provides a visual reference, the system must convert it into a reference contract before implementation and compare rendered output after implementation. DS manifests generated or changed during the same task cannot be used as proof of compliance without explicit approval.
