# Installation, Update, Uninstall and Rollback

## Clean installation

Use `tools/cpt_dist.py install`. Core works without external services, semantic memory, observability backends or remote databases.

## Migration installation

Use `tools/cpt_migrate.py plan` followed by explicit `apply`. Never skip plan review in a production repository.

## Update

The distribution updater replaces managed tooling while preserving mutable runtime and Product Knowledge. It stops on managed-file conflicts unless the user explicitly requests a forced, backed-up update.

## Uninstall

Uninstall removes only managed framework assets and blocks while tasks, workers, orchestrations or dirty worktrees are active.

## Rollback

Migration rollback is receipt-driven and external-backup-backed. It is separate from uninstall because it must restore the exact pre-migration state rather than simply remove 4.0.
