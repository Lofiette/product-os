# Changelog

## 4.0.0-alpha.7

- Added ten optional executable worker archetypes instead of one custom agent per logical role.
- Added typed orchestration runs, bounded worker contracts, structured results, quorum, cancellation, timeout, reconciliation, and main-thread integration.
- Added managed Git worktrees for parallel writable workers with dirty-base, branch/path, scope, and touched-path verification.
- Added orchestration state to checkpoints and compaction recovery.
- Added separate worker-pack installation, receipts, status, and safe removal.
- Made personal core plugin exposure the default for local and team installs; repository vendoring remains explicit.
- Added orchestration validators, policy evals, integration fixtures, and behavioral tests.
- Preserved Runtime, Product Knowledge, Skills, Roles, Gates, Distribution, and Deterministic Enforcement from Alpha 6.


## 4.0.0-alpha.6

- Added optional CPT Core lifecycle hooks for runtime validation, lease checks, compaction checkpoints, freshness, worker records, and audit events.
- Added `off`, `audit`, and `enforce` modes.
- Added enforcement, worker, and audit-event schemas.
- Added lease-aware `policy-check`, audit inspection, and worker status commands.
- Added optional conservative and strict command rules.
- Added permission-profile examples without automatic permission changes.
- Added safe fallback when hooks are disabled or untrusted.
- Preserved file-only runtime, Product Knowledge, skills, roles, and distribution split from Alpha 5.

Previous alpha changelogs are preserved under `archive/` and migration notes under `docs/`.
