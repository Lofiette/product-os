# Codex Product Operating System 4.0 Alpha 7

## Audit report: Managed Worker Orchestration

**Version:** `4.0.0-alpha.7`  
**Phase:** Managed Worker Orchestration  
**Verdict:** **PASS for the Alpha 7 phase scope, with explicit live-Codex and host-control limitations**

## 1. Scope of this phase

Alpha 7 adds an optional managed execution plane on top of the Runtime Kernel, Product Knowledge lifecycle, canonical skills, logical roles, quality gates, distribution split, and deterministic enforcement delivered in Alpha 1–6.

Implemented concerns:

- ten executable worker archetypes instead of one custom agent per logical role;
- typed orchestration runs and bounded worker contracts;
- explicit approval and activation;
- native lifecycle binding through `SubagentStart` / `SubagentStop` hook payloads;
- structured worker results independent of raw native return events;
- required and optional contracts;
- `all_required`, `all`, and `n_of_m` quorum policies;
- cooperative cancellation and timeout reconciliation;
- managed Git worktrees for parallel writers;
- disjoint write-scope and actual changed-path checks;
- disk-backed orchestration, worker, result, and worktree state;
- compaction checkpoint integration and post-compaction reconciliation;
- separate optional worker-pack installation, status, and removal;
- active-runtime uninstall protection;
- deterministic orchestration policy fixtures and synthetic lifecycle integration.

Not in scope:

- live certification against real Codex subagent threads;
- forceful cancellation of a native worker by CPT itself;
- automatic merge or conflict resolution;
- unrestricted multi-level delegation;
- remote/tamper-evident orchestration storage;
- model-output quality grading;
- cross-client reconnect certification;
- Phase 8 executable prompt/tool-trace evaluation.

## 2. Architectural decisions

### 2.1 Roles are not workers

Alpha 7 preserves:

- **50 logical roles** as accountability and expert-decision lenses;
- **45 canonical skills** as reusable methods;
- **25 quality gates** as evidence contracts.

It adds only **10 worker archetypes** as optional execution containers:

1. `cpt_explorer`
2. `cpt_researcher`
3. `cpt_product_mapper`
4. `cpt_design_reviewer`
5. `cpt_implementer`
6. `cpt_test_runner`
7. `cpt_code_reviewer`
8. `cpt_risk_reviewer`
9. `cpt_knowledge_curator`
10. `cpt_incident_investigator`

The main thread remains the final integrator and decision owner. A worker receives bounded role lenses; it does not become the owner of the overall task.

### 2.2 Worker pack is optional

The worker pack is not installed with the core runtime. It is managed separately through:

```bash
python tools/cpt_dist.py workers-install --scope personal
python tools/cpt_dist.py workers-status --scope personal
python tools/cpt_dist.py workers-remove --scope personal
```

Personal scope is recommended for reuse across projects. Repository scope is explicit and intentionally creates project-local custom-agent files.

### 2.3 Main-thread execution is the safe default

Delegation is justified only when it improves independent evidence, parallel read-heavy work, specialized challenge, or safe isolation. A Standard Task, active authorization lease, approved orchestration, and bounded contracts are required.

### 2.4 One archetype per run

Native worker lifecycle events identify the custom-agent type but do not carry a CPT contract identifier. Alpha 7 therefore permits a worker archetype at most once in one orchestration run. This removes ambiguous contract binding.

## 3. Orchestration lifecycle

The supported lifecycle is:

```text
orchestration proposal
→ worker contracts
→ user approval
→ activation
→ native worker binding or manual fallback
→ structured results
→ quorum
→ main-thread integration
→ completion
```

A contract records:

- worker archetype;
- purpose;
- required or optional status;
- role lenses;
- canonical skills;
- task and lease pointers;
- read and write scope;
- permission mode;
- isolation mode;
- timeout;
- required output fields;
- stop conditions;
- fallback strategy.

A native `SubagentStop` event means that a worker returned. It does **not** by itself satisfy a contract. The parent must submit a typed CPT result with evidence and confidence.

When hooks are unavailable, an approved contract may receive a manual structured result. This preserves a usable fallback but does not claim native lifecycle evidence.

## 4. Quorum and result semantics

Supported quorum modes:

- `all_required`: every required contract must return `success`; optional non-success does not block;
- `all`: every contract must return `success`;
- `n_of_m`: every required contract plus at least `n` successful contracts.

Only `success` satisfies a required contract.

The following statuses preserve useful evidence when present but do not satisfy required quorum:

- `partial`;
- `failure`;
- `insufficient_evidence`;
- `cancelled`;
- `timed_out`;
- `skipped`.

Draft runs remain `proposed` while contracts are still being assembled. Quorum impossibility is evaluated as a blocking condition only after the contract set is approved.

## 5. Cancellation, timeout, and reconciliation

Cancellation is cooperative:

- CPT writes `cancel_requested` with reason and timestamp;
- the parent or Codex host must stop the live native worker;
- contract cancellation does not cancel the entire run;
- run cancellation requests cancellation for all unresolved contracts.

Reconciliation:

- applies contract timeouts;
- marks ambiguous reconnect state as `needs_reconcile` rather than guessing;
- preserves disk state across compaction or client reconnect;
- requires explicit resolution before completion.

## 6. Parallel write isolation

Multiple writable workers require the `parallel_worktree` strategy.

For each writable contract CPT:

1. rejects a dirty main repository by default;
2. creates a dedicated Git worktree and managed branch;
3. verifies that the worktree is registered by Git;
4. verifies branch, contract, and orchestration ownership;
5. verifies actual changed paths against contract `write_scope`;
6. verifies worker-reported `touched_paths` against Git status;
7. produces a review-only integration plan;
8. never merges automatically.

