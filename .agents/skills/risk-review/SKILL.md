---
name: risk-review
description: Use for security, privacy, performance, dependency, migration, release, AI safety, or incident risk.
---

# Skill: risk-review

## When to use
Use for security, privacy, performance, dependency, migration, release, AI safety, or incident risk.

## Procedure
1. Identify triggers from RISK_POLICY.md.
2. Select risk owners and avoid generic all-role review.
3. Map assets, actors, data, trust boundaries, irreversible actions, and release path.
4. Classify severity and likelihood; distinguish blocker, warning, and follow-up.
5. Define mitigations, tests, monitoring, rollback, and approval gates.
6. State what was not reviewed.
7. Ask user/human owner for approval before high-risk changes.

## Output rules
- Use evidence labels from `docs/EVIDENCE_POLICY.md`.
- Respect `docs/QUALITY_GATES.md` and `docs/RISK_POLICY.md`.
- Follow `docs/LANGUAGE_POLICY.md`.
- Update `TASK.md` and/or `CHRONICLE.md` only when the procedure calls for it.
- Do not implement unless the approved work mode and approval gate allow implementation.
