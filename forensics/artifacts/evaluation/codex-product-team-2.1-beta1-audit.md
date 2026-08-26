# Codex Product Team 2.1 beta 1 — Build & Integrity Audit

## Verdict

PASS.

This build is based on the 2.0 beta 4 release line and introduces the Ticketed Memory & Context Economy architecture.

## Build summary

- Roles: 49
- Skills: 84
- Scenarios: 28
- New memory model: enabled
- `TASK.md`: deprecated compatibility pointer only
- `CURRENT.md`: active runtime state
- `TASK_INDEX.md`: ticket ledger
- Active ticket: `tasks/TKT-000-intake.md`

## Validation results

```text
VALIDATION PASSED: 49 roles, 84 skills, 28 scenarios.
ROUTING TEST PASSED: 28 scenarios, 49 roles, 84 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

## New files

```text
CURRENT.md
TASK_INDEX.md
tasks/TKT-000-intake.md
context/packets/.gitkeep
context/snapshots/.gitkeep
chronicle/.gitkeep
archive/.gitkeep
archive/tasks/.gitkeep

docs/TICKETED_MEMORY.md
docs/CONTEXT_BUDGET_POLICY.md
docs/RUNTIME_LOAD_POLICY.md
docs/TICKET_LIFECYCLE.md
docs/RELEASE_NOTES_2.1_BETA1.md

.agents/skills/context-prune/SKILL.md
.agents/skills/context-snapshot/SKILL.md
.agents/skills/task-ledger/SKILL.md
.agents/skills/ticket-router/SKILL.md
.agents/skills/memory-integrity-check/SKILL.md

.agents/templates/task-ticket.md
.agents/templates/context-snapshot.md
.agents/templates/memory-integrity-report.md

scripts/check-memory-integrity.mjs
```

## Key changes

### 1. `TASK.md` is no longer working memory

`TASK.md` now redirects older instructions to:

```text
CURRENT.md
TASK_INDEX.md
tasks/<active-ticket>.md
CHRONICLE.md
```

The validator blocks legacy working sections inside `TASK.md`.

### 2. `CHRONICLE.md` is compact rescue memory

`CHRONICLE.md` is no longer a full progress log. Detailed logs should go into `chronicle/`, evidence into `context/packets/`, and checkpoints into `context/snapshots/`.

### 3. Always-load context is reduced

The current always-load set is approximately:

```text
AGENTS.md                         9,222 chars
CURRENT.md                        2,135 chars
TASK_INDEX.md                       703 chars
CHRONICLE.md                      1,256 chars
docs/BOOTSTRAP_INDEX.md           4,199 chars
docs/QUESTION_TREE.md             1,445 chars
docs/LANGUAGE_POLICY.md             435 chars
TOTAL                            19,395 chars
```

This keeps startup memory focused while preserving routing and recovery quality.

### 4. Subagents should receive bounded packets

`SUBAGENT_RUN_CONTRACT.md` and related guidance now point to:

```text
CURRENT.md
active tasks/TKT-*.md
context/packets/<operation>.md
selected docs/skills only
```

Not the full project memory.

### 5. Memory integrity is executable

`scripts/check-memory-integrity.mjs` checks:

- required memory files exist;
- `TASK.md` is a shim;
- active ticket exists;
- active ticket is listed in `TASK_INDEX.md`;
- only one current ticket is marked;
- `CHRONICLE.md` is not bloated.

## Contradiction check

Checked and updated:

- `AGENTS.md`
- `FIRST_PROMPT.md`
- `CHRONICLE.md`
- `TASK.md`
- `SUBAGENT_RUN_CONTRACT.md`
- `UI_REVIEW_PACKET.md`
- playbooks / skills / role cards references to working `TASK.md`
- custom agent TOML instructions
- role/skill/scenario indices

Remaining `TASK.md` references are intentional compatibility references, TOML guardrails, release notes, or validator checks.

## Known caveats

1. Some old release notes still mention historical `TASK.md` behavior. They are reference-only and should not be loaded at runtime.
2. `TEAM.md` remains human-readable reference material and is not part of the default runtime loading path.
3. The next real-world test should check whether Codex actually respects `CURRENT.md` and active ticket routing during long UI/design tasks.

## Recommended beta 1 test prompts

### New task

```text
Use 2.1 ticketed memory. Start from CURRENT.md and TASK_INDEX.md. Create or update the active ticket before planning. Do not use TASK.md as working memory.
```

### Resume task after context compression

```text
Resume from CURRENT.md, compact CHRONICLE.md, and the active ticket only. Do not load archive logs or old snapshots unless the active ticket requires them.
```

### Before a large operation

```text
Create a context snapshot, then run the operation with bounded packets. If the active ticket or CHRONICLE.md becomes too large, propose context-prune.
```
