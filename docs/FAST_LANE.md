# FAST_LANE.md

Use Fast Lane when the task is small, low-risk, and well-scoped.

## Fast Lane criteria

All must be true:
- No security/privacy/payment/auth/data migration risk.
- No public API or database schema change.
- No new production dependency.
- No broad refactor.
- User request is clear enough to implement or review with at most 3 clarifying questions.

## Fast Lane process

1. Ask 0 to 3 clarifying questions.
2. Select 1 to 3 roles.
3. Update `TASK.md` briefly if files will change.
4. Implement or review only the requested scope.
5. Run the smallest relevant verification.
6. Update `CHRONICLE.md` only if the work changes files or decisions.

## Fast Lane team examples

- UI copy change: Garnet / UX Writer, Zidane / Frontend Architect, optionally Agrias / Code Reviewer.
- Small bugfix: Rikku / QA Engineer, relevant architect, Agrias / Code Reviewer.
- Dependency question: Edge / Dependency Curator, Vincent / Security Reviewer, Sabin / Performance Engineer.

Fast Lane never bypasses risk gates.
