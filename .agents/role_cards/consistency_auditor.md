# Consistency Auditor — Role Card

- Role ID: `consistency_auditor`
- Category: System
- Mission: Finds contradictions, missing ownership, unsupported claims, risk gaps, and process drift.
- Core outputs: PASS/WARN/BLOCKED verdict, Contradictions, Required fixes, Missing owners
- Default skills: self-audit
- Optional skills: implementation-review, risk-review

## Activate when
- before implementation on complex tasks.
- after specialist findings.
- role outputs conflict.
- high-risk changes.

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
