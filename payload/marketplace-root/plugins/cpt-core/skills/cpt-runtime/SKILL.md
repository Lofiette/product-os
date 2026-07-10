---
name: cpt-runtime
description: Manage task routing, micro changes, scoped authorization, checkpoints, completion, and recovery in a repository containing .cpt/runtime.yaml. Use when starting or finishing meaningful work, deciding Micro Change versus Standard Task, authorizing a bounded operation, validating runtime state, or recovering after context loss.
---

# CPT Runtime

Operate the project runtime; do not replace product or engineering judgment.

## Trigger

Use when `.cpt/runtime.yaml` exists and the request needs task lifecycle, scope authorization, runtime validation, checkpointing, or recovery.

Do not use for ordinary repositories without CPT state.

## Procedure

1. Read `.cpt/runtime.yaml`, `.cpt/current.yaml`, `.cpt/task-index.yaml`, and `.cpt/runtime-summary.md` only.
2. Run `python .cpt/bin/cpt_runtime.py validate` if state may have changed manually or after recovery.
3. Choose the smallest safe workflow:
   - Micro Change for obvious, local, reversible, low-risk work with clear verification.
   - Standard Task for meaningful discovery, design, implementation, API/data, architecture, or multi-file work.
4. State the proposed read, write, verification, delegation, and forbidden scope.
5. For Standard Task implementation, require an active scoped lease and a compact Impact Map or equivalent scope artifact.
6. Create a checkpoint before major handoff, risky runtime change, or compaction when possible.
7. On context loss, verify against the latest checkpoint and stop on mismatch.
8. Complete the runtime record only after outcome, verification, and remaining limitations are recorded.

## Commands

Use `.cpt/OPERATIONS.md` and `python .cpt/bin/cpt_runtime.py --help` for exact commands.

## Output

Report:

- selected workflow;
- current or proposed task/unit;
- bounded scope;
- authorization state;
- verification state;
- checkpoint/recovery state;
- next operation.

## Failure modes

Stop and request clarification or a renewed lease when:

- scope expands;
- runtime pointers are invalid;
- checkpoint integrity fails;
- approval is missing;
- required verification cannot run;
- a Micro Change reveals systemic impact.
