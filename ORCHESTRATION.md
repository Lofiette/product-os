# Managed Worker Orchestration

Alpha 7 introduced the optional execution plane for bounded Codex subagents. Alpha 8 preserves it and evaluates its typed contracts, timeouts, quorum, recovery, and worktree boundaries through executable fixtures. Logical roles remain accountable lenses; workers are separate execution containers.

## Core model

```text
Role     professional accountability and decision ownership
Skill    reusable method
Gate     evidence required to accept a result
Worker   bounded native subagent session
Main thread final integrator and decision owner
```

CPT never creates one worker per role. The optional worker pack contains ten archetypes:

- `cpt_explorer`
- `cpt_researcher`
- `cpt_product_mapper`
- `cpt_design_reviewer`
- `cpt_implementer`
- `cpt_test_runner`
- `cpt_code_reviewer`
- `cpt_risk_reviewer`
- `cpt_knowledge_curator`
- `cpt_incident_investigator`

## Safe default

- Main-thread role lenses are the default.
- Delegation requires an active Standard Task, an active authorization lease, and an approved orchestration run.
- Read-only workers are preferred.
- A worker may not spawn nested subagents.
- One archetype may appear at most once in a run because native lifecycle events do not carry a CPT contract identifier.
- The main thread consolidates evidence and owns the final decision.

## Lifecycle

```text
orchestration-create
→ worker-contract-add
→ orchestration-approve
→ orchestration-activate
→ native worker start/stop or manual fallback
→ worker-result-submit
→ quorum
→ orchestration-integrate
→ orchestration-complete
```

A native `SubagentStop` means only that a worker returned. It does not satisfy quorum. The parent must submit a structured CPT result.

When hooks are unavailable, an approved contract may receive a manual structured result. This preserves a usable fallback but does not claim native lifecycle evidence.

## Quorum

Supported policies:

- `all_required`: every required worker must return `success`; optional failures do not block.
- `all`: every contract must return `success`.
- `n_of_m`: all required contracts plus at least `n` successful results.

`partial`, `failure`, `insufficient_evidence`, `cancelled`, `timed_out`, and `skipped` do not satisfy a required contract. Useful partial evidence remains available to the main thread.

## Cancellation and timeouts

Cancellation is cooperative. CPT records `cancel_requested`; the Codex host or parent session must stop the live worker. A contract-level cancellation does not cancel the whole run. Run-level cancellation requests cancellation for every unresolved contract.

Reconciliation applies configured timeouts and marks ambiguous reconnect state as `needs_reconcile` instead of guessing.

## Parallel writes

Multiple writable workers require `parallel_worktree` strategy.

CPT then:

1. creates one Git worktree per approved writable contract;
2. refuses a dirty main repository by default;
3. verifies managed branch/path ownership;
4. checks actual changed paths against contract `write_scope`;
5. checks worker-reported `touched_paths` against Git status;
6. returns a review-only integration plan;
7. never merges automatically.

Dirty worktrees require explicit review or `--discard` before removal.

## Compaction and recovery

Checkpoint state includes the active orchestration, contracts, results, worker records, and managed worktrees.

- Managed read-only workers may cross compaction and are reconciled afterward.
- Unmanaged workers and active write workers block compaction in enforcement mode.
- Post-compaction verification stops on integrity or pointer mismatch.

## CLI overview

```bash
python .cpt/bin/cpt_runtime.py orchestration-create ...
python .cpt/bin/cpt_runtime.py worker-contract-add ...
python .cpt/bin/cpt_runtime.py orchestration-approve --run ORC-001
python .cpt/bin/cpt_runtime.py orchestration-activate --run ORC-001
python .cpt/bin/cpt_runtime.py worker-result-submit ...
python .cpt/bin/cpt_runtime.py orchestration-status --run ORC-001
python .cpt/bin/cpt_runtime.py orchestration-reconcile --run ORC-001
python .cpt/bin/cpt_runtime.py orchestration-integrate --run ORC-001 --summary "..." --apply
python .cpt/bin/cpt_runtime.py orchestration-complete --run ORC-001
python .cpt/bin/cpt_runtime.py orchestration-validate
```

For writable workers:

```bash
python .cpt/bin/cpt_runtime.py worktree-create --contract ORC-001-W01
python .cpt/bin/cpt_runtime.py worktree-status --contract ORC-001-W01
python .cpt/bin/cpt_runtime.py worktree-plan --contract ORC-001-W01
python .cpt/bin/cpt_runtime.py worktree-remove --contract ORC-001-W01
```

## Honest boundary

Alpha 8 preserves deterministic validation of typed contracts, hook payload simulations, persistence, quorum, timeouts, cancellation records, worktree isolation, and recovery. The Evaluation Plane adds fixture-level orchestration cases, but it is still not live certification of every Codex client, native spawn ordering, cancellation delivery, reconnect behavior, or worker model-output quality.
