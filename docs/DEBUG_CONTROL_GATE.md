# DEBUG_CONTROL_GATE.md

Prototype/debug controls are useful during development but dangerous in user-facing UI.

## Rule

Any debug/prototype-only control visible in the main UI must be classified:

- `user-facing`: intended product capability;
- `dev-only`: internal testing control;
- `prototype-only`: temporary demo control;
- `unknown`: requires clarification.

## Examples

Potential debug controls:
- “Пустое состояние” switch in a user toolbar;
- route/state toggles;
- fixture selectors;
- fake data controls;
- model/agent debug panels;
- hidden evaluation modes visible to user.

## Blocking conditions

`BLOCKED` if:
- dev-only control is visible in production-like UI;
- prototype-only control is not visually marked or explained;
- control changes user-visible state but is not part of product requirements;
- final UI review ignores an unexplained debug control.

## Required output

Use `.agents/templates/debug-control-report.md`.
