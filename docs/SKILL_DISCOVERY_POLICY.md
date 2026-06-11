# SKILL_DISCOVERY_POLICY.md

This repository contains many skills. Do not rely on implicit skill discovery for important workflows.

## Rules

1. For Tiny/Micro work, do not load role or skill indexes unless the route is unclear.
2. For Standard+ work, use staged routing:
   - `docs/SKILL_ROUTER_INDEX.json` when the domain is unclear;
   - `docs/ROLE_TINY_INDEX.json` and `docs/SKILL_TINY_INDEX.json` for first-pass routing;
   - full `docs/SKILL_INDEX.json` only when tiny routing is insufficient.
3. Critical UI/design skills must be explicitly selected when their trigger is present.
4. If a user provides a reference screenshot, good example, bad example, Figma export, or mock image, explicitly select `reference-fidelity` before implementation.
5. If a UI was implemented and a reference/spec exists, explicitly select `screenshot-reference-comparison` before final PASS.
6. If design-system compliance is claimed, explicitly select `design-source-authority` and `design-system-compliance`.
7. If Codex cannot confirm that a needed skill was loaded or applied, report `INSUFFICIENT WORKFLOW EVIDENCE` rather than PASS.

## Why

Codex skills use progressive disclosure. The initial skill list is budgeted, so in a large skill set some descriptions can be shortened or omitted. Exact skill selection from routing docs and the active ticket is more reliable than hoping implicit matching picked the right workflow.

## Critical skill groups

### Memory

- `ticket-router`
- `task-ledger`
- `context-snapshot`
- `context-prune`
- `memory-integrity-check`

### UI / design quality

- `design-recon`
- `prototype-ui-kit`
- `screen-redesign`
- `module-design`
- `reference-fidelity`
- `screenshot-reference-comparison`
- `design-source-authority`
- `design-system-compliance`
- `visual-qa-loop`
- `taste-review`

### Runtime reliability

- `subagent-run-contract`
- `subagent-failure-recovery`
- `ui-review-packet`
- `current-page-ui-review`

### Production

- `repo-recon`
- `production-service-planning`
- `production-readiness-review`
- `component-contract-scan`
- `ds-code-contract-enforcement`
