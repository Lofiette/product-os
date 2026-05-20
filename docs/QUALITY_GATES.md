# QUALITY_GATES.md

## Gate 1 — Intake complete

Required before planning:
- TASK.md has work mode, user request, scope, constraints, assumptions, and open questions.
- CHRONICLE.md has a current context rescue summary.
- Team Architect has recommended a role lineup.

## Gate 2 — Plan approval

Required before implementation:
- Specialist roles have provided evidence-backed findings.
- Consolidated plan exists.
- Consistency Auditor has checked ownership, contradictions, missing roles, missing risks, and approval gates.
- User has approved the plan or explicitly approved a bounded fast-lane change.

## Gate 3 — Implementation ready

Required before code changes:
- Files/areas to inspect or change are known.
- Out-of-scope areas are stated.
- Tests/checks are identified.
- High-risk changes are either out of scope or approved.

## Gate 4 — Verification

Required before final delivery:
- Relevant automated checks were run or honestly marked as not runnable.
- Manual verification steps are documented when applicable.
- QA Engineer or equivalent verification logic has assessed coverage.

## Gate 5 — Review

Required before merge recommendation:
- Code Reviewer has compared the diff against TASK.md and approved plan.
- Risk roles reviewed triggered domains.
- Consistency Auditor checked final summary against evidence.

## Gate 6 — Memory update

Required before final response:
- TASK.md reflects final status and plan.
- CHRONICLE.md reflects decisions, files changed, verification, risks, and next action.
