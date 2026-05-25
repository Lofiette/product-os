---
name: self-audit
description: Use to audit the kit itself.
---

# Skill: self-audit

## When to use
Use to audit the kit itself.

## Procedure
1. Run `python scripts/validate_kit.py`.
2. Check required docs exist and are referenced by AGENTS.md/FIRST_PROMPT.md.
3. Check each role has mission, activation, do-not-do, expertise, method, outputs, handoffs, escalation, failure modes.
4. Check role-specific depth: avoid repeated generic phrasing without concrete methods.
5. Check routing consistency: role triggers match ownership and risk policy.
6. Check language policy integration.
7. Check scenario tests for expected roles and missing risks.
8. Return PASS, PASS WITH WARNINGS, or BLOCKED with patch recommendations.

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


## v1.5 runtime hardening checks

Check:
- active roles vs system services vs consulted role cards;
- review level is not heavier than necessary;
- repo recon was run when existing repo files are touched;
- opportunity events are classified OE-0..OE-4;
- Tiny/Fast implicit approval is used only when reversible and low-risk;
- chronicle is compact and useful.
