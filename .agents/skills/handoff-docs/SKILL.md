---
name: handoff-docs
description: Use to create PR descriptions, release notes, docs, and reviewer checklists.
---

# Skill: handoff-docs

## When to use
Use to create PR descriptions, release notes, docs, and reviewer checklists.

## Procedure
1. Identify audience: reviewer, maintainer, end user, support, release manager, or future agent.
2. Summarize the change in one paragraph.
3. List product/user-visible changes separately from technical changes.
4. List files/areas changed and why.
5. List decisions, alternatives, and tradeoffs when relevant.
6. List verification: commands run, manual checks, checks not run.
7. List risks, rollback notes, and follow-up tasks.
8. Use repository language for technical docs unless user asks otherwise.

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
