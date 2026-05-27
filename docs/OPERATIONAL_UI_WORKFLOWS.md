# OPERATIONAL_UI_WORKFLOWS.md

## Screen workflow

1. Repo recon if existing repo.
2. Design recon if UI is affected.
3. Determine DS mode.
4. Produce Screen Design Spec.
5. Produce component tree and state matrix.
6. Ask approval if scope/design direction changes.
7. Implement approved scope.
8. Run DS compliance and UI obvious errors checks.
9. Render/screenshot if possible.
10. Fix blockers.
11. Produce Design Diff Summary.

## Module workflow

1. Recon.
2. Module Design Package.
3. Component matrix.
4. Cross-screen state matrix.
5. Developer Rebuild Brief.
6. Design Handoff QA.
7. Optional implementation only after approval.

## Production web service workflow

1. Phased orchestration.
2. Production readiness gates.
3. Risk roles only when triggered.
4. Implementation with verification.
5. Design/DS compliance for UI.
6. Release and rollback notes.

## Reference-first UI workflow

When the user provides a reference:

1. `design-recon`
2. `design-source-authority`
3. `reference-fidelity`
4. `taste-calibration` / `example-taste-board` if examples exist
5. screen/module/prototype design skill
6. implementation only after approval if fidelity implications change scope
7. `screenshot-reference-comparison`
8. `content-realism-review`
9. `debug-control-review`
10. final UI verdict

No final UI PASS without required evidence.
