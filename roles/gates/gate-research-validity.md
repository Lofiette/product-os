# Research Validity Gate

Gate ID: `gate-research-validity`

## Apply when

Before treating research output as decision-grade evidence.

## Owners

- `ux_researcher`
- `market_researcher`
- `cx_researcher`

## PASS criteria

- Method matches the decision question.
- Sampling, limitations, bias risks, and confidence are documented.
- Findings are grounded in observed evidence rather than opinion alone.

## BLOCK criteria

- Research questions and method do not align.
- Stakeholder assumptions are labelled as user findings.
- The sample cannot support the claimed generalization.

## Required evidence

- Research plan
- Participant/source profile
- Raw-evidence trace
- Synthesis with confidence

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
