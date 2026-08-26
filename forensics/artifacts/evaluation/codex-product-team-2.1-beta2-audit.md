# Codex Product Team 2.1 beta 2 — Audit Report

## Verdict

PASS.

Beta 2 applies the beta 1 deep-audit fixes focused on ticketed memory, context economy, skill discoverability, startup-policy consistency, and stronger validation.

## Validation results

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

## P0 fixes applied

### 1. Memory skills now have Codex skill front matter

Added YAML front matter to:

- `context-prune`
- `context-snapshot`
- `task-ledger`
- `ticket-router`
- `memory-integrity-check`

This improves discoverability and makes these memory-runtime workflows behave like first-class Codex skills rather than plain markdown files.

### 2. Startup load policy synchronized

Canonical Tier 0 startup set is now consistent across runtime docs:

```text
AGENTS.md
CURRENT.md
TASK_INDEX.md
CHRONICLE.md
docs/BOOTSTRAP_INDEX.md
docs/LANGUAGE_POLICY.md
```

`docs/QUESTION_TREE.md` is no longer a Tier 0 default. It is loaded only when structured intake is needed.

### 3. Bootstrap cleaned

`docs/BOOTSTRAP_INDEX.md` was rewritten:

- removed stale `2.0 beta 2` label;
- removed ambiguous `CURRENT.md / active ticket` wording;
- removed broken punctuation;
- clarified runtime flow and quick triggers;
- reinforced `TASK.md` shim rule.

### 4. Validators strengthened

`validate_kit.py` now checks:

- every skill has YAML front matter;
- front matter `name` matches folder ID;
- front matter `description` is meaningful;
- startup Tier 0 drift across core docs;
- `QUESTION_TREE.md` is not loaded in Tier 0;
- stale bootstrap/runtime labels;
- tiny-index bloat;
- scenario behavior consistency.

`test-routing.py` now checks behavior fields, not only role/skill existence.

### 5. Tiny indexes compacted

Runtime routing starts from tiny indexes:

| File | Size |
|---|---:|
| `docs/ROLE_TINY_INDEX.json` | 7,945 bytes |
| `docs/ROLE_MINI_INDEX.json` | 23,052 bytes |
| `docs/SKILL_TINY_INDEX.json` | 10,206 bytes |
| `docs/SKILL_INDEX.json` | 15,226 bytes |

The skill tiny index is now meaningfully smaller than the full skill index and is suitable for first-pass routing.

## Runtime context check

Approximate Tier 0 startup files:

| File | Size |
|---|---:|
| `AGENTS.md` | 9,311 chars |
| `CURRENT.md` | 2,176 chars |
| `TASK_INDEX.md` | 703 chars |
| `CHRONICLE.md` | 1,256 chars |
| `docs/BOOTSTRAP_INDEX.md` | 3,200 chars |
| `docs/LANGUAGE_POLICY.md` | 435 chars |
| **Total** | **17,081 chars** |

This is below the previous beta 1 reported startup set and keeps `QUESTION_TREE.md`, culture docs, naming policy, and memory docs conditional rather than always-loaded.

## TASK.md status

`TASK.md` remains only as a deprecated compatibility pointer. It is not working memory.

Working memory is:

```text
CURRENT.md
TASK_INDEX.md
tasks/TKT-*.md
CHRONICLE.md as compact rescue summary
context/packets/* for evidence
context/snapshots/* for checkpoints
```

## Remaining watch-outs

No blocking issues found in this pass. Recommended next real-world checks:

1. Run a long UI/design task and verify Codex keeps `CURRENT.md` and active ticket compact.
2. Confirm Codex calls `ticket-router` / `task-ledger` during new work intake.
3. Confirm `context-prune` and `context-snapshot` are suggested when context compression becomes frequent.
4. Watch whether `SKILL_TINY_INDEX.json` is enough for first-pass routing or needs further compression.

## Summary

2.1 beta 2 fixes the beta 1 audit issues without expanding the framework. The main improvement is reliability of the ticketed-memory runtime: memory skills are now real skills, startup policy is canonical, bootstrap is clean, and validators catch the previously invisible drift.
