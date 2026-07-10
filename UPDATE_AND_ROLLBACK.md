# Update, Uninstall, And Rollback

## Update

```bash
python tools/cpt_dist.py update --project /path/to/repo
```

Update replaces only managed tooling files whose hashes still match the installation receipt. It preserves:

- current task state;
- task index;
- runtime summary;
- tasks, leases, micro changes, and checkpoints.

If a managed tooling file changed, update stops. `--force` creates a local backup before replacement.

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

## Rollback principle

Installation owns only files and marked blocks recorded in `.cpt/install.json`. It never assumes ownership of application source files or unmarked project documentation.
