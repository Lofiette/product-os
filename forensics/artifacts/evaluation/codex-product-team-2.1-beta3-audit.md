# Codex Product Team 2.1 beta 3 — Control Audit

## Verdict

PASS.

This beta is a targeted hardening patch on top of 2.1 beta 2. It keeps the ticketed-memory architecture intact and focuses on context-economy behavior, validator reliability, and stricter design-system enforcement.

## Validation results

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
MEMORY INTEGRITY PASSED.
NODE_SYNTAX_PASS.
Zip integrity: PASS.
```

## Main fixes applied

### 1. Validator executable fix

Fixed `scripts/validate_kit.py` so the shebang is the first line. It now works both ways:

```bash
python scripts/validate_kit.py
./scripts/validate_kit.py
```

Added validator checks for executable shebang integrity.

### 2. Strict design-system scanner

Updated `scripts/check-component-imports.mjs` with:

```text
--strict-ds
--fail-on-warning
```

In `--strict-ds` mode, native primitives such as `<button>`, `<input>`, `<textarea>`, `<select>`, and `<dialog>` are treated as violations when equivalent DS components exist, except inside DS source files.

The validator now runs a synthetic strict-DS test to ensure this behavior does not regress.

### 3. Tiny/Micro context policy

Updated runtime docs so obvious Tiny/Micro tasks do not load role/skill indexes by default.

Canonical rule:

```text
Tiny/Micro obvious reversible work → Tier 0 + active ticket/inline note only.
Fast Lane → tiny indexes only if route is unclear.
Standard+ → optional SKILL_ROUTER_INDEX, then ROLE_TINY_INDEX and SKILL_TINY_INDEX.
```

This avoids spending context on indexes for trivial local edits.

### 4. Added ultra-light skill router

Added:

```text
docs/SKILL_ROUTER_INDEX.json
```

This is a small domain-level router used before heavier skill indexes when the task domain is unclear but the full skill index would be wasteful.

### 5. Skill index legacy wording fixed

Updated `implementation-review` descriptions in:

```text
docs/SKILL_INDEX.json
docs/SKILL_TINY_INDEX.json
```

They now reference the active ticket instead of legacy `TASK` wording.

### 6. Production UI route tightened

Updated `production_web_service_code_ds` scenario to require:

```text
visual-qa-loop
component-contract-scan
```

This better matches production UI work with a code-based design system.

### 7. Scenario behavior tests strengthened

Updated `scripts/test-routing.py` to check more behavior fields, including:

```text
must_not_spawn_without_approval
must_not_implement_before_reference_spec
must_block_self_validating_manifest
must_use_phased_orchestration
must_not_load
max_spawned_agents_default
Tiny/Micro no-index behavior
production UI required skills
```

### 8. Reference-only cleanup

Moved old release notes and self-audit material into:

```text
archive/release-notes/
archive/audits/
```

Kept only current `docs/RELEASE_NOTES_2.1_BETA3.md` in runtime-adjacent docs.

## Context economy check

Tier 0 remains compact:

```text
AGENTS.md
CURRENT.md
TASK_INDEX.md
CHRONICLE.md
docs/BOOTSTRAP_INDEX.md
docs/LANGUAGE_POLICY.md
```

The active work memory remains ticketed:

```text
CURRENT.md          — current control panel
TASK_INDEX.md       — compact ticket ledger
tasks/TKT-*.md      — active task details
CHRONICLE.md        — compact rescue summary
TASK.md             — deprecated compatibility pointer only
context/packets/*   — evidence packets
context/snapshots/* — checkpoints
chronicle/*         — long logs, not default runtime
archive/*           — historical/reference material, not default runtime
```

## Notes

`SKILL_TINY_INDEX.json` was not aggressively compressed further because it is already close to its safe minimum: skill ID plus a compact trigger. The better optimization is not loading it for obvious Tiny/Micro work, which beta 3 now enforces through runtime policy and scenario checks.

## Remaining watch items for real Codex runs

1. Does Codex actually skip indexes for obvious Tiny/Micro tasks?
2. Does strict DS mode catch native primitives in real projects without excessive false positives?
3. Does Codex use `SKILL_ROUTER_INDEX.json` only when it helps, not as another always-load file?
4. Do UI workflows still produce `BLOCKED` verdicts when reference fidelity, DS authority, or visual QA are missing?
