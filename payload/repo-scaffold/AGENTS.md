<!-- CPT-OS KERNEL BEGIN -->
# CPT OS 4.0 Runtime Kernel

This marked block is managed by CPT OS. It is a compact loader, not the full methodology.

## Startup

Read only:

1. `.cpt/runtime.yaml`
2. `.cpt/current.yaml`
3. `.cpt/task-index.yaml`
4. `.cpt/runtime-summary.md`

If current state references a task, micro change, lease, or checkpoint, read only those referenced files. `current_task: null` is valid. `TKT-000` is optional and never assumed active.

## Route the request

- Use **Micro Change** only for obvious, local, reversible, low-risk changes with clear verification.
- Use **Standard Task** for meaningful implementation, discovery, design, API/data, architecture, or multi-file work.
- Escalate when scope, risk, uncertainty, or affected systems exceed the selected workflow.

Use `$cpt-runtime` when the CPT Core plugin is enabled. Without the plugin, use `.cpt/OPERATIONS.md` and `python .cpt/bin/cpt_runtime.py`.

## Authorization and context

Before standard-task writes, broad reads, expensive verification, dependency/public-contract changes, network use, or delegation, require a scoped authorization lease. The lease never overrides native Codex permissions or sandboxing.

Read only what can change the next decision. Do not load whole knowledge, expertise, archive, log, generated, or external-module trees at startup.

## Continuity

Create checkpoints before major handoffs, risky state changes, and compaction when possible. After suspected context loss, compare current state with the latest checkpoint and stop on mismatch.

## Stable invariants

- Do not invent facts, approvals, evidence, or worker results.
- Do not silently broaden scope.
- Do not treat build success as product, design, or behavioral success.
- Do not delete useful knowledge merely to meet a size target.
- Do not create branches, commits, staged changes, destructive Git operations, dependencies, migrations, or network access without explicit authorization.

## Completion

Complete work only when outcome, scope, verification, runtime validity, relevant durable knowledge, and compact recovery state are accounted for.
<!-- CPT-OS KERNEL END -->
