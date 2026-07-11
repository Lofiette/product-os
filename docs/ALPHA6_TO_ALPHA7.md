# Alpha 6 to Alpha 7

Alpha 7 preserves Runtime, Product Knowledge, Skills, Roles, Gates, Distribution, and Deterministic Enforcement while adding an optional Managed Worker Orchestration Plane.

## State migration

`tools/cpt_dist.py update`:

- upgrades mutable runtime state to Alpha 7;
- adds `current_orchestration` when missing;
- creates orchestration, contract, result, and worktree directories;
- preserves tasks, leases, knowledge, checkpoints, enforcement mode, and audit logs;
- keeps Alpha 6 checkpoint schemas readable where compatibility is required.

## Distribution change

Core plugin exposure defaults to personal scope in both local and team modes. Repository-vendored core remains available through explicit `--plugin-scope repo`.

The worker pack is separately installed and separately removed.

## Behavioral change

- Logical roles are not workers.
- Native worker return is not a successful result until structured evidence is submitted.
- Required quorum accepts only `success`.
- Multiple parallel writers require managed worktrees.
- Active orchestration blocks uninstall unless explicitly overridden.
