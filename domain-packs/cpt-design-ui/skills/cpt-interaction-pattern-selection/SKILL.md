---
name: cpt-interaction-pattern-selection
description: Use to select and compose interaction patterns from user behavior, task forces, IA, navigation, lists, forms, and data.
---

# CPT Interaction Pattern Selection

## Use when

- A screen or flow needs an interaction model, page type, navigation structure, workspace model, list behavior, command system, or data-exploration pattern.
- Several familiar patterns could solve the task and the choice needs explicit context, trade-offs, and evidence.
- A requested UI risks being a copied layout rather than a coherent pattern composition.

## Do not use when

- Only token-level styling or visual polish remains.
- The authoritative product pattern is already complete, approved, and applicable without modification.
- The task is exclusively form mechanics; use `cpt-form-task-flow-design` as the primary method and this skill only for surrounding structure.

## Required inputs

- Target users, expertise, frequency, environment, risk, and primary outcome.
- Domain objects, tasks, data size/shape, relationships, permissions, and lifecycle.
- Current IA, entry points, navigation, comparable surfaces, and design-system authority.
- Required devices/input modes, interruption/re-entry needs, and technical constraints.
- Evidence, assumptions, unresolved product decisions, and expected validation method.

## References and selective loading

1. Read `references/INTERACTION_PATTERN_POLICY.md`.
2. Use `references/BEHAVIOR_LENSES.yaml` to identify human-behavior forces.
3. Load only the relevant catalog:
   - `PAGE_NAVIGATION_PATTERNS.yaml` for IA, page, navigation, and layout;
   - `WORKSPACE_COMMAND_PATTERNS.yaml` for lists, workspaces, actions, repetition, and recovery;
   - `DATA_EXPLORATION_PATTERNS.yaml` for analytical exploration and linked views.
4. Use `references/PATTERN_DECISION_RECORD.md` for the result.

Do not load every catalog for a bounded decision.

## Method

1. Restate the user goal and the decision the interface must support, independent of the requested layout.
2. Classify the dominant product surface as overview, focus, creation/workspace, action flow, or a deliberate composition of these types.
3. Identify forces: expertise, frequency, information volume, hierarchy, comparison, reversibility, interruption, repetition, collaboration, latency, and consequence.
4. Apply the relevant behavior lenses. Record which human behaviors the design must support and which assumptions require evidence.
5. Shortlist two to four pattern compositions. A composition includes the primary structure plus navigation, command, recovery, and state patterns, not a single named widget.
6. Compare candidates against task efficiency, discoverability, cognitive demand, expert acceleration, error/recovery, accessibility, responsive behavior, system fit, and implementation cost.
7. Reject patterns that are selected only because they are fashionable, familiar to the designer, space-saving, or present in a reference screenshot.
8. Specify the chosen composition: objects, regions, navigation, actions, transitions, state boundaries, keyboard model, and escape/re-entry behavior.
9. Define evidence to seek, failure signals, and what would cause a different pattern to be selected.
10. Hand the pattern decision to screen/module design, form design, professional-data design, or implementation as appropriate.

## Output contract

Produce a `Pattern Decision Record` containing:

- `Decision, scope, page/workflow classification, and confidence.`
- `Behavior lenses and contextual forces.`
- `Candidate pattern compositions and explicit rejection reasons.`
- `Selected structure, navigation, command, recovery, and state model.`
- `Novice/expert, keyboard, responsive, and interruption implications.`
- `Evidence, risks, validation, falsification criteria, and downstream owner.`

## Evidence standard

- A pattern name is not evidence that it fits.
- Book examples are transformed references, not current platform authority or visual targets.
- Claims about user behavior must trace to project evidence or remain labeled as hypotheses.
- Existing product and design-system patterns override general catalogs within their approved scope.

## Stop and escalate

- The user goal, domain model, or ownership boundary is unresolved.
- A pattern choice changes product architecture, permissions, or design-system scope without an owner.
- The task needs current platform or accessibility behavior that is not supplied or verified.

## Failure modes to avoid

- Cargo-culting a named pattern.
- Treating a page as one pattern instead of a composition.
- Choosing compactness over comprehension or expert speed without evidence.
- Ignoring safe exit, undo, resume, keyboard, or state continuity.
- Presenting old screenshots as a current UI standard.
