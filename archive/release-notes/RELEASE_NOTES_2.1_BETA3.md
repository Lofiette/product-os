# Release Notes — 2.1 beta 3

## Focus

Targeted hardening for context economy, validator reliability, and strict design-system checks.

## Changes

- Fixed `scripts/validate_kit.py` executable shebang issue.
- Added executable/shebang checks to `validate_kit.py`.
- Added strict DS scanning behavior to `scripts/check-component-imports.mjs`:
  - `--strict-ds` turns native primitives into violations when DS equivalents exist outside DS source files.
  - `--fail-on-warning` can fail warning-only scans.
  - DS source roots are ignored for primitive findings to reduce false positives.
- Updated Tiny/Micro context policy: no role/skill indexes by default for obvious reversible work.
- Added `docs/SKILL_ROUTER_INDEX.json` as an optional ultra-light domain router before heavier indexes.
- Fixed `implementation-review` index descriptions to use active ticket rather than legacy `TASK` wording.
- Added production UI scenario requirements for `visual-qa-loop` and `component-contract-scan`.
- Strengthened `scripts/test-routing.py` behavior checks.
- Moved old release notes and self-audit docs into `archive/`.

## Validation

Expected:

```text
VALIDATION PASSED
ROUTING TEST PASSED
MEMORY INTEGRITY PASSED
```
