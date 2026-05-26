---
name: production-readiness-review
description: Run production readiness gates for product, architecture, UI/DS, security, privacy, performance, release, rollback, and verification.
---


# production-readiness-review

## Purpose

Gate production release or production-grade implementation.

## Procedure

1. Load Production Service Plan.
2. Evaluate each readiness gate.
3. Request missing specialist reviews when triggered.
4. Return PASS/PASS WITH WARNINGS/BLOCKED.

## Output schema

```markdown
## Production Readiness Report

### Verdict
PASS / PASS WITH WARNINGS / BLOCKED

### Product readiness
### Architecture readiness
### UI/design-system readiness
### Security/privacy readiness
### Performance/reliability readiness
### Release/rollback readiness
### Verification readiness
### Blockers
### Approved exceptions
### Follow-ups
```

## BLOCKED conditions

- High-risk area lacks required review.
- Production deployment lacks rollback/release notes.
- UI/DS or security blockers remain unresolved.

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

