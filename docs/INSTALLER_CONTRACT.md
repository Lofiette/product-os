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

Installation receipts use `cpt-install-receipt-v2` for new writes. The
installer remains able to read v1 receipts without mutating them; the first
approved install/update/pack/worker mutation upgrades the receipt in place.
Unknown v1 source lineage stays explicitly unknown rather than being inferred.

Receipt v2 adds a stable installation ID, runtime/product identity, source
lineage, plugin materialization evidence, applied migration summaries, and the
latest Manager transaction/backup references. Legacy top-level ownership fields
remain present so existing distribution commands keep their contract.
