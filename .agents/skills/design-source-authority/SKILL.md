---
name: design-source-authority
description: Verify whether design-system/reference sources are authoritative, candidate, provisional, or self-generated. Prevents self-validating DS manifests and false compliance claims.
---

# design-source-authority

## Trigger

Use when UI/design work claims DS compliance, reference fidelity, prototype UI contract compliance, or uses a generated manifest/registry.

## Process

1. Read `docs/DESIGN_SOURCE_AUTHORITY.md` and `docs/MANIFEST_FREEZE_POLICY.md`.
2. List design sources and authority level.
3. Determine whether DS manifest existed before the task or was generated/changed during it.
4. Mark generated artifacts as `candidate`, `provisional`, or `self_generated`.
5. Block compliance claims that depend on self-generated artifacts.
6. Return PASS / PASS WITH WARNINGS / BLOCKED.

## Output

Use `.agents/templates/design-source-authority-report.md`.
