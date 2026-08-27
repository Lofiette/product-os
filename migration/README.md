# CPT Migration Assistant

This directory defines the conservative 3.x → 4.0 migration contract.

Principles:

- inspection and planning are read-only;
- apply is explicit;
- backup is external and hash-verified;
- rollback refuses concurrent managed changes by default;
- `AGENTS.override.md` is outside the contract and is preserved exactly;
- legacy Markdown is imported as `needs_review` evidence, never promoted silently;
- optional plugins, workers, and external services are never required for core migration.
- 4.1 adds four native canonical design methods recorded in `SKILL_MIGRATION.json:new_skills`; no fictional 3.x aliases are created.

Use `python tools/cpt_migrate.py --help`.
