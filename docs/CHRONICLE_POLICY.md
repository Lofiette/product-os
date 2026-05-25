# CHRONICLE_POLICY.md — Compact Project Memory

The chronicle exists to preserve continuity, not to store the whole conversation.

## Chronicle service vs Chronicle Keeper role

- **Chronicle service update**: compact update performed as part of another role. Does not count against role budget.
- **Chronicle Keeper active role**: Aerith owns a durable memory artifact. Counts when the task is long, multi-step, decision-heavy, high-risk, or context-rescue critical.

## When to update CHRONICLE.md

Update compactly when:
- files changed;
- a decision was made;
- approved scope changed;
- an opportunity event changed direction;
- risk/verification status changed;
- the task is likely to continue later.

Do not expand the chronicle for trivial tasks unless it helps future recovery.

## Compact update schema

```text
Current phase:
Decision/status change:
Files touched:
Verification:
Risks/follow-ups:
Next action:
```

## Long-running tasks

For long tasks, keep `CHRONICLE.md` focused on:
- context rescue summary;
- current command center;
- decisions;
- verification history;
- active risks;
- next action.

Move verbose history to `docs/history/YYYY-MM-DD.md` only when needed.
