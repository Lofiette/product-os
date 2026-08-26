# Codex Product Team 2.0 beta 4 — Reference Fidelity & DS Authority Patch Audit

## Verdict

PASS.

Beta 4 was created from the beta 3 archive and focuses on the failure mode observed in UI work: Codex can pass build/import/raw-value checks while still producing poor interface design, weak reference fidelity, and self-validating design-system compliance.

## Validation

```text
VALIDATION PASSED: 49 roles, 79 skills, 25 scenarios.
ROUTING TEST PASSED: 25 scenarios, 49 roles, 79 skills.
Node syntax checks: PASS.
Zip integrity: OK.
```

## Main runtime fix

Beta 4 adds a hard distinction between technical success and design success:

- Build success is not design success.
- Console-clean route is not visual QA.
- Raw-value scan passing is not design-system compliance.
- Component import scan passing is not component correctness.
- “Looks similar” is not evidence.
- Generated artifacts cannot validate themselves.

## Added docs

- `docs/REFERENCE_FIDELITY.md`
- `docs/DESIGN_SOURCE_AUTHORITY.md`
- `docs/MANIFEST_FREEZE_POLICY.md`
- `docs/SCREENSHOT_VISUAL_GATE.md`
- `docs/CONTENT_REALISM.md`
- `docs/DEBUG_CONTROL_GATE.md`
- `docs/VISUAL_ACCEPTANCE_CRITERIA.md`

## Added skills

- `reference-fidelity`
- `design-source-authority`
- `manifest-freeze-check`
- `screenshot-reference-comparison`
- `content-realism-review`
- `debug-control-review`

## Added templates

- `reference-fidelity-spec.md`
- `actual-vs-reference-delta.md`
- `design-source-authority-report.md`
- `screenshot-comparison-report.md`
- `content-realism-report.md`
- `debug-control-report.md`

## Added script

- `scripts/check-design-source-authority.mjs`

This script detects whether common DS manifest paths are tracked/changed/untracked and warns when a manifest cannot safely prove compliance.

## Updated runtime behavior

When the user provides a reference image, good example, bad example, screenshot, or visual target, Codex should:

1. Run `reference-fidelity` before implementation.
2. Extract a Reference Fidelity Spec.
3. Ask approval for ambiguous deviations.
4. After implementation, run `screenshot-reference-comparison` if rendering is possible.
5. Refuse final UI PASS if comparison is missing.

When DS manifest/registry/docs are generated or changed in the same task, Codex should:

1. Run `design-source-authority` and `manifest-freeze-check`.
2. Report whether the manifest is authoritative, candidate, provisional, or self-generated.
3. Refuse to use a self-generated manifest as proof of compliance without explicit user approval.

When prototype/demo content is generated, Codex should:

1. Run `content-realism-review`.
2. Block final PASS if placeholder/internal content prevents judging hierarchy, comprehension, or target-audience fit.

When dev/prototype controls appear in a user-facing UI, Codex should:

1. Run `debug-control-review`.
2. Classify each visible debug/prototype control.
3. Block final PASS if the control is unexplained or not approved.

## Added scenarios

- `reference_driven_ui_prototype_blocking`
- `generated_manifest_self_validation_blocked`
- `debug_control_and_content_realism_review`

## Key quality gate upgrades

`docs/UI_QUALITY_GATES.md` now includes:

- Reference Fidelity Gate
- Design Source Authority Gate
- Content Realism Gate
- Debug Control Gate
- Visual Acceptance reminder

## Important practical prompt for UI work

```text
Use beta 4 strict UI workflow.
If I provide a reference image or good/bad examples, create a Reference Fidelity Spec before implementation.
Do not treat build success, raw-value scan, or component-import scan as design success.
If any DS manifest was created or changed in this task, do not use it as proof of compliance without my approval.
After implementation, compare actual rendered UI against the reference and report PASS/WARN/BLOCKED.
No final PASS without screenshot/reference comparison when rendering is possible.
```

## Remaining watchpoints

Beta 4 improves enforcement, but real Codex runs still need observation:

- Does Codex actually call `reference-fidelity` when images are provided?
- Does it refuse self-generated DS manifest evidence?
- Does it issue `BLOCKED` instead of `PASS WITH WARNINGS` for visibly poor UI?
- Does it perform real screenshot comparison rather than route smoke checks?
- Does it treat sample content as design evidence, not filler?

These should be tested on real UI prototype tasks.
