# Runtime State Model

## Canonical ownership

| File | Owns |
|---|---|
| `.cpt/runtime.yaml` | Stable runtime configuration and paths |
| `.cpt/current.yaml` | Current unit of work, lease, checkpoint, blockers, next operation |
| `.cpt/task-index.yaml` | Task ledger only |
| `.cpt/tasks/*.yaml` | Detailed standard task state |
| `.cpt/micro-changes/*.yaml` | Qualified micro change state |
| `.cpt/leases/*.yaml` | User-approved scope records |
| `.cpt/checkpoints/*.yaml` | Recovery snapshots |
| `.cpt/runtime-summary.md` | Generated human-readable projection |

## Single-current-unit invariant

At most one of these may be non-null:

- `current_task`
- `current_micro_change`

A lease may be active only for the current unit.

## Revisions

Every dynamic state mutation increments `state_revision`. The generated summary embeds the same revision in a comment. Revision equality proves projection freshness, not task correctness.

## Manual edits

Manual edits are permitted but must be followed by:

```bash
python scripts/cpt_runtime.py validate
python scripts/cpt_runtime.py render-summary
```
