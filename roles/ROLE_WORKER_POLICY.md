# Role and Worker Policy

## Separation

The 50 roles are logical lenses. They are not installed as 50 custom agents.

A worker is an execution container for a bounded independent task. Worker archetypes are introduced in a later execution-plane phase. A worker may receive one accountable role lens plus selected specialist constraints.

## Default

Use roles in the main thread by default.

A role may be delegated only when:

- it owns a bounded independent artifact or review;
- independent context materially improves evidence or challenge quality;
- input and output contracts are explicit;
- read/write scope is bounded;
- timeout, stop condition, and fallback are defined;
- the user approves real delegation when required.

## Worker eligibility metadata

- `never`: system/integration responsibility must remain in the main thread.
- `conditional`: a bounded independent contribution can be delegated.
- `recommended`: reserved for future evidence-backed cases; none are default in Alpha 6.

Worker eligibility never grants spawn permission.

## Parallel writes

Parallel write workers are out of scope for Alpha 6. Future support must require disjoint scopes or isolated worktrees.
