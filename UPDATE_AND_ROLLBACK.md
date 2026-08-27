# Update, uninstall, and rollback

## Update the Product OS source repository

Use release tags for stable work:

```bash
git fetch --tags
git switch --detach v4.1.0
python -m pip install -r requirements.txt
```

Do not copy a new release over an old extracted source folder. Git should own source history and make every change inspectable.

## Update an installed project

Run the update command from the **new Product OS source checkout**:

```bash
python tools/cpt_dist.py status --project /path/to/repo
python tools/cpt_dist.py update --project /path/to/repo
python tools/cpt_dist.py doctor --project /path/to/repo
```

Windows:

```powershell
.\scripts\product-os.ps1 -Action update -Project "C:\path\to\repo"
```

Update replaces only managed tooling files whose hashes still match the installation receipt. It preserves:

- current task state and task index;
- runtime summary;
- tasks, leases, micro changes, and checkpoints;
- Product Knowledge artifacts and generated views;
- enforcement mode and trust annotation;
- audit logs and worker lifecycle records;
- orchestrations and worktree records.

Product OS 4.1 also refreshes every bundled domain pack recorded in `.cpt/install.json`. This prevents `cpt-design-ui` or another installed pack from remaining on an older release while `cpt-core` moves forward.

If a managed tooling file changed, update stops. `--force` creates a backup before replacement:

```bash
python tools/cpt_dist.py update --project /path/to/repo --force
```

Review the reported conflict before forcing an update.

## Update Codex plugins

Git-backed marketplace:

```bash
codex plugin marketplace upgrade product-os
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
codex plugin list
```

Start a new thread after reinstalling or upgrading plugins. Updating plugins does not update project `.cpt/` state, so run `cpt_dist.py update` for each installed project as a separate step.

## Uninstall

```bash
python tools/cpt_dist.py uninstall --project /path/to/repo
```

Default behavior:

- backs up `.cpt/` outside the project;
- removes the managed `AGENTS.md` block;
- removes repo plugin exposure;
- removes repo runtime scaffold;
- preserves application files;
- leaves a personal plugin installed because another project may use it.

Remove the personal plugin only when intended:

```bash
python tools/cpt_dist.py uninstall --project . --remove-personal-plugin
```

Discard runtime state only explicitly:

```bash
python tools/cpt_dist.py uninstall --project . --discard-state
```

## Roll back 4.1 to 4.0

Source rollback:

```bash
git fetch --tags
git switch --detach v4.0.0
```

Then reinstall the plugins from the selected marketplace revision and start a new thread. Before rolling a project runtime backward, restore the pre-update backup or validate the downgrade in a disposable clone. Product OS 4.1 does not intentionally add an incompatible runtime schema, but backward updates are not treated as a universal substitute for a migration receipt.

For a Manager adoption transaction, use its journaled rollback instead of
copying files by hand:

```bash
python tools/product_os_manager.py transactions --project /path/to/repo --user-home /path/to/user --codex-home /path/to/user/.codex --product-os-home /path/to/product-os-home
python tools/product_os_manager.py rollback --project /path/to/repo --user-home /path/to/user --codex-home /path/to/user/.codex --product-os-home /path/to/product-os-home --transaction-id <transaction-id>
```

The normal backup for that transaction is stored at
`PRODUCT_OS_HOME/backups/<installation-id>/<transaction-id>/backup-manifest.json`.
Rollback verifies that hash-bound manifest and restores the prior receipt,
registry, runtime, and selectors. Use `rollback --force` only after `doctor` or
`recover` reports a manual-recovery state and provides the exact current-state
hash; see [Product OS Manager](docs/PRODUCT_OS_MANAGER.md#transaction-and-recovery-contract).

## Ownership boundary

Installation owns only files and marked blocks recorded in `.cpt/install.json`. It never assumes ownership of application source files, unmarked project documentation, or external/custom plugin packs.
