# Product OS Manager

Product OS Manager is the provider-neutral control plane for installation
inventory, adoption planning, transactions, rollback, and migration diagnosis.
Its core does not import Codex APIs. Host integrations provide bounded target
resolution and selector observations.

## Read-only detection

`tools/product_os_manager.py detect --project <path>` reads only fixed paths
derived from `InstallationContext`. It accepts v1 and v2 receipts without
upgrading either one. Receipt-provided managed and plugin paths are treated as
claims and are opened only after containment checks against the project or
isolated `CODEX_HOME`.

The report inventories receipt/version/source claims, runtime activity and the
latest checkpoint, managed-file state, packs and plugin materialization,
personal and repository marketplace manifests, selector evidence, and the
user registry. `state_hash` excludes `detected_at` and binds the consequential
observations.

Selector state is never inferred from a marketplace listing or receipt. Only an
in-process bounded adapter can provide an authoritative observation. JSON read
from `--selector-state` remains an untrusted preview even if it contains an
`authoritative` field.

## Deterministic dry-run planning

`tools/product_os_manager.py plan --project <path> --target <claims.json>
--selector-state <observation.json>` emits a plan to stdout. It performs no
writes unless the caller explicitly supplies `--output <path>`. Raw JSON cannot
promote itself to provider or selector authority, so this form remains blocked
for apply until a registered in-process adapter supplies the same evidence.

Target evidence binds provider, repository, marketplace identity, requested
ref, resolved commit, product version, package manifest digest, and every
required plugin selector/path/manifest digest. Adapter evidence uses a closed,
normalized field set. The only permitted materialization location is
`PRODUCT_OS_HOME/sources/<marketplace>/<commit>`, bound by a source marker. An
existing target is verified against every file in package `MANIFEST.json`,
rejects undeclared files and links, and validates plugin manifests plus declared
skills/hooks resources. An exact but not-yet-materialized target becomes a
prepare-phase action.

The stable `plan_hash` excludes `generated_at`. Apply must re-detect and compare
all receipt, runtime, managed-file, registry, marketplace, selector, and target
preconditions before the first mutation.

Plans expose two independent confirmation boundaries:

1. `apply` permits backup, isolated target materialization,
   a journaled receipt candidate, and preparation of non-active selectors. It
   does not refresh the active runtime.
2. `switch` permits activation only after the prepared-state hash is confirmed.

## Transaction and recovery contract

`prepare_adoption` and `switch_adoption` accept only registered in-process
adapters whose id, version, and capability fingerprint exactly match the
approved plan. The first phase creates and verifies an external backup,
materializes an immutable target, and exposes target selectors as disabled.
The second phase refreshes runtime-owned files, activates the complete target
selector set, atomically writes receipt v2, updates only the installation's
registry entry, and commits only after migration-doctor readback passes.

Every transition is hash-bound in
`PRODUCT_OS_HOME/transactions/<project-hash>/<transaction-id>/journal.json`.
Rollback performs a read-only ownership-envelope preflight before any restore.
Unknown resource, selector, or registry drift is never overwritten and moves
the journal to `manual_recovery_required`. Normal rollback restores only
project-owned resources and the current installation's registry/selector
projection, preserving unrelated user state. Forced recovery additionally
requires the exact observed-state hash and creates an emergency backup.

Locks are process-scoped OS locks. Their small files persist for diagnostics,
but a hard process exit releases ownership automatically. `recover_adoption`
reconciles orphaned prepare/switch journals conservatively; an ambiguous
partial runtime write remains manual rather than being guessed through.

Legacy selectors are retained until post-switch adapter readback and the
known-installation registry both prove they are unreferenced. An absent or
incomplete registry can be repaired for the current project, but never grants
deletion authority.

Normative schemas:

- `manager/schemas/detection-report-v1.schema.json`
- `manager/schemas/adoption-plan-v1.schema.json`
- `manager/schemas/backup-manifest-v1.schema.json`
- `manager/schemas/adoption-transaction-v1.schema.json`
