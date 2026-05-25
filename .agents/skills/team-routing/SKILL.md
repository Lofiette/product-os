---
name: team-routing
description: Use to choose the smallest sufficient team after intake.
---

# Skill: team-routing

## When to use
Use to choose the smallest sufficient team after intake.

## Procedure
1. Read TASK.md, work mode, risk triggers, language policy, and complexity tier.
2. Load candidate role cards before full playbooks.
3. Select mandatory system roles.
4. Apply team budget: fast lane 1–3, standard 4–7, complex 8–12, high-risk 10–15, 16+ requires explicit approval.
5. Use ROLE_ROUTING_MATRIX, RISK_POLICY, and the selected-role contract schema.
6. Keep only roles with an owned artifact or decision impact.
7. Explain selected roles and skipped roles.
8. Define handoff order: discovery → design/product → architecture → risk → QA/review → handoff.
9. Load full playbooks only for selected roles that own non-trivial artifacts.
10. Run Consistency Auditor for complex/high-risk plans.
11. Ask for user approval before implementation.

## Output rules
- Use evidence labels from `docs/EVIDENCE_POLICY.md`.
- Respect `docs/QUALITY_GATES.md` and `docs/RISK_POLICY.md`.
- Follow `docs/LANGUAGE_POLICY.md`.
- Update `TASK.md` and/or `CHRONICLE.md` only when the procedure calls for it.
- Do not implement unless the approved work mode and approval gate allow implementation.


## Complexity guardrail

Before executing this skill, classify the task tier with `docs/COMPLEXITY_MODEL.md`. Use the smallest role set and shortest artifact that can safely support the next decision.

## Output schema rule

Use `docs/ROLE_OUTPUT_SCHEMAS.md` for role outputs. If this skill needs a stricter schema, state it before producing recommendations.


## v1.5 role budget classification

Before producing the team lineup, classify contributors as:

- active specialist role;
- system service;
- consulted role card.

Follow `docs/ROLE_SERVICE_BUDGET.md`. Only active specialist roles count against the tier role budget.
