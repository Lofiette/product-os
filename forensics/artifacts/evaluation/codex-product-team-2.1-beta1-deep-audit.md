# Codex Product Team 2.1 beta 1 — Deep Recheck Audit

Date: 2026-06-10

## Verdict

**PASS WITH FIXES BEFORE 2.1 beta 2.**

The archive is structurally sound and the main validators pass, but the deep audit found several issues that can affect real Codex behavior. The biggest one is skill discoverability for the new ticketed-memory skills.

## Basic inventory

| Item | Count |
|---|---:|
| Files | 386 |
| Role playbooks | 49 |
| Custom agents | 49 |
| Skills | 84 |
| Scenario tests | 28 |

## Built-in checks

### validate_kit.py

Exit code: `0`

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
```

### test-routing.py

Exit code: `0`

```text
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
```

### check-memory-integrity.mjs

Exit code: `0`

```text
MEMORY INTEGRITY PASSED
```

## Context-load size check

| Load set | Bytes | Rough tokens, chars/4 |
|---|---:|---:|
| AGENTS staged | 19,395 | ~4,848 |
| FIRST_PROMPT listed | 26,590 | ~6,647 |
| FIRST_PROMPT listed + active TKT | 28,491 | ~7,122 |

## P0 findings

### 1. Five new memory skills are missing YAML front matter

Affected skills:

```text
context-prune
context-snapshot
task-ledger
ticket-router
memory-integrity-check
```

Why it matters: most project skills use `name` and `description` front matter. These five skills are among the most important additions in 2.1 beta 1, but without front matter they are less likely to be surfaced and selected reliably by Codex as skills. This weakens the whole ticketed-memory upgrade.

Fix: add YAML front matter to each:

```yaml
---
name: context-prune
description: Compress bloated project memory into CURRENT.md, active ticket, compact CHRONICLE.md, and archive logs without losing blockers, decisions, approvals, evidence links, or next action.
---
```

Do the same for `context-snapshot`, `task-ledger`, `ticket-router`, and `memory-integrity-check`.

### 2. Runtime startup policy is inconsistent across files

`AGENTS.md` says the staged startup set is 7 files. `FIRST_PROMPT.md` asks to load 11 files. `CONTEXT_BUDGET_POLICY.md` lists 6 always-load files. `CURRENT.md` lists another “must load next” set.

This is not catastrophic, but it creates ambiguity about the real bootstrap load. The actual `FIRST_PROMPT.md` load set is ~26.6 KB before the active ticket, not ~19.4 KB.

Fix: define one canonical startup tier in `docs/RUNTIME_LOAD_POLICY.md` and make `AGENTS.md`, `FIRST_PROMPT.md`, `CURRENT.md`, and `CONTEXT_BUDGET_POLICY.md` point to it.

Recommended split:

- Tier 0 minimal: `AGENTS.md`, `CURRENT.md`, `TASK_INDEX.md`, `CHRONICLE.md`, `docs/BOOTSTRAP_INDEX.md`, `docs/LANGUAGE_POLICY.md`.
- Tier 0 optional, triggered: `docs/TEAM_CULTURE.md`, `docs/AGENT_NAMING_POLICY.md`, `docs/TICKETED_MEMORY.md`, `docs/CONTEXT_BUDGET_POLICY.md`.
- Tier 1: active ticket + tiny indexes + relevant role cards.

### 3. `docs/BOOTSTRAP_INDEX.md` has stale and malformed metadata

Problems:

```text
# BOOTSTRAP_INDEX.md — 2.0 beta 2 runtime index
Read this file at startup after `AGENTS.md`, `CURRENT.md / active ticket`, `CHRONICLE.md`, `QUESTION_TREE.md`, , `LANGUAGE_POLICY.md`, ...
```

Issues:
- stale version label: `2.0 beta 2`;
- malformed double comma;
- some doc references omit `docs/` prefix;
- it says to read “CURRENT.md / active ticket” too early, while ticket loading should happen after deciding the active operation.

Fix: rewrite the first paragraph as version-neutral and precise.

### 4. Built-in validators do not catch the most important new failure modes

The current validators pass, but they do not catch:

- missing skill front matter;
- startup-load contradictions;
- stale version labels outside release notes;
- malformed bootstrap references;
- whether `ROLE_TINY_INDEX.json` / `SKILL_TINY_INDEX.json` are actually smaller than mini/full;
- semantic scenario rules such as `must_not_implement`, `max_spawned_agents_default`, `must_not_implement_before_reference_spec`.

Fix: extend `validate_kit.py` and `test-routing.py` to cover these.

## P1 findings

### 5. `SKILL_TINY_INDEX.json` is not actually tiny

| File | Size |
|---|---:|
| `docs/SKILL_TINY_INDEX.json` | 14,951 bytes |
| `docs/SKILL_INDEX.json` | 15,225 bytes |

`SKILL_TINY_INDEX.json` is almost the same size as the full index. It helps naming consistency but not much context economy.

Fix: reduce `SKILL_TINY_INDEX.json` to `id`, `short_trigger`, `artifact`, `expensive: true/false`, `phase`.

### 6. `ROLE_TINY_INDEX.json` is still moderately heavy

`ROLE_TINY_INDEX.json` is 10,941 bytes. Acceptable, but for extra-high reasoning and frequent compression, a smaller `ROLE_MICRO_INDEX.json` could help.

### 7. Anticipation skills overlap

There are three related skills:

- `anticipation-radar`
- `expectation-anticipation`
- `proactive-proposal-review`

They are valid, but their boundaries are soft. Codex may call the wrong one or over-call all three.

Recommended boundary:

- `anticipation-radar`: detects hidden expectations and produces candidates.
- `proactive-proposal-review`: filters candidates.
- `expectation-anticipation`: can be deprecated or become an umbrella doc/skill alias.

### 8. Some runtime docs still carry old beta labels

Non-release files with stale labels:

```text
docs/BOOTSTRAP_INDEX.md
docs/ROLE_ROUTING_MATRIX.md
docs/SELF_AUDIT_REPORT.md
docs/SKILL_ROUTING_MATRIX.md
docs/TEAM_CULTURE.md
```

This is mostly cosmetic, but it weakens trust in the “2.1 beta 1” release and may make Codex cite old policies as current.

### 9. Release zip includes the audit report at top level

The uploaded zip contains:

```text
codex-product-team-2.1-beta1-audit.md
codex-product-team-2.1-beta1/
```

Not fatal, but for release packaging, keep the project archive clean and provide audit report as a separate download.

## P2 findings

### 10. Scenario tests still validate references, not behavior

`test-routing.py` checks that referenced roles/skills exist. It does not simulate whether a scenario would actually choose the required routing, obey max questions, block implementation, or enforce reference fidelity before implementation.

Fix: add a behavior-level scenario tester that reads each scenario and validates fields like:

- `max_questions`;
- `max_spawned_agents_default`;
- `must_not_implement_before_reference_spec`;
- `must_not_spawn_without_approval`;
- `forbidden_files_to_update_as_working_memory`.

### 11. CHRONICLE size threshold in validator is too generous

`check-memory-integrity.mjs` warns only above 5,000 chars. The policy says compact rescue summary. For this framework, I would warn at ~2,500 chars and block at ~5,000 chars.

## Practical simulations

### Simulation A — New multi-step UI task

Expected path:

1. Load Tier 0.
2. Route new work into a new ticket via `ticket-router` + `task-ledger`.
3. Load active ticket only.
4. If reference exists, run `reference-fidelity` before implementation.
5. If no DS exists, run `prototype-ui-kit`.
6. If DS exists or generated manifest appears, run `design-source-authority`.

Current risk: because `ticket-router` and `task-ledger` lack skill front matter, Codex may not select them reliably and may continue writing state into the active placeholder or into ad hoc summaries.

### Simulation B — Long-running work with context compression

Expected path:

1. Detect context pressure.
2. Run `context-snapshot`.
3. Run `context-prune`.
4. Keep `CURRENT.md` and `CHRONICLE.md` compact.
5. Move details to `chronicle/` and active ticket.

Current risk: the two critical skills also lack front matter. The validator checks files exist, but Codex may not treat them as first-class skills.

### Simulation C — Current-page UI review with spawned reviewers

Expected path:

1. Create `UI Review Packet`.
2. Apply bounded review.
3. Spawn at most 1–2 reviewers by approval.
4. Use failure policy if agents hang.

Current status: structurally good. The run-contract and failure policy are present. This part looks usable.

## Recommended beta 2 patch

P0:

1. Add YAML front matter to the five memory skills.
2. Align startup load policy across `AGENTS.md`, `FIRST_PROMPT.md`, `CURRENT.md`, `BOOTSTRAP_INDEX.md`, and `CONTEXT_BUDGET_POLICY.md`.
3. Clean stale/malformed `BOOTSTRAP_INDEX.md` header.
4. Extend validators to catch missing skill front matter and startup policy drift.

P1:

5. Make `SKILL_TINY_INDEX.json` truly tiny.
6. Clarify or merge anticipation-related skills.
7. Add behavior-level scenario validation.
8. Tighten `CHRONICLE.md` size warnings.

P2:

9. Clean stale beta labels from non-release docs.
10. Package audit report outside release zip.

## Bottom line

2.1 beta 1 is a solid architectural step. Ticketed memory is correctly introduced, `TASK.md` is safely demoted, and memory integrity passes. But the very skills that should operate the new memory model are not fully discoverable as Codex skills yet. Fixing that is the main release blocker before moving toward 2.1 beta 2.
