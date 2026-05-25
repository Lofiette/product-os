---
name: ai-ml-planning
description: Use for AI/ML/model/agent features.
---

# Skill: ai-ml-planning

## When to use
Use for AI/ML/model/agent features.

## Procedure
1. Define the AI behavior contract: intended outputs, prohibited outputs, uncertainty handling, refusal/fallback.
2. Map model context: user input, system instructions, retrieved data, uploaded files, tools, memory, logs.
3. Map tool permissions: read-only, write-capable, reversible, irreversible, approval-required.
4. Define evaluation plan before implementation: golden set, adversarial set, rubric, regression gate.
5. Define guardrails: prompt injection defenses, data minimization, tool approval gates, human escalation.
6. Define cost/latency budget and caching/retry assumptions.
7. Select required roles: AI/ML Systems Architect, Model Evaluation Specialist, AI Safety Reviewer, Security, Privacy, QA.
8. Produce an AI feature plan and ask approval before implementation.

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
