# AGENTS.md — Codex Product Operating System 4.0 Alpha 1

You are operating under the **CPT OS 4.0 Runtime Kernel**. This file is a loader and invariant set, not the full methodology.

## Startup

Read only:

1. `.cpt/runtime.yaml`
2. `.cpt/current.yaml`
3. `.cpt/task-index.yaml`
4. `.cpt/runtime-summary.md`

If `.cpt/current.yaml` points to an active task, micro change, authorization lease, or checkpoint, load only those referenced files.

`current_task: null` is a valid ready state. `TKT-000` is optional and is never assumed to be active merely because it exists.

Do not load the whole product knowledge base, role library, skill library, archives, logs, or external modules at startup.

## Route the request

Choose the smallest workflow that preserves quality:

- **Micro change**: obvious, local, reversible, low-risk, with an obvious verification path. Follow `docs/MICRO_CHANGE_PROTOCOL.md`.
- **Standard task**: meaningful implementation, discovery, design, API/data, architecture, or multi-file work. Follow `docs/NEW_TASK_PROTOCOL.md`.
- **Escalate** whenever scope, risk, uncertainty, or affected systems exceed the current workflow.

A direct user request may authorize an eligible micro change after a one-line scope declaration. It does not authorize scope expansion.

## Runtime state

Machine-readable state under `.cpt/` is canonical for task continuity:

- `runtime.yaml` — stable runtime configuration.
- `current.yaml` — current task/unit, blockers, lease, checkpoint, and next operation.
- `task-index.yaml` — compact task ledger.
- `tasks/*.yaml` — task records.
- `micro-changes/*.yaml` — micro change records.
- `leases/*.yaml` — scoped authorization leases.
- `checkpoints/*.yaml` — recovery snapshots.
- `runtime-summary.md` — generated human-readable rescue view; never a transcript.

Use `python scripts/cpt_runtime.py validate` before relying on state after manual edits or recovery.

## Authorization

Before project-file writes, broad reads, expensive verification, dependency changes, public API changes, network use, or delegation, require an active **scoped authorization lease** unless the Micro Change Protocol explicitly permits the operation.

A lease records user-approved scope. It never overrides native Codex sandbox, permission, approval, or organizational policy. Scope expansion invalidates the lease and requires renewal.

## Context economy

- Read only what can change the next decision.
- Prefer path/symbol discovery before opening many files.
- Prefer targeted sections and compact evidence packets over full dumps.
- Product knowledge and expertise packs are loaded by task area/type, never all at once.
- External services are optional; local files remain sufficient.
- Do not copy large tool output into runtime files.

## Checkpoint and recovery

Create a checkpoint:

- before compaction when possible;
- before a major phase handoff;
- before recovery or risky runtime-state changes;
- when unfinished verification, blockers, or delegated work must survive context loss.

After compaction or suspected context loss, compare runtime state with the latest checkpoint. Stop on mismatch; do not reconstruct critical scope or approvals from memory.

Alpha 1 provides a validated file-based checkpoint contract and explicit recovery commands. Automatic hook enforcement is a later phase.

## Execution transparency

Before non-trivial work, briefly state:

- workflow: micro or standard;
- current/proposed task;
- files or product knowledge to read;
- bounded discovery scope;
- writes and verification requested;
- expertise or workers proposed;
- authorization needed.

Before implementation of a standard task, produce an Impact Map or equivalent compact scope artifact.

## Stable safety invariants

- Do not invent missing product facts, approvals, evidence, or worker results.
- Do not treat build success as product, design, or behavioral success.
- Do not silently broaden read/write scope.
- Do not create branches, commits, staged changes, destructive Git operations, dependencies, migrations, or network access without explicit authorization.
- Do not use optional integrations as the only source of canonical state.
- Do not delete useful knowledge merely to meet a size target.

## Completion

A unit of work is complete only when:

- requested outcome is delivered;
- approved scope is respected;
- required verification is complete or explicitly reported as unavailable;
- runtime state is valid;
- affected durable knowledge is updated when relevant;
- `runtime-summary.md` reflects only the current recovery state.
