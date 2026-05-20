---
name: team-routing
description: Use to choose the smallest sufficient team after intake.
---

# Skill: team-routing

## When to use
Use to choose the smallest sufficient team after intake.

## Procedure
1. Read TASK.md, work mode, risk triggers, and language policy.
2. Select mandatory system roles.
3. Apply team budget: fast lane 1–3, standard 4–7, complex 8–12, high-risk 10–15, 16+ requires explicit approval.
4. Use ROLE_ROUTING_MATRIX and RISK_POLICY.
5. Explain selected roles and skipped roles.
6. Define handoff order: discovery → design/product → architecture → risk → QA/review → handoff.
7. Run Consistency Auditor for complex/high-risk plans.
8. Ask for user approval before implementation.

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
