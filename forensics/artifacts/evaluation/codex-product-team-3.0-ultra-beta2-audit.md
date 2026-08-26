# Codex Product Team 3.0 Ultra beta 2 — Control Audit

## Verdict

PASS.

This build applies the targeted hardening requested after the 3.0 Ultra control audit. The package is structurally valid, runtime-coherent, and better aligned with the 3.0 operating model.

## Validation results

```text
VALIDATION PASSED: 50 roles, 95 skills, 34 scenarios.
3.0 VALIDATION PASSED: 50 roles, 95 skills, 34 scenarios.
ROUTING TEST PASSED: 34 scenarios, 50 roles, 95 skills.
MEMORY INTEGRITY PASSED.
Node syntax checks: PASS.
Zip integrity: PASS.
```

## Inventory

```text
Roles indexed:         50
Role cards:            50
Playbooks:             50
Custom agent TOMLs:    50
Skills indexed:        95
Skill files:           95
Scenario tests:        34
```

## Fixes applied

### 1. Stale version labels removed

Updated stale 2.x references in runtime/config locations:

- `.codex/config.toml` now uses `codex-product-team-3.0-ultra-beta2`.
- `ROLE_INDEX.json`, `ROLE_MINI_INDEX.json`, `ROLE_TINY_INDEX.json`, `SCENARIO_TESTS.json` are updated to `3.0-ultra-beta2`.
- Old `RELEASE_NOTES_2.1_BETA4.md` moved to `archive/release-notes/`.
- `VALIDATOR_RULES.md` now describes 3.0 beta 2 validation rules.
- `validate_3_0.py` now checks stale 2.x labels outside `archive/`.

### 2. Routing matrices updated for 3.0

`ROLE_ROUTING_MATRIX.md` now explicitly covers:

- Runtime / task management;
- Product Knowledge onboarding;
- Existing product / greenfield / redesign modes;
- UI discovery/planning/review;
- UI/product implementation with `frontend_engineer`;
- API-dependent UI with `api_contract_guardian`;
- AI, risk, research, service, growth, and localization routing.

`SKILL_ROUTING_MATRIX.md` now explicitly covers:

- Runtime Kernel / Safe Autonomy;
- Product Knowledge System;
- UI/design/DS flows;
- Frontend implementation;
- API/Data Shape prewarm;
- AI/risk/ops;
- Research/analytics/service.

### 3. 3.0 skills upgraded from generic shells

Expanded operational content for critical skills:

- `new-task-protocol`
- `bounded-discovery`
- `impact-map`
- `product-knowledge-onboarding`
- `api-data-shape-prewarm`
- `framework-loading`
- `knowledge-update`
- `greenfield-onboarding`
- `knowledge-freshness-review`

These skills now include concrete inputs, procedures, output artifacts, rules, and stop/failure conditions.

### 4. Role metadata added

`ROLE_INDEX.json` now includes staged-loading metadata:

- `default_execution`
- `spawn_policy`
- `load_cost`
- `primary_task_types`

This supports routing without loading every role card/playbook and makes simulation/subagent eligibility more explicit.

### 5. TKT-000 placeholder clarified

`CURRENT.md`, `CHRONICLE.md`, and `tasks/TKT-000-ready.md` now clarify:

- `TKT-000` is an intake placeholder;
- no active user task is selected;
- replace the placeholder with a real ticket when the user provides a concrete task.

### 6. Scenario suite strengthened

Added/updated scenarios:

- `existing_product_knowledge_onboarding`
- `new_task_safe_autonomy`
- updated `new_task_protocol_ui_button`
- updated `greenfield_product_start`
- updated `api_data_shape_prewarm`

Markdown scenario files are synchronized with JSON scenario IDs.

### 7. Validators hardened

`validate_3_0.py` now checks:

- stale 2.x labels outside archive;
- missing 3.0 critical skills;
- routing matrix references to `frontend_engineer`, Runtime Kernel, Product Knowledge, API-dependent UI;
- staged-loading role metadata;
- scenario markdown / JSON sync;
- universal-doc ban on project-specific design-system names;
- soft artifact-size policy presence.

`validate_kit.py` now treats `new-task-protocol` and `knowledge-freshness-review` as required runtime skills.

## Remaining considerations

No blocking issues found.

Recommended future live-test focus:

1. Existing product UI task:
   - user gives a task;
   - Codex creates/proposes ticket;
   - reads Product Knowledge;
   - chooses area map;
   - selects `frontend_engineer` + relevant UI roles;
   - produces Impact Map;
   - asks approval before edits.

2. Greenfield product task:
   - Codex creates hypothesis Product Knowledge;
   - marks planned behavior as hypothesis, not confirmed.

3. API-dependent UI task:
   - Codex uses API/Data Shape prewarm;
   - does not deep-read backend unless task requires it.

4. Chronicle compaction stress:
   - after multiple task steps, `CHRONICLE.md` remains compact.

## Release recommendation

3.0 Ultra beta 2 is ready for live testing.

It should not yet be called final RC until it passes at least two live tasks:

- one existing-product UI implementation task;
- one product-knowledge / API-dependent task.
