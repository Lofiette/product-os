# Migration Troubleshooting

## Plan is blocked by existing 4.x

Use the normal updater. Migration is for 3.x or legacy overlays. Only use the explicit existing-4.x review option when recovering a partial migration.

## Existing AGENTS.md is ambiguous

The assistant preserves it. Review the plan and decide whether it is framework-owned. Never replace a product-owned instruction file automatically.

## Dirty worktree warning

Migration does not stage or commit existing changes. Prefer a clean repository so rollback and review remain understandable.

## Unmapped roles or skills

They are treated as custom extensions, preserved in the external backup and reported. They are not silently dropped or activated.

## Rollback refuses

Managed paths changed after migration. Review the changes. Forced rollback creates an emergency copy before restoring the pre-migration snapshot.

## Override behavior

`AGENTS.override.md` is intentionally unmanaged. Its behavior is neither preserved nor guaranteed by the framework beyond byte-for-byte non-modification.
