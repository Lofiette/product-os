# Plugin Metadata Budget

Codex initially discovers skills from lightweight metadata before loading full `SKILL.md` content. The distribution tools estimate the active discovery surface as:

```text
skill name + description + plugin-relative skill path
```

Use:

```bash
python tools/measure_metadata_budget.py payload/marketplace-root/plugins/cpt-core
```

The official initial discovery budget is context-sensitive and may be limited. Alpha 2 keeps core to one precise skill and reports combined pack metadata before expertise migration.
