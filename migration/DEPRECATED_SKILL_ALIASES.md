# Deprecated 3.x skill aliases

The 3.x skill folders are not shipped as active skills in Alpha 3. Use `SKILL_MIGRATION.csv` to migrate prompts and documentation. Keeping aliases active would increase metadata pressure and create ambiguous implicit routing.

Notable explicit alias:

- `security-review` → `$cpt-threat-model`

No legacy alias silently invokes another skill. Migration is documented rather than hidden.
