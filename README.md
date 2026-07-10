# Codex Product Operating System 4.0 — Alpha 1 Runtime Kernel

This package is the first executable slice of CPT OS 4.0. It implements the **Runtime Plane** only:

- a small root `AGENTS.md` loader;
- machine-readable file-based runtime state;
- a valid no-active-task state;
- optional `TKT-000` semantics;
- Standard Task and Micro Change lifecycles;
- scoped authorization leases;
- compact `RUNTIME_SUMMARY` projection;
- checkpoint creation, verification, and recovery;
- schema validation and cross-file integrity checks;
- a synthetic compaction-recovery test.

It intentionally does **not** include Product Knowledge, the 50-role expertise library, skills consolidation, worker orchestration, plugin distribution, hooks, external services, or migration tooling. Those belong to later phases.

## Quick check

```bash
python -m pip install -r requirements.txt
python scripts/cpt_runtime.py validate
python scripts/cpt_runtime.py status
python scripts/simulate_compaction_recovery.py
python -m unittest discover -s tests -v
```

## Core commands

```bash
# Show current state
python scripts/cpt_runtime.py status

# Create and activate a standard task
python scripts/cpt_runtime.py create-task \
  --title "Implement a bounded change" \
  --objective "Deliver the requested outcome with scoped discovery" \
  --task-type implementation \
  --complexity standard \
  --activate

# Create an authorization lease for the active task
python scripts/cpt_runtime.py lease-create \
  --task TKT-001 \
  --read 'src/feature/**' \
  --write 'src/feature/**' \
  --verify 'python -m unittest tests.test_feature' \
  --forbid dependency_change \
  --forbid network_access

# Save a checkpoint
python scripts/cpt_runtime.py checkpoint --reason "Before phase handoff"

# Verify state against the latest checkpoint
python scripts/cpt_runtime.py recover --checkpoint latest --verify-only

# Start a qualified micro change
python scripts/cpt_runtime.py micro-start \
  --title "Correct a local label" \
  --intent "Fix one visible label without changing behavior" \
  --target 'src/ui/example.tsx' \
  --verify 'python -m unittest tests.test_ui' \
  --confirm-eligible
```

## Canonical state

Human-readable runtime facts are stored under `.cpt/`. The Markdown summary is generated from YAML and should not be edited manually.

This alpha uses a **file-only** adapter. SQLite becomes the default exact registry in a later phase, while file-only operation remains a supported fallback.

## Safety note

Authorization leases in Alpha 1 are declarative and validated. They do not bypass or replace native Codex permissions, sandbox controls, rules, or approval prompts. Deterministic hook/rule enforcement is planned for the enforcement phase.

See `ALPHA1_LIMITATIONS.md` before production use.
