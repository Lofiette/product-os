---
name: cpt-form-task-flow-design
description: Use to design forms and data-entry flows, including question reduction, validation, focus, upload, save-resume, and long processes.
---

# CPT Form Task Flow Design

## Use when

- Users enter, select, upload, review, submit, publish, configure, search, filter, or repeatedly add structured information.
- A form is long, branching, high-risk, multi-session, multi-actor, or expected to serve both novice and expert users.
- Validation, error recovery, focus, keyboard behavior, native semantics, or progressive enhancement materially affects the solution.

## Do not use when

- The task contains no user input or state-changing control.
- Only visual styling of an already governed form component is requested.
- The main problem is broad information architecture with no form or task-flow decision yet.

## Required inputs

- User outcome, context, expertise, frequency, risk, and constraints.
- Question/data requirements, source of truth, dependencies, privacy, and why each value is needed.
- Branching, eligibility, review, confirmation, save/resume, ownership, and offline requirements.
- Validation rules, server/client boundaries, permissions, API behavior, and failure modes.
- Current platform, accessibility, design-system, content, and security authority.

## References and selective loading

1. Read `references/FORM_KNOWLEDGE_POLICY.md`.
2. Use `references/FORM_FLOW_MODE_MATRIX.yaml` to choose the journey model.
3. Load only relevant entries from `references/FORM_PATTERN_CATALOG.yaml`.
4. Apply `references/FORM_ACCESSIBILITY_CONTRACT.md` for custom or dynamic behavior.
5. Use `references/FORM_TASK_FLOW_DECISION.md` for the result.

## Method

1. Run the Question Protocol. For every requested value, state why it is needed, who needs it, when it becomes necessary, whether it can be derived or deferred, and what happens if it is removed.
2. Model the task before the fields: eligibility, prerequisites, sequence, branching, dependencies, review, completion, later correction, and cross-channel or multi-actor handoff.
3. Choose a flow mode from the actual context: compact form, one-thing-per-page, wizard, persistent form, add-another, check-before-you-start, task list, workspace, or a deliberate hybrid.
4. Order questions at the moment they become understandable and acceptable. Preserve entered data when branches, devices, roles, or sessions change.
5. Choose native semantic controls first. Create custom behavior only when native controls cannot meet a verified user need and the team can implement the full keyboard, focus, announcement, fallback, and state contract.
6. Design labels, hints, examples, optionality, defaults, field widths, input modes, autocomplete, formatting tolerance, privacy explanations, and realistic content.
7. Define validation timing and recovery. Prevent avoidable errors, accept harmless format variation, keep user input, show specific messages, provide summary plus local context when needed, and deliberately manage focus.
8. Define dynamic behavior for search, filters, uploads, repeated items, asynchronous checks, partial success, and removal. Specify visible and non-visual feedback without duplicating noise.
9. Design review, final commitment, confirmation, next steps, second-time experience, correction, cancellation, undo, save/resume, and ownership states.
10. Stress with keyboard, screen reader, zoom, touch, low literacy, interruption, slow/failing network, long/localized content, extreme item counts, and server-only validation.
11. Define test evidence, implementation contracts, specialist gates, and falsification criteria.

## Output contract

Produce a `Form Task Flow Decision` containing:

- `Outcome, scope, Question Protocol, removed/deferred/derived data, and confidence.`
- `Flow mode, branching/dependency map, ownership, save/resume, and completion model.`
- `Field/control/content contract and native/custom rationale.`
- `Validation, error, focus, announcement, and recovery matrix.`
- `Search/filter/upload/repetition/asynchronous behavior where applicable.`
- `Review, confirmation, second-time, accessibility, technical, and privacy requirements.`
- `Tests, evidence, blockers, residual risks, and downstream handoff.`

## Evidence standard

- A stakeholder-requested field is not proof that the field is necessary.
- A short completion time is not sufficient if accuracy, recovery, trust, or operating cost worsens.
- Historical browser code and ARIA recipes from sources are not current implementation authority.
- Custom controls require current platform/accessibility verification and cannot be approved from a visual mock alone.

## Stop and escalate

- Legal, security, privacy, payment, identity, or eligibility rules are unresolved.
- Server/client validation ownership or data persistence is unknown.
- A custom control is required but no implementation and accessibility owner exists.
- The business process itself can be removed or materially simplified only by another owner.

## Failure modes to avoid

- Designing fields before questioning the process.
- Treating one-thing-per-page as one literal field per screen.
- Disabling the primary action without telling users how to proceed.
- Validating on every keystroke by default.
- Losing data on back, branch change, error, timeout, or device switch.
- Using placeholder text as the only label or instruction.
- Making links look like controls or controls behave unlike their semantics.
- Building a beautiful custom control with incomplete keyboard, focus, or fallback behavior.
