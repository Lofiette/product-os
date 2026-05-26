# PRODUCTION_READINESS_GATES.md

Use for production web services, high-risk product changes, public APIs, auth/data-sensitive work, or deployable MVPs.

## Gate verdicts

Each gate returns one of:
- PASS
- PASS WITH WARNINGS
- BLOCKED

## Required gates by area

### Product readiness
- User problem and success criteria are explicit.
- Scope and non-goals are clear.
- Acceptance criteria are testable.

### Architecture readiness
- System boundaries are clear.
- Data flows and integration points are documented.
- Failure modes and fallback behavior are known.

### UI readiness
- Design-system mode is known.
- Screen/module specs exist when UI changes are included.
- DS deviations are documented and approved.

### Security readiness
- Auth, authorization, secrets, data exposure, and abuse cases reviewed when triggered.

### Privacy readiness
- Personal/sensitive data, retention, consent, logging, and third-party sharing reviewed when triggered.

### Reliability/readiness
- Critical paths have monitoring/logging expectations.
- Deploy/rollback plan exists for production deployment.

### Verification readiness
- Unit/integration/e2e/manual checks are identified.
- Unrun checks and environment limitations are explicitly reported.

## BLOCKED examples

- Production service with no rollback plan.
- Auth-sensitive change without authorization review.
- UI implementation with existing DS but custom duplicate components.
- API change without contract impact notes.
- AI tool action with side effects but no confirmation gate.
