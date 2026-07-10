# Skill migration

- `LEGACY_SKILL_INVENTORY.csv` records the 95 source skills, their size, boilerplate assessment, and target.
- `SKILL_MIGRATION.csv` and `.json` map every source ID exactly once.
- `DEPRECATED_SKILL_ALIASES.md` explains why aliases are not installed.

Resolve a name from the command line:

```bash
python tools/cpt_dist.py skill-resolve --name bounded-discovery
python tools/cpt_dist.py skill-resolve --name cpt-api-contract --json
```
