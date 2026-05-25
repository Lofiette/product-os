---
name: progress-chronicle
description: Use to update CHRONICLE.md after meaningful progress.
---

# Skill: progress-chronicle

## When to use
Use to update CHRONICLE.md after meaningful progress.

## Procedure
1. Update top context rescue summary first: task, phase, approved scope, latest decision, next action.
2. Add timeline entry only for meaningful phase changes, decisions, implementations, checks, or blockers.
3. Log decisions with reason and consequence.
4. Log role activity only when it changes plan, scope, risk, or artifact ownership.
5. Log files touched and verification results.
6. Log unresolved risks and follow-ups.
7. Keep compact English by default; add short Russian note only if it helps the user.

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


## v1.5 chronicle compaction

Follow `docs/CHRONICLE_POLICY.md`.

Use compact chronicle service updates for Tiny/Fast Lane. Activate Aerith / Chronicle Keeper only for long, multi-step, decision-heavy, high-risk, or context-rescue-critical tasks.
