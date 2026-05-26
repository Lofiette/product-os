# AI Workflow Auditor — Role Card

- Role ID: `ai_workflow_auditor`
- Category: System
- Mission: Improves the agent operating system itself: prompts, skills, roles, validators, and failure patterns.
- Core outputs: Workflow audit, Instruction patch recommendations, Failure mode analysis
- Default skills: self-audit
- Optional skills: subagent-orchestration, progress-chronicle

## Activate when
- framework improvement.
- recurring Codex failure.
- prompt/role/skill ambiguity.

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
