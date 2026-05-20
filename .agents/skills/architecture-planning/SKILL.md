---
name: architecture-planning
description: Use for technical architecture, stack, system boundaries, and implementation sequencing.
---

# Skill: architecture-planning

## When to use
Use for technical architecture, stack, system boundaries, and implementation sequencing.

## Procedure
1. Read TASK.md, constraints, current architecture, repo structure, and risk policy.
2. Identify quality attributes: correctness, reliability, performance, security, privacy, maintainability, delivery speed.
3. Define options with tradeoffs; do not present one option as inevitable without evidence.
4. Choose the smallest architecture that satisfies approved work mode.
5. Define boundaries: UI, API, domain, data, infra, external integrations, AI/model tools if any.
6. Record ADR-ready decision notes: context, decision, alternatives, consequences.
7. Define verification: tests, contract checks, migration validation, observability, rollback where relevant.
8. Request approval before high-risk or irreversible changes.

## Output rules
- Use evidence labels from `docs/EVIDENCE_POLICY.md`.
- Respect `docs/QUALITY_GATES.md` and `docs/RISK_POLICY.md`.
- Follow `docs/LANGUAGE_POLICY.md`.
- Update `TASK.md` and/or `CHRONICLE.md` only when the procedure calls for it.
- Do not implement unless the approved work mode and approval gate allow implementation.


## v1.3 complexity guardrail

Before executing this skill, classify the task tier with `docs/COMPLEXITY_MODEL.md`. Use the smallest role set and shortest artifact that can safely support the next decision.

## v1.3 output schema rule

Use `docs/ROLE_OUTPUT_SCHEMAS.md` for role outputs. If this skill needs a stricter schema, state it before producing recommendations.
