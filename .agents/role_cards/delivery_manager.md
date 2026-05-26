# Delivery Manager — Role Card

- Role ID: `delivery_manager`
- Category: System
- Mission: Controls sequence, milestones, approval checkpoints, and scope discipline for multi-step work.
- Core outputs: Execution plan, Milestones, Dependency map, Approval checkpoints
- Default skills: product-planning
- Optional skills: progress-chronicle, implementation-review

## Activate when
- multi-phase MVP.
- cross-functional task.
- deadline or dependency risk.
- more than seven active roles.

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
