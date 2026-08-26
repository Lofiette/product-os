# Installation receipt v2

`.cpt/install.json` is the project-local source of truth for one Product OS
installation. The user-level Manager registry is rebuildable from receipts and
never replaces them.

## Compatibility

- v1 is accepted by read-only status, doctor, detection, and planning.
- read-only operations do not rewrite v1.
- the next approved mutating distribution or Manager operation writes v2.
- all v1 ownership fields remain in v2.
- missing v1 lineage is represented as `unknown` or `null`.

## Added evidence

- `installation_id`: stable UUID for registry identity;
- `product`: Product OS version and runtime schema;
- `source_lineage`: delivery type, repository, marketplace, release/ref,
  resolved commit, package manifest digest, and observation source;
- `installed_plugins`: selector identity plus observed payload and manifest;
- `applied_migrations`: durable summaries only;
- `manager`: last committed transaction and backup references.

An in-progress transaction journal is intentionally external to the project
receipt. The receipt records only durable installation state; a crash cannot
make an incomplete switch look committed.

The normative schema is
`manager/schemas/installation-receipt-v2.schema.json`.
