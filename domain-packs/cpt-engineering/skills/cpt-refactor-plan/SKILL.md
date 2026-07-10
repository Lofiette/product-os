---
name: cpt-refactor-plan
description: Use to plan behavior-preserving refactoring with characterization tests, staged changes, invariants, and rollback.
---

# CPT Refactor Plan

## Use when

- Code structure must improve without intended product behavior change.

## Do not use when

- The desired behavior itself is changing materially.

## Required inputs

- Refactor goal, current behavior/invariants, dependency graph, tests, hotspots, constraints, and rollout risk.

## Method

1. Define structural problem, target qualities, and behaviors that must not change.
2. Map callers, dependencies, state, side effects, extension points, and ownership.
3. Establish characterization tests and observability before restructuring.
4. Choose seams and stages that keep the system working after each step.
5. Separate mechanical moves from semantic changes.
6. Plan compatibility adapters, deprecation, cleanup, and rollback.
7. Define performance, bundle, API, and data checks where relevant.

## Output contract

Produce a compact artifact containing:

- `Refactor scope and invariants.`
- `Dependency/seam map.`
- `Staged plan and characterization tests.`
- `Risk, rollback, and completion criteria.`

## Evidence standard

- Behavior preservation needs tests or runtime evidence, not intent.

## Stop and escalate

- Current behavior is unknown or tests cannot characterize critical paths.

## Failure modes to avoid

- Mixing feature changes into refactor.
- Large-bang rewrite without working intermediate states.
