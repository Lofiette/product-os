# Verification Gate

Gate ID: `gate-verification`

## Apply when

Before declaring an implementation or review task complete.

## Owners

- `qa_engineer`
- `code_reviewer`

## PASS criteria

- Verification strategy matches risk.
- Changed behavior, edges, regressions, and visual/runtime evidence are covered as applicable.
- Commands and results are reported honestly.

## BLOCK criteria

- No evidence supports the completion claim.
- Only compilation is used to validate user-facing behavior.
- Known blockers are hidden as warnings.

## Required evidence

- Test matrix/results
- Review findings
- Rendered/runtime evidence
- Residual risks

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
