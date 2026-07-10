# File-Only Runtime Adapter

Alpha 1 uses YAML and Markdown as the complete runtime store. No database or external service is required.

## Durability techniques

- schema validation;
- cross-file invariants;
- atomic file replacement;
- a simple runtime lock;
- revisioned generated summary;
- checkpoint snapshots with SHA-256 digests;
- explicit reconciliation after manual edits.

## Degraded manual mode

When Python dependencies are unavailable:

1. Keep `current.yaml`, `task-index.yaml`, and the active unit consistent.
2. Never set both `current_task` and `current_micro_change`.
3. Keep lease ownership aligned with the active unit.
4. Create a manual checkpoint copy before risky changes.
5. Update `runtime-summary.md` from current state.
6. Run the validator as soon as tooling is restored.

SQLite will become the preferred exact registry later. File-only operation remains a supported fallback.
