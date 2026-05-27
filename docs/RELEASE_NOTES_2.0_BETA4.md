# Release Notes — Codex Product Team 2.0 beta 4

## Focus

Reference Fidelity & Design Source Authority Patch.

## Added

- `docs/REFERENCE_FIDELITY.md`
- `docs/DESIGN_SOURCE_AUTHORITY.md`
- `docs/MANIFEST_FREEZE_POLICY.md`
- `docs/SCREENSHOT_VISUAL_GATE.md`
- `docs/CONTENT_REALISM.md`
- `docs/DEBUG_CONTROL_GATE.md`
- `docs/VISUAL_ACCEPTANCE_CRITERIA.md`
- skills: `reference-fidelity`, `design-source-authority`, `manifest-freeze-check`, `screenshot-reference-comparison`, `content-realism-review`, `debug-control-review`
- templates for reference fidelity, actual/reference delta, source authority, screenshot comparison, content realism, and debug-control reports
- `scripts/check-design-source-authority.mjs`

## Runtime rules

- “Looks similar” is not evidence.
- Build success is not design success.
- Generated artifacts cannot validate themselves.
- No final UI PASS without reference comparison when a visual reference exists and rendering is possible.
- Prototype/demo content must be realistic enough to judge layout, hierarchy, and comprehension.
