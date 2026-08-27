# Migration from Product OS 4.0 to 4.1

Product OS 4.0.0 is the complete pre-redesign baseline. Product OS 4.1.0 introduces the full Product Designer redesign in one release: UI craft and critique, Interaction Intelligence, form and long-process design, professional data interfaces, Design Intelligence evaluation, and the provider-neutral Design Execution Plane.

## First determine what the `Product OS 4.0` folder is

Two different things can look like an installation:

1. **Source distribution**: contains `tools/cpt_dist.py`, `payload/`, `domain-packs/`, tests, and documentation.
2. **Installed project instance**: contains `.cpt/install.json` and usually a managed `AGENTS.md` block.

On Windows:

```powershell
Test-Path "C:\path\to\Product OS 4.0\.cpt\install.json"
```

- `False` means the folder is the Product OS source checkout or extracted release.
- `True` means the folder is also an installed project instance.

Do not overlay the 4.1 release blindly on top of a source folder. Source history belongs in Git. Project runtime state belongs in `.cpt/` and is updated by the distribution tool.

## Recommended one-time transition to Git

1. Keep the old extracted directory as a temporary backup.
2. Clone the Product OS Git repository into a stable directory named `Product OS`, without a version in the folder name.
3. Check out the intended release tag.
4. Install Python dependencies.
5. Update each project that has a `.cpt/install.json` receipt.

```powershell
git clone <REPOSITORY_URL> "Product OS"
Set-Location "Product OS"
git fetch --tags
git switch --detach v4.1.0
py -3 -m pip install -r requirements.txt
```

The repository tag carries the version. The directory name should remain stable across releases.

## Update an installed project

Run these commands from the Product OS 4.1 source repository, not from the target project:

```powershell
py -3 tools\cpt_dist.py status --project "C:\path\to\target-project"
py -3 tools\cpt_dist.py update --project "C:\path\to\target-project"
py -3 tools\cpt_dist.py doctor --project "C:\path\to\target-project"
```

The 4.1 updater:

- preserves mutable task, knowledge, enforcement, orchestration, and checkpoint state;
- replaces only Product OS-managed tooling files;
- refreshes `cpt-core`;
- refreshes every bundled domain pack recorded in `.cpt/install.json`, including `cpt-design-ui`;
- stops when a managed file was edited locally unless `--force` is explicitly used.

The domain-pack refresh is important. The original 4.0 updater refreshed the core plugin but could leave an already installed design pack on the old implementation.

This direct updater is the in-place local-distribution path. Converting an
existing local installation to the Git marketplace uses Product OS Manager
instead: create an authoritative `plan-local-git` plan from a registered local
Git repository, confirm its exact plan hash for `prepare`, then confirm the
prepared-state hash for `switch`. The Manager takes a verified backup, preserves
the old selectors during prepare, commits receipt/registry lineage only after
readback, and exposes explicit `doctor`, `recover`, and `rollback` commands.
If a process exits before it prints the transaction id, use the read-only
`transactions` command with the same explicit roots to discover unresolved
journals. Doctor and rollback do not require the original Git repository after
the commit-addressed target has been materialized.
All trusted commands require isolated roots explicitly; see
`PRODUCT_OS_MANAGER.md` for the contract. Do not use the active `CODEX_HOME`
during the isolated acceptance run.
Launch the isolated Codex process with `PRODUCT_OS_HOME` set to the same
explicit isolated Manager root so the fresh-session hook can locate its
hash-bound transaction journal.

## Update a source-only local marketplace

When Codex is connected to the local Product OS repository as a marketplace:

```powershell
codex plugin marketplace upgrade product-os
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
codex plugin list
```

For a local-path marketplace with uncommitted development changes, remove and re-add the marketplace only when Codex does not pick up the changed source. Start a new Codex thread after plugin reinstall or upgrade.

This Codex marketplace command applies only when Codex itself registered a
Git-backed marketplace that it can upgrade. A Product OS Manager installation
is intentionally pinned to
`PRODUCT_OS_HOME/sources/<marketplace>/<commit>`. Pushing a new commit or tag to
GitHub does not update that installation automatically. Plan the newer Git ref
with Product OS Manager, confirm `prepare`, then confirm `switch`; Manager keeps
the predecessor active until switch and can restore it on failure or rollback.

## What not to copy manually

Do not manually copy only the Product Designer role or only several `SKILL.md` files into 4.0. Product Designer 4.1 also changes:

- routing profiles and skill registry;
- domain-pack metadata;
- gates and role contracts;
- design-intelligence evals;
- execution adapters;
- validation and distribution metadata.

A partial copy creates an internally inconsistent package that may look operational while routing or evaluating the wrong behavior.

## Rollback

4.1 does not introduce an incompatible project-runtime schema change, so the safest rollback is release-based:

1. keep or restore the project backup created before the update;
2. check out `v4.0.0` in the Product OS repository;
3. reinstall the relevant plugins from that version;
4. start a new thread;
5. run `doctor` before resuming work.

For future major releases, use an explicit migration and rollback receipt instead of assuming a backward update is safe.
