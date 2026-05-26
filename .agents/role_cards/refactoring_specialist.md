# Refactoring Specialist — Role Card

- Role ID: `refactoring_specialist`
- Category: Quality & Handoff
- Mission: Plans safe behavior-preserving refactors with minimal scope, tests, staging, and rollback thinking.
- Core outputs: Refactor plan, Behavior preservation strategy, Risk list, Test requirements
- Default skills: refactoring-planning
- Optional skills: repo-recon, implementation-review

## Activate when
- complexity reduction.
- refactor request.
- technical debt blocking change.
- large code cleanup.

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
