# REFERENCE_FIDELITY.md

Use this document whenever the user provides a visual reference, screenshot, design mock, Figma export, product example, or explicit good/bad visual example that should influence a UI/design result.

## Core rule

A visual reference is not inspiration by default. It is a design constraint until the user says otherwise.

`Looks similar` is not evidence.

Reference fidelity must be proven through observed reference traits, an approved adaptation plan, and post-implementation comparison.

## When required

Required when:
- the user provides a screenshot/reference and asks to build, redesign, prototype, or review UI;
- the user says “как на референсе”, “в таком духе”, “по этому примеру”, “не как в плохом примере”;
- a Taste Profile uses good/bad examples;
- UI quality is judged against a target visual direction.

Optional when:
- reference is only mood inspiration and the user explicitly says fidelity is not important.

## Reference Fidelity workflow

1. **Extract the reference contract before implementation.**
   - layout anatomy;
   - component anatomy;
   - navigation/shell structure;
   - toolbar/search/filter behavior;
   - card/list/table anatomy;
   - information hierarchy;
   - density and spacing rhythm;
   - typography hierarchy;
   - color/emphasis strategy;
   - iconography/control style;
   - content tone and realism;
   - must-match traits;
   - may-adapt traits;
   - must-not-copy traits.

2. **Ask for approval when fidelity is ambiguous.**
   If reference can be interpreted multiple ways, ask the user which traits matter.

3. **Implementation must cite the reference contract.**
   UI choices should map to the reference traits or approved deviations.

4. **Post-implementation comparison is mandatory.**
   Compare actual rendered UI against the reference contract and screenshot if available.

5. **Final UI verdict cannot be PASS without reference comparison.**
   If no rendered screenshot is available, maximum verdict is `PASS WITH WARNINGS`.

## Severity

- **BLOCKER**: violates must-match trait, breaks primary hierarchy, exposes wrong product model, or contradicts explicit bad example.
- **MAJOR**: noticeable divergence that harms clarity, taste, density, or DS fidelity.
- **MINOR**: acceptable difference that should be noted or polished later.

## Required artifact

Use `.agents/templates/reference-fidelity-spec.md`.

## Evidence rules

Valid evidence:
- reference image/screenshot observation;
- actual screenshot/rendered UI;
- component source;
- token source;
- DS document/source;
- approved deviation;
- user-provided clarification.

Invalid evidence:
- “looks close”;
- build success;
- absence of console errors;
- raw value scan passing;
- a Codex-generated manifest created after the implementation.
