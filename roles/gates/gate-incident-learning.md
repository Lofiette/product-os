# Incident Learning Gate

Gate ID: `gate-incident-learning`

## Apply when

For incident closure, root-cause claims, or corrective action planning.

## Owners

- `incident_investigator`
- `observability_engineer`

## PASS criteria

- Impact, timeline, evidence, root/contributing causes, containment, corrective actions, owners, and validation are explicit.
- Learning is systemic rather than blame-focused.

## BLOCK criteria

- Root cause is asserted without evidence.
- Actions only tell people to be more careful.
- Recurrence detection or validation is missing.

## Required evidence

- Incident timeline
- Evidence/hypothesis log
- Corrective action register
- Validation plan

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
