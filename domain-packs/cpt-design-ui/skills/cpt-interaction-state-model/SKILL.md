---
name: cpt-interaction-state-model
description: Use to define interaction behavior and complete state coverage across empty, loading, success, error, permission, responsive, and edge cases.
---

# CPT Interaction State Model

## Use when

- A UI flow or component has multiple asynchronous, validation, permission, or lifecycle states.

## Do not use when

- The task is purely static visual styling.

## Required inputs

- User flow, actions, data/API contract, permissions, validation, design-system patterns, and failure/recovery behavior.

## Method

1. List actors, triggers, actions, objects, and system events.
2. Build state inventory across initial, loading, empty, partial, populated, success, error, stale, offline, permission, disabled, destructive, and responsive conditions.
3. Define transitions, guards, retries, cancellation, optimistic/pessimistic behavior, and recovery.
4. Specify UI behavior, copy, focus, announcements, and primary/secondary actions per state.
5. Check impossible/ambiguous transitions and consistency across related surfaces.
6. Map each state to implementation evidence and verification.

## Output contract

Produce a compact artifact containing:

- `State/transition matrix.`
- `UI behavior and content per state.`
- `Recovery, accessibility, and responsive requirements.`
- `Implementation/verification mapping and unknowns.`

## Evidence standard

- Data/API states should cite actual contracts or remain assumptions.

## Stop and escalate

- State ownership or server/client source of truth is unresolved.

## Failure modes to avoid

- Listing states without transitions.
- Treating disabled as an explanation.
