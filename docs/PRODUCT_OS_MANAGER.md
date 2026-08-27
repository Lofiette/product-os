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

The production trusted path is `plan-local-git`. It composes
`LocalGitTargetProvider` with the optional `CodexCliSelectorAdapter` in-process;
it never treats a JSON file as authority. All trusted commands require explicit
`--project`, `--user-home`, `--codex-home`, and `--product-os-home` values;
source resolution, prepare, switch, and recover additionally require
`--repository-root`. Doctor and rollback rely on the immutable materialized
target plus the hash-bound journal, so a disappeared source repository cannot
block diagnosis or restore. The process-active `CODEX_HOME` is rejected by
default. A future, separately authorized live migration must repeat its exact
path through `--confirmed-active-codex-home`; ordinary isolated acceptance does
not use that option.

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

`LocalGitTargetProvider` is the production offline source adapter. It accepts
only a registered local, non-bare repository and a constrained ref; it never
fetches, checks out, runs hooks, or reads payload bytes from the working tree.
The ref is resolved to a commit, every package file is streamed from the Git
object database and checked against `MANIFEST.json`, and symlink/submodule
entries are rejected. A dirty working tree is therefore irrelevant, while a
ref that moves after plan approval invalidates the evidence and requires a new
plan.

The stable `plan_hash` excludes `generated_at`. Apply must re-detect and compare
all receipt, runtime, managed-file, registry, marketplace, selector, and target
preconditions before the first mutation.

Plans expose two independent confirmation boundaries:

1. `apply` permits backup, isolated target materialization,
   a journaled receipt candidate, and preparation of non-active selectors. It
   does not refresh the active runtime.
2. `switch` permits activation only after the prepared-state hash is confirmed.

The trusted CLI mirrors those boundaries instead of adding another execution
engine:

```text
product_os_manager.py plan-local-git ... --output plan.json
product_os_manager.py prepare ... --plan plan.json --confirmed-plan-hash <hash>
product_os_manager.py switch ... --transaction-id <id> --confirmed-prepared-state-hash <hash>
product_os_manager.py doctor ... --transaction-id <id>
product_os_manager.py rollback ... --transaction-id <id>
product_os_manager.py recover ... --transaction-id <id>
product_os_manager.py transactions ...
```

`rollback --force` is reserved for an already diagnosed manual-recovery state
and still requires `--confirmed-current-state-hash`.

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
`transactions` exposes a read-only newest-first journal index, including every
unresolved transaction id, so a hard exit before CLI output does not make
recovery undiscoverable.

`run_migration_doctor` is a separate read-only post-migration API. It requires
a committed journal, quiescent transaction lock, hash-bound target evidence,
and the exact live selector adapter binding recorded by the transaction. It
then rechecks runtime,
backup, selectors, receipt lineage, plugin coverage, managed files, registry,
immutable target, and journal stability. It reports drift but never repairs it;
repair remains an explicit rollback or recovery operation.

## Optional Codex host adapters

The Manager core remains provider-neutral. `CodexCliSelectorAdapter` is an
optional bounded host adapter over the Codex plugin JSON CLI. Prepare registers
only the already materialized local marketplace; switch installs the complete
target selector set. A single OS lock serializes all Product OS mutations of an
explicit `CODEX_HOME`. The adapter binds its capability fingerprint to the Git
commit, closed package manifest, plugin manifest digests, target paths, and
legacy selector versions. It verifies the complete source inventory and Codex
source metadata around every host mutation. This proves a verified source plus
an observed selector; proof of the bytes inside Codex's private plugin cache is
left to isolated integration acceptance.

Legacy retirement is deliberately unsupported by the Codex adapter until the
user registry proves every cross-project reference. The transaction therefore
retains legacy selectors after a successful switch.

`CodexSessionLifecycleAdapter` is an optional post-commit observation. The
bundled hook records only hashes and timestamps for `SessionStart` and
`SessionEnd`; it never stores raw session ids, transcript paths, prompts, model
names, or project paths. Only `SessionStart(source=startup)` for the committed
transaction satisfies the new-session gate. Resume, clear, compact, and
SessionEnd-only evidence remain `pending`. Lifecycle status never changes the
provider-neutral doctor result, but `doctor --require-codex-lifecycle` returns a
non-zero acceptance result until both core and lifecycle are `PASS`.
For a non-default `PRODUCT_OS_HOME`, the Codex process that creates the new
session and the lifecycle-required doctor command must both inherit that exact
environment variable. The CLI rejects a lifecycle-required doctor run when
the variable does not match, instead of leaving the missing locator implicit.
On Windows, the bundled hook launcher discovers Python in this order:
PRODUCT_OS_PYTHON, the nearest project-local .runtime/python/python.exe, the
Python launcher, and finally a real Python executable on PATH (Windows Store
aliases are rejected). This avoids assuming that the py launcher is installed.
Both launch paths disable bytecode writes so trusted hooks cannot mutate the
Manager's hash-verified immutable source materialization.
The Windows hook command is deliberately quote-free and resolves PLUGIN_ROOT
inside PowerShell. This avoids the current Codex cmd.exe quoting failure while
remaining safe when the installed plugin path contains spaces.
Lifecycle evidence uses a bounded 64-session ring and one shared lock per
installation transaction.

Offline release readiness includes a dedicated Manager/adoption gate. Real
isolated Codex switching plus fresh-session delivery is a separate RC gate and
remains pending until the user-authorized acceptance run.

Legacy selectors are retained until post-switch adapter readback and the
known-installation registry both prove they are unreferenced. An absent or
incomplete registry can be repaired for the current project, but never grants
deletion authority.

Normative schemas:

- `manager/schemas/detection-report-v1.schema.json`
- `manager/schemas/adoption-plan-v1.schema.json`
- `manager/schemas/backup-manifest-v1.schema.json`
- `manager/schemas/adoption-transaction-v1.schema.json`
- `manager/schemas/migration-doctor-report-v1.schema.json`
- `manager/schemas/codex-lifecycle-event-v1.schema.json`
