# Task Scope Gate

Gate ID: `gate-task-scope`

## Apply when

Before implementation when scope, acceptance criteria, work mode, or approval boundary may be ambiguous.

## Owners

- `intake_orchestrator`
- `delivery_manager`

## PASS criteria

- Objective and intended outcome are explicit.
- In-scope and out-of-scope boundaries are recorded.
- Acceptance evidence and approval lease are sufficient for the next operation.

## BLOCK criteria

- A plausible interpretation would materially change files, risks, or acceptance criteria.
- The user request is discovery-only but implementation is about to begin.
- The approved scope cannot be distinguished from optional improvement ideas.

## Required evidence

- Active task or micro-change record
- Impact Map or compact scope note
- User approval or lease

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
