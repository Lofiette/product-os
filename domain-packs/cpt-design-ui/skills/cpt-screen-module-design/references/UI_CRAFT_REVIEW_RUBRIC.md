# UI Craft Review Rubric

Rubric ID: `cpt-ui-craft-review-v1`
Policy dependency: `UI_KNOWLEDGE_POLICY.md`.

## Purpose

Evaluate product-design quality as observable problem fit, interaction quality, visual craft, system coherence, and evidence. The rubric is suitable for self-critique, independent design review, human-versus-agent comparison, and future screenshot-based evaluation.

A numeric score supports diagnosis. It never overrides a blocker, missing evidence, or specialist gate.

## Required review packet

- task and product goal;
- target users, context, expertise, frequency, and risk;
- authoritative design-system and platform sources;
- object/flow/state model;
- alternatives and decision rationale;
- rendered evidence for representative states and breakpoints when visual acceptance is claimed;
- content and realistic data;
- known constraints, assumptions, and validation plan.

If rendered evidence is required but absent, return `INSUFFICIENT_EVIDENCE` for visual acceptance rather than guessing from a specification.

## Review sequence

1. Inspect the rendered result before reading the rationale where practical.
2. Perform a five-second scan: location, state, primary information, primary action, main groups.
3. Inspect without relying on color: hierarchy, grouping, boundaries, and affordances.
4. Walk the primary task and all material state transitions.
5. Stress the solution with novice, expert, error, empty, extreme-data, permission, localization, keyboard, zoom, and narrow/wide conditions as applicable.
6. Compare with design-system sources and approved references.
7. Run the subtraction pass and identify accidental complexity.
8. Read the rationale and verify that evidence supports the decisions.
9. Record blockers, major findings, minor findings, score, confidence, and unverified areas.

## Scoring scale

- `0 - ABSENT_OR_CONTRADICTORY`: the dimension is missing, fundamentally wrong, or contradicts the task.
- `1 - MAJOR_DEFECT`: material user harm, ambiguity, inconsistency, or rework is likely.
- `2 - ACCEPTABLE_BASELINE`: usable and supportable, but generic, brittle, or insufficiently refined.
- `3 - STRONG`: intentional, coherent, robust, and well supported.
- `4 - EXCEPTIONAL`: unusually clear, efficient, elegant, systematic, and resilient without unnecessary complexity.

## Dimensions

### D1. Problem and product fit

Does the solution address the actual user task and product outcome rather than merely arranging requirements?

Observe:

- explicit problem frame and success condition;
- evidence or hypothesis status;
- non-goals and trade-offs;
- no invented domain or system facts;
- solution scope matches the problem.

### D2. Object, action, and mental model clarity

Can the user understand what objects exist, what can be done, and what changes?

Observe:

- stable object identity;
- action-object mapping;
- visible consequence and scope;
- terminology matches user/domain language;
- no misleading controls or modes.

### D3. Task flow and efficiency

Does the flow minimize unnecessary decisions, navigation, repetition, and waiting while supporting expert use?

Observe:

- clear entry and completion;
- sensible defaults;
- progressive disclosure where useful;
- shortcut and bulk behavior for frequent work;
- preservation of context and user input;
- acceptable choice complexity.

### D4. State, feedback, error prevention, and recovery

Are system status and transitions complete and recoverable?

Observe:

- loading, empty, partial, success, error, stale, offline, permission, disabled, destructive, and interrupted states as applicable;
- immediate feedback;
- clear ownership of failure;
- retry, undo, cancel, and recovery;
- no ambiguous or impossible transitions.

### D5. Information architecture and findability

Is information grouped, labeled, navigable, searchable, and scalable?

Observe:

- user-oriented hierarchy;
- stable navigation and location cues;
- browse/search/filter/compare/resume support;
- role and permission effects;
- scalability and localization.

### D6. Hierarchy of attention

Does visual prominence match task priority and reading order?

Observe:

- location and current state are apparent;
- primary information/action are dominant without shouting;
- secondary content is available but not competing;
- emphasis uses a controlled set of mechanisms;
- hierarchy survives grayscale and reduced decoration.

### D7. Composition, grouping, alignment, and rhythm

Does the layout form coherent perceptual groups and a predictable scan path?

Observe:

- proximity reflects semantic grouping;
- shared anchors and intentional breaks;
- spacing tokens and vertical rhythm;
- balance rather than mandatory symmetry;
- optical correction where needed;
- robust behavior with real content.

### D8. Typography and readability

Does typography support hierarchy, comprehension, density, and language?

Observe:

- semantic roles and consistency;
- legibility at actual size and target conditions;
- line length, line height, weight, spacing, and alignment;
- number and data formatting;
- wrapping, truncation, localization, zoom, and reflow;
- no unsupported serif/sans-serif assumptions.

### D9. Color, contrast, and semantic signaling

Does color clarify identity, hierarchy, state, and data without becoming the only cue?

Observe:

- accessible foreground/background pairs;
- semantic color roles;
- focus, selection, disabled, and error distinction;
- theme behavior;
- accent restraint;
- no deterministic color-psychology rationale.

