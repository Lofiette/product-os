
# Changelog

## 4.0.0-alpha.6

- Added optional CPT Core lifecycle hooks for runtime validation, lease checks, compaction checkpoints, freshness, worker records, and audit events.
- Added `off`, `audit`, and `enforce` modes.
- Added enforcement, worker, and audit-event schemas.
- Added lease-aware `policy-check`, audit inspection, and worker status commands.
- Added optional conservative and strict command rules.
- Added permission-profile examples without automatic permission changes.
- Added safe fallback when hooks are disabled or untrusted.
- Preserved file-only runtime, Product Knowledge, skills, roles, and distribution split from Alpha 5.

Previous alpha changelogs are preserved under `archive/` and migration notes under `docs/`.
