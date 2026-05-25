# QUALITY_GATES.md

## Gate 1: Before planning

- Intake A completed or fast lane justified.
- Work mode candidates identified.
- Key risks asked about or ruled out.
- Existing repo tasks have a Repo Recon decision: run now / not needed / deferred with reason.

## Gate 2: Before implementation

Required for Standard/Complex/High-risk:
- `TASK.md` updated.
- Team selected with rationale.
- Open assumptions listed.
- Plan created by selected roles.
- Consistency audit PASS or PASS WITH WARNINGS when required.
- User approval received.

Tiny/Fast exception:
- Explicit implementation request + reversible low-risk change can count as approval.
- Still disclose scope and verification.

## Gate 3: Before high-risk changes

Explicit approval is required for auth, security, privacy, migrations, public APIs, dependencies, infra, payments, deletion, AI tool actions, or large refactors.

## Gate 4: Before final answer

- Verification run or limitation disclosed.
- Review level completed according to `docs/REVIEW_LEVELS.md`.
- `CHRONICLE.md` updated when appropriate.
- Risks/follow-ups listed.

## Irreversible Action Gate

Any action that deletes, publishes, sends, purchases, grants/revokes access, changes production data, triggers external side effects, or cannot be easily rolled back requires explicit user approval and relevant risk review.

## Consistency Auditor verdicts

- PASS: no blocking contradictions or missing gates.
- PASS WITH WARNINGS: work may proceed, warnings must be listed.
- BLOCKED: do not implement until issues are resolved.


## Review levels quick map

Use `docs/REVIEW_LEVELS.md`:
- Review 0: Tiny self-check.
- Review 1: Fast Lane lightweight checklist.
- Review 2: active Code Reviewer role.
- Review 3: Code Reviewer plus triggered risk roles.
