# Changelog

## 4.0.0-alpha.4 — Role Expertise and Routing Overhaul

- Preserved and rewrote all 50 logical roles from 3.0.
- Added explicit decision rights, evidence obligations, artifacts, canonical skills, gates, handoffs, task types, and worker eligibility.
- Added 50 compact role lenses and 50 deep role-specific method references.
- Added 25 evidence-based quality gates and four-state verdict contracts.
- Added 14 machine-readable task routing profiles.
- Added role-to-skill and role-to-gate matrices plus a complete role migration registry.
- Added deterministic role trigger/routing proxy evaluations.
- Kept logical roles separate from custom agents and future worker archetypes.

## 4.0.0-alpha.4 — Skills Consolidation

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
