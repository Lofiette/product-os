# Changelog

## 4.0.0-alpha.8

- Added an executable Evaluation Plane with 20 isolated fixture-repository cases.
- Added mandatory deterministic `offline-core` evaluations and optional live Codex backends.
- Added structured output, trace-policy, filesystem, runtime, resource-budget, and rubric graders.
- Added reviewed baseline comparison and four mutation checks.
- Added external fixture preparation/grading for the official Codex GitHub Action or other controlled runners.
- Added offline CI across Linux, macOS, Windows, Python 3.10, and Python 3.12.
- Added a manual read-only live Codex smoke workflow.
- Added explicit handling for missing CLI, non-zero live exits, reported-vs-observed file activity, and mixed PASS/SKIPPED suites.
- Added 13 Evaluation Plane behavioral tests and package-manifest exclusions for generated reports.
- Replaced bytecode-producing validator compilation with AST-based syntax checks.
- Preserved Runtime, Product Knowledge, Skills, Roles, Gates, Enforcement, Distribution, and Worker Orchestration from Alpha 1–7.

## 4.0.0-alpha.7

- Added ten optional executable worker archetypes instead of one custom agent per logical role.
- Added typed orchestration runs, bounded worker contracts, structured results, quorum, cancellation, timeout, reconciliation, and main-thread integration.
- Added managed Git worktrees for parallel writable workers with dirty-base, branch/path, scope, and touched-path verification.
- Added orchestration state to checkpoints and compaction recovery.
- Added separate worker-pack installation, receipts, status, and safe removal.

## 4.0.0-alpha.6

- Added optional CPT Core lifecycle hooks for runtime validation, lease checks, compaction checkpoints, freshness, worker records, and audit events.
- Added `off`, `audit`, and `enforce` modes.
- Added enforcement, worker, and audit-event schemas.
- Added lease-aware policy checks, audit inspection, and worker status commands.

Previous alpha changelogs are preserved under `archive/` and migration notes under `docs/`.
