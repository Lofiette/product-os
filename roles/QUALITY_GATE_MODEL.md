# Quality Gate Model

A gate is an evidence-based acceptance contract. It is not a role, checklist decoration, or ceremonial approval.

## Verdicts

- `PASS`: evidence supports acceptance.
- `PASS_WITH_WARNINGS`: acceptance is supportable with explicit non-blocking residual risk.
- `BLOCKED`: a blocking condition is present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

## Application

- Select gates from task/risk/role routing.
- Identify gate owners before implementation.
- State required evidence before the gate runs.
- A warning cannot hide a blocker.
- Missing evidence cannot be converted into PASS.
- The same agent may implement and self-check low-risk work, but material independent-review gates should use an independent reviewer when practical.
- Gate output must link to evidence and identify remaining risk/owner.

`GATE_REGISTRY.json` and `roles/gates/*.md` are canonical for Beta 1.
