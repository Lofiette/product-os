# Evidence Integrity Gate

Gate ID: `gate-evidence-integrity`

## Apply when

Whenever conclusions depend on research, product claims, external facts, inferred behavior, or incomplete code evidence.

## Owners

- `consistency_auditor`
- `domain_expert`

## PASS criteria

- Claims distinguish confirmed evidence, inference, hypothesis, and unknown.
- Each load-bearing claim points to an approved source.
- Contradictions and missing evidence are visible.

## BLOCK criteria

- A hypothesis is presented as a finding.
- A generated artifact validates itself without an independent source.
- The result cannot show how its conclusion was reached.

## Required evidence

- Evidence table or citations
- Claim-status markers
- Contradiction log

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
