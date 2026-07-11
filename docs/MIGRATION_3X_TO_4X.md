# Migration Guide: 3.x to 4.0

## Objective

Move an embedded or local 3.x environment to the compact 4.0 runtime without losing task history, Product Knowledge, custom expertise, or rollback capability. Migration never stages or commits files.

## Recommended sequence

```bash
python tools/cpt_migrate.py platform-check --project /path/to/repo
python tools/cpt_migrate.py inspect --project /path/to/repo
python tools/cpt_migrate.py plan --project /path/to/repo --mode local --output /safe/path/plan.json
# Review plan, warnings, mappings and backup location.
python tools/cpt_migrate.py apply --plan /safe/path/plan.json --accept-warnings
python tools/cpt_migrate.py verify --project /path/to/repo
```

Use `--mode team` when the framework is intentionally versioned in the repository. Use local mode for ignored personal runtime overlays.

## What is migrated

- legacy task and runtime documents are preserved as unverified migration sources;
- legacy Product Knowledge Markdown is preserved under the migration import area and marked `needs_review`;
- legacy skill and role IDs are compared with the canonical migration registries;
- the 4.0 runtime is installed through the standard distribution tool;
- optional domain packs and worker pack are installed only when requested.

## What is not interpreted

`AGENTS.override.md` is never read, modified, validated or migrated. It is a native user-controlled override outside the framework contract.

## Legacy framework retirement

`--legacy-action archive` removes confidently identified legacy framework paths only after creating the external backup. Ambiguous project documentation is preserved and reported for review.

## Rollback

```bash
python tools/cpt_migrate.py rollback --project /path/to/repo
```

Rollback restores the managed project paths from the external backup. It refuses when those paths changed after migration unless `--force` is explicitly used; forced rollback first creates an emergency safety copy. Personal plugins are not removed automatically because they may be shared across projects.
