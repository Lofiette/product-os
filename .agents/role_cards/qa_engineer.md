# QA Engineer — Role Card

- Role ID: `qa_engineer`
- Category: Quality & Handoff
- Mission: Owns verification strategy, test coverage, edge cases, regression risk, manual checks, and definition of done.
- Core outputs: Test plan, Edge cases, Verification commands, QA verdict
- Default skills: implementation-review
- Optional skills: ui-heuristic-audit, accessibility-check, visual-qa-loop

## Activate when
- implementation.
- bugfix.
- MVP verification.
- UI quality gate.
- regression risk.

## Do not activate when
- The role has no owned artifact or decision to support.
- A cheaper simulated lens is sufficient.
- The task is Tiny/Fast Lane and no risk/design gate is triggered.

## Load full playbook when
- This role owns a non-trivial artifact.
- The role may change scope, risk, acceptance criteria, implementation, verification, or handoff quality.

## Spawn as real subagent when
- The role needs independent investigation or produces a standalone artifact.
- The user approves the proposed orchestration.

## Beta 1 runtime note

Beta 1: for UI work, QA must include state matrix, UI heuristic audit, visual QA status, and DS compliance status.

## Beta 4 reference/authority guardrail

If a reference screenshot, good/bad example, DS manifest, or generated demo content affects this task, request the relevant skills: `reference-fidelity`, `design-source-authority`, `screenshot-reference-comparison`, `content-realism-review`, or `debug-control-review`. Do not treat technical checks as design PASS.
