# Codex Product Team 2.1 beta 4

A role-skill orchestration framework for Codex that can either simulate product-team roles in the main thread or spawn approved custom subagents for bounded expert work.

## Start

1. Open this folder in Codex.
2. Paste `FIRST_PROMPT.md`.
3. Answer only decision-changing intake questions.
4. Review the proposed roles, skills, orchestration mode, gates, and context budget.
5. Approve real subagent spawn or request cheaper simulation mode.

## Key ideas

- Roles own decisions and artifacts.
- Skills are reusable methods/workflows.
- Custom agents are spawnable role executors.
- Real subagents run only after explicit approval unless auto-orchestration was explicitly approved.
- Ticketed memory keeps long-running work compact: use `CURRENT.md`, `TASK_INDEX.md`, active `tasks/TKT-*.md`, and compact `CHRONICLE.md`.
- `TASK.md` is only a deprecated compatibility pointer.
- UI work requires design recon, design-system authority checks, and reference/taste/visual gates when relevant.
- Design systems may be absent, emerging, component-based, documented, or governed.

## Important files

- `AGENTS.md` — core runtime rules.
- `FIRST_PROMPT.md` — startup prompt.
- `CURRENT.md` — active control panel.
- `TASK_INDEX.md` — ticket ledger.
- `tasks/TKT-*.md` — detailed task briefs.
- `CHRONICLE.md` — compact rescue summary.
- `docs/BOOTSTRAP_INDEX.md` — compact startup map.
- `docs/CONTEXT_BUDGET_POLICY.md` — context loading tiers.
- `docs/RUNTIME_LOAD_POLICY.md` — runtime/reference file separation.
- `docs/TICKETED_MEMORY.md` — memory model.
- `docs/SUBAGENT_ORCHESTRATION.md` — real subagent rules.
- `docs/ROLE_SKILL_ARCHITECTURE.md` — role/skill model.
- `docs/DESIGN_SYSTEM_MODES.md` — no DS vs rich DS handling.
- `docs/REFERENCE_FIDELITY.md` — reference-driven UI constraints.
- `docs/DESIGN_SOURCE_AUTHORITY.md` — DS/source authority rules.
- `docs/UI_QUALITY_GATES.md` — blocking UI quality checks.

## 2.1 beta 4 focus

Beta 4 is a targeted hardening patch for context economy, diagnostics, and skill-discovery discipline:

- Fixes `scripts/validate_kit.py` as a proper executable script.
- Adds validator checks for executable shebangs and strict DS scanner behavior.
- Adds strict DS mode to `scripts/check-component-imports.mjs`:
  - `--strict-ds`
  - `--fail-on-warning`
  - DS source-file exclusions for native primitives.
- Prevents obvious Tiny/Micro tasks from loading role/skill indexes by default.
- Adds `docs/SKILL_ROUTER_INDEX.json` as an optional ultra-light domain router before heavier indexes.
- Updates scenario behavior checks for Tiny/Micro, production UI, spawn approval, and reference/manifest gates.
- Fixes legacy `TASK` wording in skill indexes: implementation review now references the active ticket.

## Runtime loading summary

Tier 0 startup files:

- `AGENTS.md`
- `CURRENT.md`
- `TASK_INDEX.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/LANGUAGE_POLICY.md`

After intake:

- Tiny/Micro obvious reversible work: do **not** load role/skill indexes by default.
- Fast Lane: load tiny indexes only when routing is unclear or a gate may be triggered.
- Standard+: optionally use `docs/SKILL_ROUTER_INDEX.json`, then load `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json`.
- Mini/full indexes, role cards, full playbooks, and full skill docs load only when they can change a decision.

Do not load archives, all tickets, all skills, all playbooks, release notes, self-audit reports, or reference-only docs by default.

## Validation

Run:

```bash
python scripts/validate_kit.py
./scripts/validate_kit.py
python scripts/test-routing.py
node scripts/check-memory-integrity.mjs
```

Expected result:

```text
VALIDATION PASSED
ROUTING TEST PASSED
MEMORY INTEGRITY PASSED
```
