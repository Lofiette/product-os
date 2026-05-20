---
name: implementation-review
description: Use after code changes or for PR/diff review.
---

# Skill: implementation-review

## When to use
Use after code changes or for PR/diff review.

## Procedure
1. Compare diff to TASK.md approved scope and non-goals.
2. Check if quality/risk gates were respected.
3. Check correctness against acceptance criteria.
4. Check tests and verification evidence.
5. Check UI copy, accessibility, design system, performance, security/privacy only when relevant.
6. Check TASK.md/CHRONICLE.md updates when task is multi-step or file-changing.
7. Return APPROVE, REQUEST CHANGES, or NEEDS HUMAN DECISION with severity-ranked findings.

## Output rules
- Use evidence labels from `docs/EVIDENCE_POLICY.md`.
- Respect `docs/QUALITY_GATES.md` and `docs/RISK_POLICY.md`.
- Follow `docs/LANGUAGE_POLICY.md`.
- Update `TASK.md` and/or `CHRONICLE.md` only when the procedure calls for it.
- Do not implement unless the approved work mode and approval gate allow implementation.
