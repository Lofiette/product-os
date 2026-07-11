---
name: cpt-delegation
description: Use explicitly to plan, launch, monitor, and recover bounded worker delegation; not for simple or tightly coupled tasks.
---

# CPT Delegation

## Use when

- Independent analysis or review artifacts can run in parallel.
- A worker can operate with a small input packet and clear stop condition.

## Do not use when

- A single main-thread pass is cheaper and equally reliable.
- Workers would edit overlapping files or depend on each other sequentially.
- The user has not approved real delegation.

## Required inputs

- Approved worker budget, worker archetypes, role lenses, input packets, read/write scopes, deadlines, and quorum.
- Active task and authorization lease.

## Method

1. Define why delegation improves quality, latency, or context isolation.
2. Choose worker archetype and inject only the necessary role lens.
3. Create a run contract: task, evidence, scope, output schema, deadline, stop condition, and write isolation.
4. Request explicit user approval for the lineup and cost.
5. Materialize the plan through CPT orchestration runs and bounded worker contracts.
6. Launch no more workers than the approved budget; prefer read-only workers and one contract per archetype.
7. Require managed Git worktrees for parallel writable workers; never auto-merge.
8. Track approved, active, returned, completed, partial, failed, timed-out, cancel-requested, cancelled, and needs-reconcile states on disk.
9. Require a structured result after native return; only `success` satisfies required quorum.
10. Apply deadline, cancellation, reconciliation, and quorum rules; do not wait indefinitely.
11. Consolidate conflicts through the main-thread decision owner.
12. Close, skip, cancel, or explicitly defer remaining workers and record missing evidence.

## Output contract

Produce a compact artifact containing:

- `Approved worker lineup and contracts.`
- `Worker status table and artifacts used.`
- `Conflicts, quorum result, fallback, and final consolidation.`
- `Remaining workers closed/cancelled and runtime checkpoint updated.`

## Evidence standard

- A worker result is evidence only within its declared scope.
- Missing worker output cannot be converted into PASS.

## Stop and escalate

- Approval is missing.
- Write scopes overlap without worktree or disjoint-file proof.
- Worker registry is inconsistent after compaction.
- Required quorum cannot be met.

## Failure modes to avoid

- Spawning one worker per logical role.
- Waiting for all results without a deadline.
- Launching duplicate workers after one appears slow.

## Runtime commands

Use the managed CLI described in `ORCHESTRATION.md`: `orchestration-create`, `worker-contract-add`, `orchestration-approve`, `orchestration-activate`, `worker-result-submit`, `orchestration-reconcile`, `orchestration-integrate`, and `orchestration-complete`.
