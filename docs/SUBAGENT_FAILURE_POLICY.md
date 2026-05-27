# SUBAGENT_FAILURE_POLICY.md

This policy prevents the workflow from hanging when one or more real subagents do not finish.

## Key principle

A stuck subagent must not block the quality gate forever. Missing specialist output is a workflow limitation, not a reason to invent results.

## Quorum policy

For each operation, mark roles as:

- `required_for_verdict`: needed to issue final PASS/WARN/BLOCKED.
- `optional_for_depth`: improves the review but may be skipped if unavailable.
- `service_only`: system support, not a blocking reviewer.

If optional agents do not respond, proceed with available evidence and mark them as `not completed`.

## Retry policy

Do not repeatedly spawn the same role.

1. First failure: continue with completed agents and main-thread role simulation.
2. Second need for same expertise: use a smaller review packet or a generic bounded reviewer prompt.
3. Never start a duplicate role-specific agent while a previous one is still running unless the user explicitly approves.

## Fallback hierarchy

1. Completed spawned agent result.
2. Bounded generic reviewer with exact role prompt and review packet.
3. Main-thread role simulation using the same strict checklist.
4. `INSUFFICIENT EVIDENCE` with missing evidence and next action.

## Reporting

Final reports must include:

```markdown
## Subagent completion status
| Agent ID | Expected artifact | Status | Used in verdict | Fallback |
|---|---|---|---|---|
```

Allowed statuses: `completed`, `running/not used`, `failed`, `skipped`, `simulated fallback`, `insufficient evidence`.

## Quality rule

Do not convert a missing specialist result into `PASS`. If a required role fails and no fallback can cover it, the verdict is `PASS WITH WARNINGS` or `BLOCKED` depending on risk.
