# Alpha 2 Limitations

- Plugin exposure does not automatically enable a plugin in Codex.
- User restart or plugin UI action may be required after marketplace changes.
- Installer does not migrate a manually copied Alpha 1 runtime.
- Runtime still uses YAML files as exact state; SQLite is a later phase.
- Domain pack content is not migrated yet.
- Hooks, rules, permissions, Product Knowledge, roles, and worker orchestration are not installed.
- Existing tracked `AGENTS.md` stays untouched in local mode unless explicitly authorized.
- Uninstall can remove only marked or receipt-owned framework files; it never guesses ownership.
