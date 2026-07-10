# Skill metadata budget

Codex initially sees skill names, descriptions, and paths under a bounded discovery budget. Alpha 3 therefore treats plugin selection as part of context engineering.

## Release budgets

- `cpt-core`: target maximum 2,000 estimated characters.
- Each optional domain pack: target maximum 3,000 estimated characters.
- Recommended task profiles: target maximum 7,000 estimated characters.
- All domain packs are **not** expected to be enabled simultaneously.

If every optional pack is enabled, Codex may shorten or omit entries from the initial skill list. This is not a reason to damage skill descriptions; it is a reason to enable only relevant packs.

Run:

```bash
python tools/measure_all_skill_metadata.py
```
