# Installer Contract

The installer owns only:

- marked CPT kernel block in `AGENTS.md`;
- files listed in `.cpt/install.json`;
- CPT marketplace entries;
- copied CPT plugin directories.

It must not:

- edit application source;
- stage or commit files;
- overwrite modified managed tooling without conflict handling;
- remove personal plugins during project uninstall by default;
- infer ownership of unmarked files.

Mutable runtime state is initialized once and preserved during updates.
