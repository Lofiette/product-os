---
name: implementation-review
description: Use after code changes or on an existing diff to review correctness, scope, tests, risks, and merge readiness.
---

# implementation-review

## Purpose

Use after code changes or on an existing diff to review correctness, scope, tests, risks, and merge readiness.

## Required behavior

- Read `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `TEAM.md`, and relevant docs before acting.
- Keep the work bounded to the current task and work mode.
- Use evidence-backed findings.
- Update or request updates to `TASK.md` and `CHRONICLE.md` when the skill changes task state.
- Respect approval gates in `docs/QUALITY_GATES.md` and risk triggers in `docs/RISK_POLICY.md`.

## Output

Return concise structured output with:

1. What was inspected
2. Findings
3. Decisions or recommendations
4. Risks
5. Required approvals or next steps
