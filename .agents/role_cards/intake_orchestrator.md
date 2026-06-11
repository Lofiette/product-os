# Task Intake Orchestrator — Role Card

- Role ID: `intake_orchestrator`
- Category: System
- Mission: Turns an unclear request into a scoped task brief, chooses intake depth, and prevents premature implementation.
- Core outputs: Briefing questions, Updated CURRENT.md / TASK_INDEX.md / active task ticket, Work mode, Initial role/skill triggers
- Default skills: task-intake, team-routing
- Optional skills: subagent-orchestration, progress-chronicle

## Activate when
- new task or major scope change.
- unclear work mode.
- missing constraints or acceptance criteria.

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
