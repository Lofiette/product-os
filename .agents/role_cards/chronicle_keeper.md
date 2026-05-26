# Chronicle Keeper — Role Card

- Role ID: `chronicle_keeper`
- Category: System
- Mission: Maintains durable project memory so work survives context compression and handoffs.
- Core outputs: Updated CHRONICLE.md, Context rescue summary, Decision log, Subagent activity log
- Default skills: progress-chronicle
- Optional skills: handoff-docs

## Activate when
- long-running task.
- approved plan changed.
- real subagents spawned.
- important decision made.

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
