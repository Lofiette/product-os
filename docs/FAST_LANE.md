# FAST_LANE.md

Use Fast Lane when the task is small, low-risk, and well-scoped.

## Fast Lane criteria

All must be true:
- No security/privacy/payment/auth/data migration/AI autonomy risk.
- No public API or database schema change.
- No new production dependency.
- No broad refactor.
- User request is clear enough to implement or review with at most 3 clarifying questions.
- The change is reversible or easy to inspect.

## Fast Lane process

1. Ask 0 to 3 clarifying questions.
2. Select 1 to 3 active roles, excluding compact system services.
3. Use role cards before full playbooks.
4. Update `TASK.md` briefly if files will change or decisions matter.
5. Implement or review only the requested scope.
6. Run the smallest relevant verification.
7. Apply Review 0 or Review 1 from `docs/REVIEW_LEVELS.md`.
8. Update `CHRONICLE.md` only as a compact service update when files or decisions changed.

## Implicit approval

If the user explicitly asked to implement, no risk gate is triggered, and the change is reversible, the request counts as implementation approval. Do not stop for a ceremonial approval.

## Fast Lane team examples

- UI copy change: Garnet / UX Writer, optionally Zidane / Frontend Architect. Review 0/1 service.
- Small bugfix: Rikku / QA Engineer, relevant architect, Review 1 or Agrias only if meaningful diff.
- Dependency question: Edge / Dependency Curator, Vincent / Security Reviewer, Sabin / Performance Engineer only when risk triggers justify them.

Fast Lane never bypasses risk gates.

## Creative methods in Fast Lane

Do not run creative frameworks by default. Use at most one lightweight creative pass only if:
- the user explicitly asks for alternatives;
- the task is a small UX/copy/product improvement where alternatives can improve the exact requested change;
- the creative pass will not expand scope or trigger extra active roles beyond the Fast Lane budget.
