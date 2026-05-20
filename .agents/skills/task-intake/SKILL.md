---
name: task-intake
description: Use for Intake A and Intake B when starting or reshaping a task.
---

# Skill: task-intake

## When to use
Use for Intake A and Intake B when starting or reshaping a task.

## Procedure
Intake A:
1. Load core docs only.
2. Confirm language policy.
3. Identify likely work modes.
4. Ask 5–9 adaptive questions max, unless exhaustive briefing is requested.
5. Use fast lane when task is small and low-risk.
6. Do not update product code or final plan.

Intake B:
1. Update TASK.md from user answers.
2. Mark evidence, assumptions, hypotheses, constraints, and open questions.
3. Identify risk triggers.
4. Ask Chronicle Keeper to update CHRONICLE.md when task is multi-step or file-changing.
5. Hand off to Team Architect for role routing.

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
