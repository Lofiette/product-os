# Changelog

## 4.0.0-alpha.3 — Skills Consolidation

- Consolidated 95 legacy skills into 45 canonical skills with complete migration coverage.
- Implemented five independently installable domain plugins alongside `cpt-core`.
- Rewrote every active skill with trigger/non-trigger boundaries, required inputs, domain method, output contract, evidence standard, stop conditions, and failure modes.
- Added `agents/openai.yaml` and invocation policy for every skill.
- Added central skill registry, migration map, trigger proxy evals, pack profiles, and metadata-budget checks.
- Added bundled pack installation by name while preserving Alpha 2 installer/update/uninstall behavior.

## 4.0.0-alpha.2 — Distribution Split

- Packaged Runtime Kernel as a minimal repo scaffold and native `cpt-core` plugin.
- Added personal/repo marketplace exposure, local/team modes, safe lifecycle tooling, and independent pack boundaries.

## 4.0.0-alpha.1 — Runtime Kernel

- Added typed file runtime, Standard Task and Micro Change lifecycles, leases, checkpoints, and recovery.