### D10. Affordance and control quality

Can users recognize interactive elements and operate them accurately?

Observe:

- control type matches behavior;
- target and focus areas;
- action hierarchy;
- icon-label clarity;
- hover/touch/keyboard parity;
- destructive and disabled behavior;
- visual style does not obscure affordance.

### D11. Density and expert performance

Does the interface provide the right information and control density for the task?

Observe:

- necessary complexity remains visible and structured;
- frequent actions are efficient;
- comparison and scanning are supported;
- novice guidance does not permanently slow experts;
- whitespace and chrome do not waste task-critical space;
- density modes are considered where relevant.

### D12. Content and microcopy

Does language clarify action, state, consequence, and recovery?

Observe:

- explicit labels;
- consistent terminology;
- realistic content and data;
- helpful errors and empty states;
- no dark patterns or shame;
- localization readiness.

### D13. Responsive and adaptive behavior

Does the solution preserve priority, relationships, and operability across target contexts?

Observe:

- layout adaptation rather than simple shrinkage;
- navigation transformation;
- content priority and reflow;
- input method and reach;
- orientation/window resizing;
- extreme content and zoom.

### D14. Design-system and systemic quality

Does the solution use the authoritative system and improve rather than fragment it?

Observe:

- governed components, tokens, and patterns;
- correct variants and states;
- justified deviations;
- reusable contribution when a gap is systemic;
- no local lookalikes or raw values without approval.

### D15. Accessibility and inclusive operation

Can representative users operate and understand the interface under the applicable target?

Observe:

- semantics and names;
- keyboard and focus;
- reading order and announcements;
- contrast and non-color cues;
- target size, zoom, reflow, and reduced motion;
- accessible error and recovery.

The specialist accessibility gate remains authoritative.

### D16. Restraint, polish, and implementation realism

Is the result detailed and refined without decoration or complexity that weakens the product?

Observe:

- subtraction pass completed;
- low-importance details are still intentional;
- effects support hierarchy or brand;
- performance and implementation constraints are plausible;
- no impossible interaction or data assumptions;
- handoff and verification are complete.

## Blocking conditions

Return `BLOCKED` when any applicable condition is present:

- the solution does not address the stated problem or invents critical facts;
- the primary task, action, consequence, or current state is materially ambiguous;
- a required state or recovery path is missing and can cause loss, error, or dead end;
- interaction and visual hierarchy contradict each other;
- a critical accessibility issue is present;
- a governed design-system rule is violated without an approved deviation;
- important data is misleading, truncated without recovery, or visually distorted;
- implementation must invent core behavior;
- a high-risk or destructive action lacks sufficient consequence and recovery design.

## Verdict guidance

- `PASS`: no blockers, all applicable dimensions score at least 2, weighted mean at least 3.0, and required evidence is present.
- `PASS_WITH_WARNINGS`: no blockers, no applicable dimension below 2 unless explicitly deferred outside current scope, and weighted mean at least 2.5.
- `BLOCKED`: any blocker or any critical dimension at 0-1 with material user/product impact.
- `INSUFFICIENT_EVIDENCE`: the reviewer cannot responsibly inspect the claimed quality level.

The thresholds are diagnostic defaults. Product-specific risk gates may be stricter.

## Default profile weights

### General product interface

- D1-D5: `1.2`
- D6-D10: `1.0`
- D11-D16: `1.0`

### Enterprise B2B / professional tool

- D1-D5: `1.2`
- D6-D10: `1.0`
- D11 density/expert performance: `1.5`
- D12-D16: `1.1`

### Data-dense analytics interface

- D1-D5: `1.2`
- D6 hierarchy: `1.2`
- D7 composition: `1.2`
- D8 typography: `1.2`
- D9 color/data semantics: `1.4`
- D11 density/expert performance: `1.5`
- D12-D16: `1.0`

### Design-system component

- D2 object/action clarity: `1.3`
- D4 state/recovery: `1.4`
- D7-D10: `1.2`
- D13 responsive: `1.2`
- D14 system quality: `1.6`
- D15 accessibility: `1.6`
- D16 implementation realism: `1.3`

## Adversarial critique prompt

Assume the design is competent but mediocre. Find:

- unnecessary UI;
- false simplicity;
- hidden complexity;
- weak defaults;
- ambiguous hierarchy;
- competing emphasis;
- needless modes;
- expert inefficiency;
- novice traps;
- accidental state loss;
- inconsistent patterns;
- premature abstraction;
- visual noise;
- weak feedback;
- irreversible action risk;
- unsupported rationale;
- decorative choices masquerading as usability.

For every finding, state evidence, user impact, severity, smallest systemic fix, and verification.

## Review output contract

1. Scope, profile, evidence, and missing evidence.
2. Five-second scan result.
3. Dimension score table with concise evidence.
4. Blockers, major findings, and minor findings.
5. Subtraction opportunities.
6. Recommendation and smallest systemic fix.
7. Verdict, confidence, residual risk, and unverified areas.
