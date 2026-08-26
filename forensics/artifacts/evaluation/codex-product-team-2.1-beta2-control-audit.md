# Codex Product Team 2.1 beta 2 — Control Audit

## Verdict

**PASS WITH FIXES BEFORE 2.1 beta 3 / RC.**

The archive is structurally healthy and the new ticketed-memory architecture is in place. Built-in validation passes, role/skill/agent links are consistent, and `TASK.md` is correctly reduced to a compatibility pointer. However, the control audit found a few issues the current validators do not fully protect against, including one real executable-script bug.

## Checks performed

- Zip integrity: PASS.
- Built-in `python3 scripts/validate_kit.py`: PASS.
- Built-in `python3 scripts/test-routing.py`: PASS.
- Built-in `node scripts/check-memory-integrity.mjs`: PASS.
- Node syntax checks for UI/DS scripts: PASS.
- Role consistency: 49 roles, 49 playbooks, 49 role cards, 49 TOML agents.
- Skill consistency: 84 skills, 84 `SKILL.md` files, 84 valid YAML front matter blocks.
- Scenario count: 28 scenarios.

## Runtime context size

### Tier 0 always-load set

| File | Characters |
|---|---:|
| `AGENTS.md` | 9,299 |
| `CURRENT.md` | 2,174 |
| `TASK_INDEX.md` | 701 |
| `CHRONICLE.md` | 1,254 |
| `docs/BOOTSTRAP_INDEX.md` | 3,174 |
| `docs/LANGUAGE_POLICY.md` | 435 |
| **Total** | **17,037** |

Approximate rough token estimate: **~4,259 tokens**. This is acceptable for the current architecture.

### Common Tier 1 files

| File | Characters |
|---|---:|
| `tasks/TKT-000-intake.md` | 1,899 |
| `docs/ROLE_TINY_INDEX.json` | 7,945 |
| `docs/SKILL_TINY_INDEX.json` | 10,206 |
| `docs/ROLE_MINI_INDEX.json` | 23,052 |
| `docs/SKILL_INDEX.json` | 15,226 |
| `docs/QUESTION_TREE.md` | 1,437 |

## Findings

### P0 — `scripts/validate_kit.py` is broken when executed directly

`validate_kit.py` has an extra leading backslash before the shebang:

```text
#!/usr/bin/env python3
```

Running it via `python3 scripts/validate_kit.py` works, but running it as an executable fails and the shell tries to interpret Python code as shell commands. Since the file is marked executable, this is a real release-quality bug.

**Fix:** remove the leading backslash and add a validator check that all executable scripts start with a valid shebang at byte 0.

### P1 — executable permissions are inconsistent for scripts

Current script modes:

