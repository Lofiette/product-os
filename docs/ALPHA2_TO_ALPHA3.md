# Alpha 2 to Alpha 3

Alpha 2 established a safe distribution split: minimal repo scaffold, core plugin, optional packs, installer/update/uninstall, and metadata measurement.

Alpha 3 migrates the legacy skill surface without returning hundreds of files to each repository.

## Changed

- 95 legacy skills were inventoried and mapped.
- 45 canonical active skills replace aliases and procedural fragments.
- Five domain plugins are now implemented and independently installable.
- Every active skill has domain-specific method, output contract, evidence rules, stop conditions, failure modes, `agents/openai.yaml`, and trigger cases.
- Broad/high-cost workflows use explicit-only invocation.
- Skill registry, migration map, pack profiles, validation, trigger proxy eval, and metadata profile checks were added.

## Preserved

- Alpha 1 Runtime Kernel behavior.
- Alpha 2 local-ignored and team-shared installation modes.
- Safe update/uninstall ownership and runtime-state preservation.
- Core independence from domain packs.

## Intentionally not migrated yet

- 50 logical roles and role methodologies;
- role-to-skill and gate routing;
- worker archetypes and real delegation runtime;
- Product Knowledge schemas and freshness graph;
- hooks, rules, permissions, SQLite, MCP, and external adapters;
- executable Codex trace evals.

## Compatibility

Legacy skill names are not installed as aliases. Resolve them through `migration/SKILL_MIGRATION.json`. This avoids spending discovery metadata on compatibility shims and exposes ambiguous legacy references during migration.
