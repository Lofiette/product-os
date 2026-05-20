---
name: research-planning
description: Use for market, UX, CX, product discovery, and evidence-building tasks.
---

# Skill: research-planning

## When to use
Use for market, UX, CX, product discovery, and evidence-building tasks.

## Procedure
1. Define the decision the research must support.
2. Split questions into market, UX, CX, product, analytics, support, and domain categories.
3. Choose method per question: desk research, interviews, usability test, survey, analytics review, support-ticket analysis, competitor teardown.
4. Define evidence sources and confidence thresholds.
5. Define participant/data requirements and ethical/privacy constraints.
6. Create research artifacts: plan, protocol, screener, analysis approach, synthesis output.
7. Mark unsupported claims as assumptions or hypotheses.
8. Identify what needs web search or user-provided evidence before claims can be made.

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
