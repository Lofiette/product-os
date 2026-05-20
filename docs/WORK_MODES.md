# WORK_MODES.md

## Research
Goal: reduce uncertainty before building.
Default output: research plan, evidence map, hypotheses, risks, and next decisions.
Do not implement unless explicitly approved.

## Prototype
Goal: make an idea tangible, usually UI/interaction focused.
Quality bar: fast, exploratory, disposable or semi-disposable.
Avoid overbuilding infrastructure.

## PoC
Goal: prove technical feasibility.
Quality bar: clear technical hypothesis, constraints, result, and decision.
Avoid product polish unless needed for the proof.

## MVP
Goal: smallest valuable end-to-end product slice.
Quality bar: user can complete a real core flow; scope is narrow but coherent.

## Production change
Goal: safely change a live system.
Quality bar: tests, rollout, rollback, risks, compatibility, observability.

## Bugfix
Goal: reproduce, isolate, fix, verify.
Quality bar: root cause, regression test when feasible, minimal fix.

## Refactor
Goal: improve structure while preserving behavior.
Quality bar: staged plan, behavior-preservation tests, no opportunistic expansion.

## Review / audit
Goal: evaluate existing work.
Quality bar: evidence-backed findings, severity, recommendations, no unnecessary edits.

## Data / analytics
Goal: answer measurement questions or build instrumentation.
Quality bar: definitions, event schema, data caveats, reproducibility.

## Incident response
Goal: triage, mitigate, understand root cause, prevent recurrence.
Quality bar: timeline, evidence, blast radius, mitigation, follow-ups.

## Documentation / handoff
Goal: make work understandable and maintainable.
Quality bar: concise, accurate, evidence-linked, audience-appropriate.
