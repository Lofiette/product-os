# Form Accessibility Contract

Use for any custom, dynamic, asynchronous, or multi-step form behavior.

## Required behavior

- Every input and group has a clear accessible name; essential instructions remain available while entering and reviewing.
- Native semantics are the baseline. ARIA supplements semantics and state; it does not excuse an incorrect interaction model.
- Full task completion is possible with keyboard alone, with visible focus and predictable order.
- Composite controls use a deliberate single-entry keyboard model and documented internal navigation.
- Dynamic additions, removals, loading, validation, upload, and completion have an intentional focus and announcement plan.
- Information and status do not rely on color, motion, position, or visual change alone.
- Zoom, reflow, long labels, localization, and on-screen keyboards do not hide instructions, errors, or actions.
- Input is preserved across validation, back, branch changes, timeouts, and recoverable failures.
- A basic or fallback route remains usable when enhancement, script, service, or device capability fails.

## Custom-control acceptance

A custom control is `BLOCKED` until its owner supplies:

1. user need not met by a native option;
2. semantic role/name/value/state contract;
3. keyboard model and focus transitions;
4. pointer/touch model;
5. announcements and errors;
6. fallback/progressive-enhancement behavior;
7. disabled/read-only/permission/loading states;
8. current accessibility verification and test evidence.
