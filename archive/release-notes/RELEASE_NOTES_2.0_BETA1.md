# Codex Product Team 2.0 beta 2 Release Notes

## Focus

2.0 beta 2 hardens the practical runtime for UI, module, and production web/service tasks. It upgrades skills from generic shells into operational workflows and adds executable DS/code checks.

## Main changes

- Added `prototype-ui-kit` for UI prototypes without a design system.
- Added `module-design` and `design-handoff-qa` for module design and later developer rebuild.
- Added phased orchestration and production readiness gates.
- Added `ds-code-contract-enforcement` and `e2e-visual-state-capture`.
- Fixed `find-raw-ui-values.mjs` syntax and made it usable.
- Upgraded `check-component-imports.mjs` from placeholder to heuristic scanner.
- Added `ROLE_MINI_INDEX.json` for cheaper routing.
- Updated FIRST_PROMPT to force role/skill index loading after intake and explicit spawned/simulated declaration after approval.
- Added scenario tests for module handoff and production web service with DS in code.

## Runtime principle

Do not rely on role titles alone. Every selected role must own an artifact, every loaded skill must change a decision/check/handoff, and every real subagent spawn must be approved and explicitly announced.
