---
name: self-audit
description: Use before delivering a plan or archive to check internal consistency: roles, scope, gates, file references, contradictions, and missing handoffs.
---

# self-audit

## Purpose

Use before delivering a plan or archive to check internal consistency: roles, scope, gates, file references, contradictions, and missing handoffs.

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


## Self-audit checklist

Check:
- all selected roles exist in TEAM.md and `.codex/agents`;
- every selected role has a clear reason;
- skipped high-risk roles have a rationale;
- TASK.md, CHRONICLE.md, and the current plan agree;
- no implementation is happening before approval;
- all required gates are satisfied;
- file references exist when file claims are made;
- final output does not claim checks were run unless they were run.
