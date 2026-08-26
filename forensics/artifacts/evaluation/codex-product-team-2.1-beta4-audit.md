# Codex Product Team 2.1 beta 4 — Control Audit

## Verdict

PASS WITH TARGETED HARDENING.

This iteration keeps the 2.1 release focus on context economy and working reliability. No new roles were added. No heavy process layer was added.

## Validation

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

## Runtime context budget

Tier 0 startup set:

| File | Approx chars |
|---|---:|
| AGENTS.md | 10,600 |
| CURRENT.md | 2,174 |
| TASK_INDEX.md | 701 |
| CHRONICLE.md | 1,254 |
| docs/BOOTSTRAP_INDEX.md | 3,689 |
| docs/LANGUAGE_POLICY.md | 435 |
| **Total** | **18,853** |

This remains below the usual 32 KiB project-guidance ceiling, but the full skill ecosystem is large enough that implicit skill discovery should not be trusted for critical workflows.

## Key finding: skill ecosystem is large

The repo currently has:

```text
49 roles
84 skills
28 scenarios
```

Approximate initial native skill list budget if all skill names/descriptions/paths are considered:

```text
~16,022 chars
```

This can exceed Codex's initial skill-list budget. The correct fix is not to mutilate `SKILL_TINY_INDEX.json`; the safer fix is to rely on explicit staged routing and explicit skill selection for critical workflows.

## Changes applied

### 1. Added skill-discovery discipline

Added:

```text
docs/SKILL_DISCOVERY_POLICY.md
```

Updated:

```text
AGENTS.md
FIRST_PROMPT.md
docs/BOOTSTRAP_INDEX.md
docs/RUNTIME_LOAD_POLICY.md
scripts/validate_kit.py
```

The system now explicitly says: do not rely on implicit skill discovery for critical UI/design/runtime workflows. Use staged routing and exact skill IDs.

### 2. Added WSL diagnostic export

Added:

```text
docs/CODEX_DIAGNOSTIC_EXPORT_WSL.md
scripts/export-codex-diagnostics-wsl.sh
```

This creates a redaction-ready diagnostic pack for VS Code + WSL Codex runs.

### 3. Kept SKILL_TINY_INDEX intact

I did not aggressively compress `SKILL_TINY_INDEX.json`. It is already close to the minimum useful shape: `id + trigger`. Further cuts would reduce routing quality more than they would save context.

The policy is now:

```text
Tiny/Micro: do not load indexes by default.
Fast/Standard+: load tiny/router indexes when routing value justifies it.
Critical workflows: explicitly select exact skills.
```

### 4. Cleaned stale beta labels

Neutralized old Beta 1/Beta 2 notes in role cards and skills. Old release notes remain only in `archive/release-notes/`.

### 5. Validator coverage updated

`validate_kit.py` now checks:

- new diagnostic docs/scripts exist;
- diagnostic script has executable shebang;
- `SKILL_DISCOVERY_POLICY.md` is referenced by runtime files;
- existing role/skill/scenario/memory validations still pass.

## Practical simulation conclusions

### Tiny/Micro tasks

Should remain cheap:

```text
Tier 0 + active ticket / inline note.
No role/skill indexes by default.
No spawned subagents.
```

If Codex still loads indexes for obvious micro work, it violates beta 4 policy.

### UI/design tasks

Must not rely on implicit skill discovery. Critical skills must be explicitly selected by exact ID when triggers are present:

```text
reference-fidelity
design-source-authority
design-system-compliance
screenshot-reference-comparison
visual-qa-loop
taste-review
```

### Long sessions with frequent context compaction

Use:

```text
context-snapshot
context-prune
memory-integrity-check
```

If the problem persists, export a diagnostic pack from WSL:

```bash
bash scripts/export-codex-diagnostics-wsl.sh
```

## Remaining watch items for real testing

1. Does Codex actually follow the Tiny/Micro no-index policy?
2. Does it explicitly select critical UI/design skills rather than saying “I considered design quality”?
3. Does it keep `CHRONICLE.md` compact after long work?
4. Does it update active tickets instead of resurrecting `TASK.md`?
5. Does repeated context compaction correlate with huge assistant outputs, spawned subagents, large screenshots, or unnecessary file loading?

## Recommended next diagnostic pack

For one problematic Codex run, collect:

```text
~/.codex/history.jsonl
~/.codex/sessions/latest session files
project CURRENT.md / TASK_INDEX.md / CHRONICLE.md / active tasks/TKT-*.md
context/packets/* for the operation
diff.patch
reference and actual screenshots
Codex UI screenshots showing compaction/subagent behavior
```

Use the included WSL script where possible.
