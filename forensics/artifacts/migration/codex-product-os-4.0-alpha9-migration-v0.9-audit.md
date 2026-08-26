# Codex Product Operating System 4.0 Alpha 9

## Migration and Release Integration Audit

**Version:** `4.0.0-alpha.9`  
**Phase:** Migration and Release Integration

## Executive verdict

Alpha 9 provides a conservative, reversible adoption path from 3.x-style embedded frameworks and local runtime overlays to the 4.0 operating system. The migration path is plan-first, backup-backed, non-destructive by default, and fully self-contained. External services are not required.

The release is suitable for Phase 10 RC trials. It is not yet a live-client-certified 4.0 release candidate.

## Delivered capabilities

### Migration assistant

`tools/cpt_migrate.py` provides:

- `inspect`: read-only inventory of the project and legacy environment;
- `plan`: read-only migration plan with conflicts, warnings, mappings, backup location and plan hash;
- `apply`: explicit installation, import, optional legacy retirement and validation;
- `verify`: post-migration integrity and runtime checks;
- `status`: migration and receipt state;
- `rollback`: external-backup-backed restoration of pre-migration managed paths;
- `platform-check`: Linux, macOS, Windows and WSL readiness diagnostics.

### Legacy inventory

The assistant detects:

- embedded 2.x/3.x role and skill libraries;
- `.codex-runtime` local overlays;
- legacy task and memory documents;
- Product Knowledge Markdown;
- custom/unmapped roles and skills;
- current 4.x runtimes;
- dirty Git state;
- framework-owned versus ambiguous `AGENTS.md`;
- presence of `AGENTS.override.md` without reading or interpreting it.

### Role and skill migration

The package reuses the audited registries from previous phases:

- all legacy skill IDs are compared with the 45 canonical skills;
- all 50 logical roles are compared with the retained/reworked role inventory;
- unmapped custom extensions are preserved and reported;
- compatibility aliases are not reactivated as discovery-budget-consuming skills;
- detected domain packs are selected from valid CPT pack manifests only; fixtures, examples and templates are excluded.

### Runtime-state preservation

Legacy runtime files are preserved as migration evidence. They are not silently activated as current 4.0 task state. This prevents stale or ambiguous task history from becoming authoritative after migration.

### Product Knowledge preservation

Legacy Product Knowledge Markdown is copied into a migration import area and marked `needs_review`. It is never silently promoted into validated 4.0 claims. The original sources remain available for bounded review and deliberate promotion.

### External backup and rollback

Before changing managed paths, Alpha 9 creates an external hash-described backup. By default it lives under user-level CPT state rather than inside the product repository.

Rollback:

- restores exact pre-migration managed paths;
- refuses when managed state changed after migration;
- supports an explicit forced mode that first creates an emergency safety copy;
- does not remove personal plugins automatically because they may be shared by multiple projects;
- leaves `AGENTS.override.md` untouched.

### Local and team modes

- **Local mode** supports ignored personal runtime overlays and remains Git-clean when the source environment is also local/ignored.
- **Team mode** performs an intentional repository migration without staging, committing or creating branches.

### Release documentation

The package includes:

- migration guide;
- installation, update, uninstall and rollback guide;
- platform support notes;
- troubleshooting guide;
- Alpha 9 release-integration notes;
- JSON Schemas for migration plans and receipts;
- machine-readable legacy detection rules;
- example plan;
- cross-platform GitHub Actions migration matrix.

## Safety invariants

1. `inspect` and `plan` are read-only.
2. `apply` is explicit.
3. The assistant never stages, commits or creates branches.
4. Core migration requires no external service.
5. `AGENTS.override.md` is outside the architecture contract and preserved byte-for-byte.
6. Ambiguous project-owned files are preserved rather than guessed.
7. Legacy claims are not automatically validated.
8. Backups live outside the repository by default.
9. Existing 4.x runtimes block ordinary migration and should use update workflows.
10. Rollback is receipt-driven and conflict-aware.

## Validation results

### Migration-specific behavior

```text
Migration unit tests: 7 / 7 PASS
Migration asset validation: PASS
Extracted-package migration tests: PASS
Extracted-package manifest hash validation: PASS
Product-specific term scan: PASS
Package hygiene scan: PASS
```

Covered cases include:

- read-only inspect and dry-run plan;
- local ignored overlay migration with clean Git;
- exact preservation of `AGENTS.override.md`;
- team migration followed by exact rollback;
- current-4.x conflict detection;
- rollback refusal after concurrent managed changes;
- forced rollback safety backup;
- platform diagnostics;
- domain-pack discovery excluding fixtures and examples.

### Regression protection

The existing Alpha 8 package validators and behavioral suite completed successfully during the Alpha 9 build. The migration layer was added without weakening Runtime, Skills, Roles, Product Knowledge, Enforcement, Orchestration or Evaluation Plane contracts.

### Extracted-package proof

The final ZIP was unpacked into a clean directory. From the extracted copy, the build executed:

- migration asset validation;
- migration behavior tests;
- manifest size/hash/inventory checks;
- local installation in an isolated Git repository;
- distribution doctor;
- runtime validation;
- Git cleanliness verification.

## Cross-platform status

The implementation is pure Python/pathlib plus Git and does not require symlinks or shell-specific scripts. A CI matrix is included for Linux, macOS and Windows, with explicit WSL diagnostics.

The current build environment did not execute native Windows or macOS hosts. Those live platform runs remain Phase 10 evidence.

## Honest limitations

1. Arbitrary custom 3.x extensions cannot be semantically mapped with certainty. They are preserved and reported.
2. Legacy Markdown is preserved as unverified evidence, not automatically converted into validated Product Knowledge.
3. Existing ambiguous `AGENTS.md` files require human review.
4. Project rollback does not automatically remove personal plugins shared by other repositories.
5. Concurrent application changes are outside the migration assistant’s managed rollback scope.
6. Cross-platform logic is implemented and CI-configured, but live platform certification belongs to Phase 10.
7. Live Codex client behavior, plugin enablement UX and organization-managed policy interactions remain RC-trial concerns.

## Recommendation

Freeze Alpha 9 as the Migration and Release Integration baseline, then proceed to Phase 10 RC Trials:

- clean installation;
- 3.x embedded migration;
- local-overlay migration;
- existing product;
- greenfield product;
- redesign/migration task;
- UI/design-system work;
- API-dependent UI;
- real worker orchestration;
- compaction/reconnect;
- Linux/macOS/Windows/WSL;
- token, latency, tool and approval measurements;
- final mega-audit.
