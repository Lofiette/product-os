# Product Designer Design Intelligence Evaluation Preview

Status: `preview-not-beta-certified`

This adjunct evaluates Product Designer reasoning, interaction intelligence, form/professional workflow quality, UI craft, and capability-portable execution. It does not modify the existing 21-case executable Evaluation Plane or its offline Beta 1 baseline.

## Purpose

The existing Evaluation Plane verifies runtime, routing, skills, traces, filesystem outcomes, and bounded task behavior. This preview adds a future-facing layer for:

- product-design reasoning;
- human-behavior and interaction-pattern selection;
- forms, validation, focus, long processes, and inclusive operation;
- professional density, expert throughput, bulk actions, and linked data;
- UI craft and adversarial critique;
- design execution capability discovery, adapters, provenance, and fallbacks;
- human-versus-agent comparison;
- eventual screenshot-based evaluation.

## Assets

- `rubric.json`: machine-readable 16-dimension rubric.
- `baseline-cases.json`: 20 Product Designer cases.
- `schema.json`: validation contract.
- `../../tools/validate_design_intelligence.py`: deterministic structure validator.
- `../../tools/validate_product_design_vnext2.py`: pattern/form/professional/execution knowledge validator.

## Evaluation model

Use a mixed evidence model:

1. Deterministic checks for required artifacts, files, states, source/capability provenance, design-system references, and explicit constraints.
2. Human review for product judgment, pattern fit, form/service trade-offs, professional workflow quality, and visual craft.
3. LLM-as-judge only with the same rubric, blinded alternatives, explicit evidence, and periodic human calibration.
4. Screenshot or rendered-prototype review for final visual claims.
5. Pairwise comparison when evaluating human and agent solutions.
6. Provider-independent acceptance when an execution adapter creates the artifact.

## Verdict rule

A weighted score is diagnostic. Any critical error or blocker produces `BLOCKED` regardless of average score. Missing rendered evidence or missing capability/source provenance produces `INSUFFICIENT_EVIDENCE` for the affected claim.

## Human-versus-agent protocol

1. Freeze the same brief, design system, product knowledge, constraints, and time box.
2. Produce independent solutions without cross-contamination.
3. Remove author identity and normalize presentation quality where possible.
4. Evaluate product/pattern reasoning and rendered UI separately.
5. Use the same rubric and task-specific weights.
6. Record evaluator confidence and disagreements.
7. Compare profiles by dimension rather than only total score.
8. Preserve the combined `human + agent` condition as a separate benchmark.

## Future integration

When stable rendering fixtures exist, promote selected cases into the executable plane with realistic data, state/breakpoint capture, trace requirements, accessibility/design-system checks, reviewed baselines, and mutation cases. External plugin adapters require separate live certification per host and version.
