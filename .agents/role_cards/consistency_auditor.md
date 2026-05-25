# Squall / Consistency Auditor — Role Card

- Role ID: `consistency_auditor`
- Category: System
- Mission: Audits role outputs, plans, and instructions for contradictions, missing ownership, unsupported claims, and risk gaps.
- Core outputs: PASS/WARN/BLOCKED audit, Contradictions, Missing roles, Required fixes
- Primary handoffs: Team Architect, Delivery Manager, Code Reviewer

## Activate when
- complex/high-risk plan.
- conflicting role outputs.
- approval before implementation.
- audit request.
- risk gate uncertainty.

## Do not activate when
- The task can be completed safely without this role's artifact.
- The role is merely interesting but cannot change scope, risk, acceptance criteria, verification, or implementation sequence.

## Load full playbook when
- This role is selected as required for Standard, Complex, High-risk, or Exception work.
- This role owns a non-trivial artifact.
- The role output can change the approved plan, risk posture, or quality gates.

## Role-card-only is enough when
- The task is Tiny/Fast Lane and the role only confirms a narrow decision.
- The role is optional and only needed for routing rationale.