| Script | Mode | First line |
|---|---:|---|
| `scripts/check-component-imports.mjs` | `0o666` | `#!/usr/bin/env node` |
| `scripts/check-design-source-authority.mjs` | `0o644` | `#!/usr/bin/env node` |
| `scripts/check-memory-integrity.mjs` | `0o755` | `#!/usr/bin/env node` |
| `scripts/find-raw-ui-values.mjs` | `0o666` | `#!/usr/bin/env node` |
| `scripts/test-routing.py` | `0o755` | `#!/usr/bin/env python3` |
| `scripts/validate_kit.py` | `0o755` | `\` |


The Node scripts have shebangs but are not executable. This is not fatal because docs call them through `node ...`, but the package is cleaner if either all script permissions match their shebangs or docs consistently say they must be run through `node` / `python3`.

**Fix:** either chmod executable for `.mjs` scripts or remove reliance on direct execution entirely. Keep README commands explicit.

### P1 — `check-component-imports.mjs` is still too soft for governed DS work

The script now performs real checks, but it treats native primitive usage as `warning`, and `--fail-on-violation` ignores warnings. In a governed design-system mode, this can let a custom `<button>` / `<input>` implementation pass even when a DS component exists.

It also may warn inside the DS component implementation itself, because native primitive detection does not currently exempt allowed DS source files.

**Fix:** add a strict mode, for example:

```text
--strict-ds
--fail-on-warning
```

And classify native primitives outside allowed DS component source files as violations in `documented_ds` / `governed_ds` mode.

### P1 — `SKILL_TINY_INDEX.json` is not truly tiny

`SKILL_TINY_INDEX.json` is **10.2 KB**, while full `SKILL_INDEX.json` is **15.2 KB**. That is smaller, but not “tiny” enough to fully support the context-economy goal.

**Fix:** reduce it to a compact routing map with only:

```json
{
  "id": "reference-fidelity",
  "trigger": "visual reference / screenshot / good-bad example",
  "artifact": "Reference Fidelity Spec",
  "phase": "before UI implementation"
}
```

No long descriptions, no prose, no dense explanation.

### P1 — old release notes and self-audit docs still live in `docs/`

The runtime policy says release notes and self-audit reports are reference/build-time only. That is correct. But they still live in the root `docs/` folder, including stale 2.0 beta labels.

This is not a direct runtime failure, but it creates accidental retrieval risk when Codex searches broadly.

**Fix:** move old release notes and self-audit reports into:

```text
archive/release-notes/
archive/audits/
```

Keep only the current release note or a short `docs/RELEASE_INDEX.md` in `docs/`.

### P2 — many non-critical skills still share generic workflow scaffolding

44 skills still include a generic process pattern like “Confirm this skill is needed / Load only relevant files/docs / Separate evidence...”. This is acceptable for less-used skills, but the most important design/runtime skills should stay concrete and artifact-driven.

Critical UI/runtime skills are already stronger than the generic ones, so this is not blocking. But before release candidate, prioritize deepening skills used in the most common real work:

- `repo-recon`
- `design-recon`
- `ui-review-packet`
- `current-page-ui-review`
- `design-system-compliance`
- `reference-fidelity`
- `screenshot-reference-comparison`
- `visual-qa-loop`
- `context-prune`
- `ticket-router`

### P2 — scenario tests are improved but still not fully behavioral

`test-routing.py` now validates some behavior fields, which is good. It still does not fully simulate routing behavior for fields like `max_roles`, `max_questions`, `must_not_load`, or `forbidden_spawn`.

**Fix:** add a small routing simulator or scenario linter that checks expected behaviors more deeply:

- Tiny tasks cannot include spawned agents.
- Reference-driven UI tasks require `reference-fidelity` before implementation.
- Production web/service tasks require phased orchestration.
- Ticketed-memory tasks must not update `TASK.md` as working memory.
- Current-page UI review must create a UI Review Packet before spawned review.

## What is good

- Ticketed memory architecture is correctly installed.
- `TASK.md` is now a short compatibility shim, not working memory.
- `CURRENT.md`, `TASK_INDEX.md`, active ticket, and compact `CHRONICLE.md` are coherent.
- All new memory skills have valid YAML front matter.
- Startup policy is now mostly consistent and significantly cleaner than beta 1.
- Agent naming policy is present and referenced.
- Role IDs are consistent across `TEAM.md`, `ROLE_INDEX.json`, playbooks, role cards, and TOML agents.
- UI quality/runtime docs from beta 4 are still present.

## Recommended beta 3 patch

### Must fix

1. Remove the leading backslash from `scripts/validate_kit.py`.
2. Add shebang/exec validation to `validate_kit.py`.
3. Strengthen `check-component-imports.mjs` strict DS behavior.

### Should fix

4. Make `SKILL_TINY_INDEX.json` genuinely tiny.
5. Move old release notes / self-audit docs into archive.
6. Add stricter scenario-behavior tests.

### Nice

7. Normalize script permissions or document execution mode explicitly.
8. Continue converting generic skills into artifact-specific workflows where they affect common real tasks.

## Final note

2.1 beta 2 is not broken. It is a solid context-economy upgrade. The most important issue is the broken executable validator shebang, because validation tooling should be boring, direct, and impossible to misfire. After that, the next quality leap is to tighten the DS scanner and reduce the skill tiny index.
