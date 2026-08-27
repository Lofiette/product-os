# Product OS installation registry

The user registry is a rebuildable index at
`~/.product-os/registry.json`. Set `PRODUCT_OS_HOME` to place all Manager
state under an isolated root.

The registry is not installation truth. Each project-owned
`.cpt/install.json` receipt remains authoritative. Rebuild accepts only
explicitly supplied v2 receipts; it does not scan a disk and does not invent an
installation ID for v1.

Writes use an OS-backed exclusive lock, compare-and-swap against the inspected
registry digest, fsync, and atomic replace. A live writer or stale plan fails
closed; an abandoned lock file does not remain owned after process death.
Unrelated installation entries are preserved by normal upsert and scoped
rollback operations.

Registry entries record the canonical project and receipt paths, semantic
receipt digest, product/runtime versions, source lineage, plugin names, and
verified selector identities. Missing, stale, or corrupt registry state never
authorizes deletion of a shared legacy source.

The normative schema is
`manager/schemas/installation-registry-v1.schema.json`.
