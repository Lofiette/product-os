# Codex Product Operating System 4.0 — Alpha 2 Distribution Split

Alpha 2 packages the working Alpha 1 Runtime Kernel into a distribution model that does **not** require copying the whole future framework into every repository.

This increment provides:

- a repo scaffold with fewer than 20 framework files;
- a separately installable `cpt-core` Codex plugin;
- local-ignored and team-shared installation modes;
- safe installer, updater, doctor, and uninstaller commands;
- independent domain-pack exposure through Codex marketplaces;
- plugin metadata-budget measurement;
- rollback-oriented installation receipts;
- behavioral distribution tests.

It does **not** yet migrate the 50-role library, consolidate the 95 skills, add Product Knowledge, install hooks, or add external services.

## Quick start

```bash
python tools/cpt_dist.py install --project /path/to/repo --mode local
python tools/cpt_dist.py doctor --project /path/to/repo
```

Local mode installs an ignored `.cpt/` runtime and exposes `cpt-core` through the personal plugin marketplace. Team mode creates a shareable repo scaffold and, by default, a repo marketplace entry.

After a plugin is exposed, restart Codex and install or enable **CPT Core** from the plugin interface.

## Safety

- Application source files are never modified by installation.
- Existing tracked `AGENTS.md` is not modified in local mode unless explicitly authorized.
- Mutable runtime state is preserved on update.
- Uninstall backs up `.cpt/` state outside the project unless `--discard-state` is explicitly used.
- Personal plugins are not removed by project uninstall unless explicitly requested.

See `INSTALL.md`, `DISTRIBUTION_MODES.md`, and `UPDATE_AND_ROLLBACK.md`.
