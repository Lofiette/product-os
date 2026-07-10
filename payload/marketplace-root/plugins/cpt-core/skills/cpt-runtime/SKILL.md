---
name: cpt-runtime
description: Use for CPT task lifecycle, micro changes, scoped authorization, checkpoints, completion, or recovery; not for domain judgment.
---

# CPT Runtime

## Use when

- A repository contains `.cpt/runtime.yaml`.
- Work must start, change scope, complete, checkpoint, or recover after context loss.

## Do not use when

- The repository has no CPT runtime.
- The request only needs domain analysis and runtime state is already valid.

## Required inputs

- `.cpt/runtime.yaml`, `.cpt/current.yaml`, `.cpt/task-index.yaml`, `.cpt/runtime-summary.md`.
- User intent and any existing task, micro-change, lease, or checkpoint identifier.

## Method

1. Validate runtime pointers before making lifecycle decisions.
2. Classify the request as Micro Change, Standard Task, or clarification-only.
3. For a Micro Change, record the smallest reversible scope and verification; escalate when impact becomes systemic.
4. For a Standard Task, create or activate a task and keep current/task-index pointers consistent.
5. Before writes, record a scoped authorization lease covering read, write, verification, delegation, forbidden operations, and expiry.
6. Create a checkpoint before compaction, risky handoff, or runtime mutation.
7. Complete only after outcome, verification, limitations, and next state are recorded.
8. On recovery, verify checkpoint integrity and stop on mismatch rather than guessing.

## Output contract

Produce a compact artifact containing:

- `Selected workflow and active runtime unit.`
- `Approved and forbidden scope.`
- `Authorization and checkpoint state.`
- `Verification status, blockers, and next operation.`

## Evidence standard

- Runtime CLI output is authoritative for pointer and schema validity.
- User approval is authoritative for lease scope.
- Do not infer a completed verification from an intended command.

## Stop and escalate

- Runtime pointers or checkpoint hashes are invalid.
- Scope expands beyond the active lease.
- A Micro Change reveals systemic or risky impact.
- Required verification cannot run or is inconclusive.

## Failure modes to avoid

- Using a full ticket for a trivial local edit.
- Continuing after compaction without checking disk state.
- Treating the lease as a security sandbox rather than an authorization record.
