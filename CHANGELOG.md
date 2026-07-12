# Changelog

## 4.0.0-beta.1

- Integrated the Runtime, Distribution, Expertise, Product Knowledge, Enforcement, Worker Orchestration, Evaluation, Migration, and Release planes into the first self-contained 4.0 Beta.
- Consolidated 95 legacy skills into 45 canonical skills across six focused plugins while preserving 95/95 migration mappings.
- Preserved 50 logical professional roles, added 25 evidence-based quality gates, and separated role lenses from ten optional executable worker archetypes.
- Added typed runtime state, Micro Change and Standard Task protocols, scoped authorization leases, checkpoints, compaction recovery, and local/team distribution modes.
- Added schema-driven Product Knowledge with claim lifecycle, provenance, freshness propagation, context packets, existing/greenfield/redesign modes, and sanitization policy.
- Added optional deterministic enforcement through lifecycle hooks, command classification, rules profiles, audit events, and a manual file-only fallback.
- Added managed worker orchestration with bounded contracts, structured results, quorum, timeout, cancellation records, reconciliation, and isolated Git worktrees for parallel writes.
- Added an executable Evaluation Plane with 21 isolated offline fixture cases, structured-output and trace graders, reviewed baselines, four mutation checks, and optional live Codex runners.
- Added backup-backed 2.x/3.x migration with dry-run planning, conflict reporting, rollback protection, and preservation of unverified legacy knowledge as evidence.
- Added a Release Plane with 33 trial tracks and nine gates, explicitly separating offline `BETA_READY` evidence from live/native `RC_READY` evidence.
- Replaced bytecode-producing syntax validation with AST-based checks so validators cannot pollute the immutable package manifest.
- Kept all external services optional; the core works with local files, Git, and Python only.

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

Previous alpha changelogs are preserved under `archive/`; migration and release notes live under `docs/`.
