# QUALITY_GATES.md

## Gate 1: Before planning
- Intake A completed or fast lane justified.
- Work mode candidates identified.
- Key risks asked about.

## Gate 2: Before implementation
- `TASK.md` updated.
- Team selected with rationale.
- Open assumptions listed.
- Plan created by selected roles.
- Consistency audit PASS or PASS WITH WARNINGS.
- User approval received.

## Gate 3: Before high-risk changes
Explicit approval is required for auth, security, privacy, migrations, public APIs, dependencies, infra, payments, deletion, large refactors.

## Gate 4: Before final answer
- Verification run or limitation disclosed.
- Review completed when code changed.
- `CHRONICLE.md` updated.
- Risks/follow-ups listed.

## Consistency Auditor verdicts

- PASS: no blocking contradictions or missing gates.
- PASS WITH WARNINGS: work may proceed, warnings must be listed.
- BLOCKED: do not implement until issues are resolved.
