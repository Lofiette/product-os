# Product Design Quality Gate

Gate ID: `gate-design-quality`

## Apply when

For new or redesigned screens, flows, forms, professional workspaces, modules, interaction behavior, execution artifacts, or material visual changes.

The gate is stage-aware:

- During concept or low-fidelity work, it evaluates problem fit, behavior/pattern model, hierarchy intent, state planning, and validation readiness.
- During high-fidelity or implementation acceptance, it also requires rendered UI craft evidence across representative states and contexts.
- When an execution adapter is used, it additionally evaluates capability provenance, source fidelity, approval boundaries, and independent acceptance.

## Owners

- `product_designer`
- `ux_interaction_reviewer`

## PASS criteria

### Problem and evidence

- The actual user task, product outcome, context, success condition, scope, and non-goals are explicit.
- Evidence, assumptions, confidence, and unknowns are separated.
- The solution does not invent critical domain, user, data, permission, legal, security, or technical facts.

### Behavior, pattern, and product model

- Objects, actions, page/workflow type, pattern composition, navigation, permissions, selection scope, states, transitions, feedback, interruption, failure, and recovery are coherent.
- Pattern choices trace to contextual forces and alternatives rather than names, screenshots, or fashion.
- The primary task is efficient for target frequency and expertise; novice support does not impose an unjustified permanent tax on experts.
- Material alternatives and trade-offs are visible for consequential decisions.
- Required behavior can be implemented without inventing core decisions.

### Forms and professional workflows

- Requested data has a purpose, timing, ownership, and necessity or is removed, derived, deferred, prefilled, or explicitly optional.
- Validation, errors, focus, announcements, preservation, review, commitment, confirmation, and save/resume are designed when applicable.
- Professional interfaces preserve useful comparison, stable action/selection scope, keyboard operation, auditability, and partial-failure recovery.
- Draft, saved, queued, published, full success, and partial success are not conflated.

### Information and visual hierarchy

- Location, current state, primary information, primary action, and main groups are understandable.
- Visual prominence matches task and product priority.
- Grouping, alignment, spacing, density, typography, color, boundaries, and affordances form an intentional and coherent visual contract.
- Necessary complexity is structured rather than hidden; unnecessary UI has been challenged through a subtraction pass.

### System, content, accessibility, and robustness

- Authoritative design-system components, tokens, patterns, and deviations are explicit.
- Content is realistic, consistent, and sufficient for actions, states, errors, and recovery.
- Accessibility requirements are designed into semantics, focus, keyboard, announcements, contrast, non-color cues, target size, zoom/reflow, and motion.
- Responsive behavior preserves priority, relationships, spatial continuity, and operability.
- Applicable empty, loading, partial, success, error, stale, offline, conflict, permission, disabled, destructive, interrupted, localized, and extreme-data states are covered.

### Execution and acceptance

- The decision includes falsification criteria and an appropriate validation plan.
- Any execution adapter was actually observed, used within approval boundaries, and has a documented vendor-independent fallback or explicit quality loss.
- Source authority, generated artifacts, tool provenance, writes, publishing visibility, rollback, and limitations are recorded.
- Adapter-produced QA is independently challenged for material acceptance where feasible.
- High-fidelity or implementation PASS includes sufficient rendered evidence and visual review.
- Specialist gates remain satisfied or explicitly pending outside the claimed scope.

## BLOCK criteria

- The solution does not address the stated problem or product outcome.
- A pattern or visual reference is copied without contextual fit, alternatives, or state consequences.
- Primary task, action, consequence, location, current state, selection scope, draft/publish state, or visual hierarchy is materially ambiguous.
- A material state, transition, error, recovery, permission, interruption, or partial-failure path is missing.
- Form questions lack necessity or users lose input during recoverable failure.
- Important professional data, comparison, or expert actions are hidden for cosmetic simplicity.
- Important data is misleading, distorted, or truncated without recovery.
- A critical accessibility issue is present.
- The design violates authoritative system sources without an approved deviation.
- The interface depends on invented behavior or impossible technical/data assumptions.
- An unavailable capability, hidden plugin behavior, external write, or publication is assumed without evidence/approval.
- The execution provider's own success report is the only acceptance evidence.
- Implementation must infer core interaction, content, responsive, or state decisions.

## Required evidence

- UI Design Decision or equivalent problem/rationale artifact
- Object/action/state model and task flow
- Behavior lenses, page/workflow classification, and Pattern Decision Record
- Conditional Form Task Flow Decision and/or Professional Interface Contract
- Screen/module design spec and intended perception order
- State and responsive matrix
- Design-system/component/token references and deviations
- Content/data examples, permissions, and technical constraints
- Adversarial critique and residual risks
- Capability Inventory, Design Execution Brief, provenance, and fallback when tools are used
- Validation plan and Design QA notes
- Rendered screenshots or inspectable implementation for final visual acceptance

## Verdict contract

- `PASS`: all applicable criteria are supported; no blockers; rendered evidence exists when final visual quality is claimed.
- `PASS_WITH_WARNINGS`: acceptance is supportable with explicit non-blocking residual risk or deferred evidence outside the current claim.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide, including visual acceptance without rendered evidence or execution claims without capability/source provenance.

A warning must never hide a blocker. A numeric score must never average away a critical failure. Missing evidence must never be converted into a clean pass.