Tampered worktree records cannot redirect removal to the main repository, an unrelated worktree, or an arbitrary branch. Dirty worktrees require explicit review or `--discard` before removal.

## 7. Compaction and recovery

Checkpoint state includes:

- current runtime pointers;
- task index and active task;
- active lease and micro change;
- active orchestration;
- contracts and structured results;
- worker lifecycle records;
- managed worktrees;
- blockers and unfinished verification;
- next operation.

Compaction behavior:

- managed read-only workers may cross compaction and are reconciled afterward;
- unmanaged workers block compaction in enforcement mode;
- active writable workers block compaction in enforcement mode;
- post-compaction verification stops on integrity or pointer mismatch.

## 8. Distribution and installation

Default team-shared installation currently uses **11 project-local framework files**, below the 20-file target. Core plugin exposure is personal by default for both local and team modes; repository vendoring remains explicit.

Local mode remains Git-clean when Git is available. Repository-scoped worker-pack installation is explicit and therefore may create intentional project-local files.

Uninstall is blocked when CPT detects:

- an active task or micro change;
- an unfinished orchestration;
- a running, cancellation-requested, or reconcile-needed worker;
- an active or dirty managed worktree.

An explicit `--force-active-runtime` flag is required to override this guard. Personal worker packs are not removed with a single project because other repositories may use them.

## 9. Native Codex boundary

Worker TOML profiles, CPT contracts, and CPT leases do not replace native Codex controls. Native sandboxing, permission profiles, approvals, project trust, organization policy, and host lifecycle remain authoritative.

Recommended worker limits are supplied as an example, not silently merged:

```toml
[agents]
max_threads = 4
max_depth = 1
job_max_runtime_seconds = 900
interrupt_message = true
```

Workers are instructed not to spawn nested subagents.

## 10. Validation and evaluation results

### Isolated behavioral tests

- Distribution: **18 / 18**
- Skills: **5 / 5**
- Roles: **4 / 4**
- Product Knowledge: **13 / 13**
- Enforcement: **21 / 21**
- Orchestration: **24 / 24**
- **Total: 85 / 85**

### Static, policy, and proxy validation

- Distribution static validation: PASS
- Skill validation: PASS
- Role validation: PASS
- Knowledge asset validation: PASS
- Knowledge runtime validation: PASS
- Enforcement asset validation: PASS
- Orchestration asset validation: PASS
- Skill trigger proxy eval: **135 / 135**
- Role routing proxy eval: **164 / 164**
- Knowledge lifecycle eval: **11 / 11**
- Enforcement policy eval: **5 / 5**
- Orchestration policy eval: **34 / 34**

### Synthetic lifecycle integrations

- Enforcement integration: **13 / 13**
- Orchestration integration: **16 / 16**

The orchestration integration covers:

```text
local installation
→ Git-clean core runtime
→ optional repository worker pack
→ Standard Task
→ authorization lease
→ two required read-only workers
→ native start/stop hook simulation
→ checkpoint before compaction
→ post-compaction verification
→ structured results
→ required quorum
→ main-thread integration
→ orchestration completion
→ task completion
→ final checkpoint verification
→ doctor
```

### Package integrity

The final packaging process additionally requires:

- Python compilation;
- JavaScript syntax validation;
- manifest hash validation;
- ZIP integrity validation;
- validation and install/doctor smoke tests from a clean extracted archive.

## 11. Bugs caught during final hardening

Final regression testing caught and corrected several nontrivial issues:

1. an orchestration could become `satisfied` or `blocked` while its contract set was still being assembled;
2. `partial` results could incorrectly satisfy required quorum;
3. a local orchestration note outside the managed `AGENTS.md` block survived uninstall;
4. an old enforcement test referenced the removed `explorer` worker ID;
5. a brittle distribution test compared YAML quoting rather than semantic content;
6. the integration fixture checked Git cleanliness after intentionally vendoring the worker pack;
7. the checkpoint integration expected the wrong successful verification message;
8. worktree and worker-pack receipt records required stricter tamper validation.

## 12. Known limitations

1. Live Codex subagent sessions were unavailable in the build environment; hook lifecycle events are simulated deterministically.
2. CPT cannot forcibly terminate a native worker; cancellation delivery belongs to the parent/host.
3. One contract per archetype is required because native events do not carry CPT contract IDs.
4. Real reconnect and parallel-event ordering across Codex clients require live evaluation.
5. Worktree integration is review-only; CPT does not merge or resolve conflicts.
6. Shell/tool classification remains incomplete for arbitrary programs.
7. Local YAML/JSONL state is not tamper-evident remote storage.
8. Worker outputs are schema-checked but not yet graded for model quality.
9. Token, latency, and approval budgets are not yet enforced by an executable Evaluation Plane.
10. The optional worker pack must be installed and enabled before CPT can claim native worker lifecycle evidence.

## 13. Release recommendation

Alpha 7 is accepted as the baseline for the Managed Worker Orchestration phase.

Recommended use:

1. keep main-thread role lenses as default;
2. install the worker pack only when delegation is useful;
3. prefer read-only workers;
4. use low thread count and depth 1;
5. require scoped leases and bounded contracts;
6. inspect structured evidence before integration;
7. use managed worktrees for every parallel writer;
8. never treat synthetic integration as live-client certification.

## 14. Next phase

**Phase 8: Executable Evals and CI** should add:

- fixture repositories;
- real prompts and expected artifacts;
- captured tool traces;
- allowed/forbidden read and write assertions;
- approval-boundary checks;
- token, tool, latency, and approval budgets;
- timeout/reconnect/compaction stress cases;
- worker-output graders;
- cross-platform CI;
- live Codex certification where available.
