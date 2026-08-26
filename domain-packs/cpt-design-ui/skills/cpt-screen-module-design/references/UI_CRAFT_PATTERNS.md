# UI Craft Patterns

Reference ID: `cpt-ui-craft-patterns-v1`
Source structure: *Designing User Interfaces*, chapters 13-23 and relevant audit/handoff chapters.
Policy dependency: `UI_KNOWLEDGE_POLICY.md`.

Use only the sections relevant to the current interface. Project design-system patterns override these defaults.

## 1. Icons

### Invariant

An icon must be legible, stylistically coherent, and understandable in context. Icon meaning is not universal.

### Procedure

1. Determine whether an icon is necessary or whether text is clearer.
2. Prefer an existing governed icon.
3. Check metaphor against audience, domain, and platform convention.
4. Define size, optical box, stroke/fill, corner treatment, and state behavior.
5. Add a label when meaning or consequence is not obvious.
6. Verify at actual size and across themes.

### Critical checks

- consistent stroke weight or fill logic;
- consistent corner and terminal treatment;
- bounded level of detail;
- adequate hit area independent of glyph size;
- no reliance on color alone for state;
- no ambiguous destructive or security metaphors;
- optical alignment with adjacent text and controls.

### Contextual heuristic

Labels may be omitted for deeply established icons in a familiar location and low-risk context. Treat this as a hypothesis, not a universal list.

## 2. Buttons, links, and action hierarchy

### Invariant

Interactive controls must look actionable, communicate consequence, and form a clear hierarchy.

### Action model

Classify actions by:

- primary task contribution;
- frequency;
- reversibility;
- risk;
- scope of effect;
- current state;
- permission;
- latency.

### Procedure

1. Name the action with an explicit verb and object where useful.
2. Choose control type from behavior, not visual preference.
3. Define primary, secondary, tertiary, destructive, disabled, loading, success, and error behavior.
4. Ensure target size and focus treatment meet project requirements.
5. Separate destructive actions from routine actions.
6. Verify icon-label relationship and localization expansion.

### Critical checks

- one dominant action per decision context unless the task genuinely has peers;
- link versus button semantics match behavior;
- disabled state is not used as the only explanation;
- loading does not permit duplicate submission;
- destructive action includes consequence and recovery where possible;
- hover is never the only access to meaning;
- visual prominence matches actual priority.

Shadows, gradients, arrows, and radius can support affordance but do not prove it.

## 3. Cards and containers

### Invariant

A container is justified when it creates a meaningful object boundary, interaction scope, comparison unit, or responsive grouping.

### Procedure

1. Identify the object represented by the container.
2. Define its identity, key value, status, actions, and drill-down behavior.
3. Establish internal hierarchy before decoration.
4. Choose boundary mechanism from spacing, tone, border, or elevation.
5. Define repeated, selected, hover, focus, disabled, loading, and error states.
6. Check list/grid behavior and responsive reflow.

### Critical checks

- the card is not a wrapper around unrelated content;
- the whole card and inner actions do not create conflicting click targets;
- repeated cards align comparable information;
- secondary decoration does not overpower the object;
- truncated content has a deliberate strategy;
- selected and focused states remain distinct.

Cards do not inherently require shadows or rounded corners.

## 4. Tables and data-dense views

### Invariant

Data interfaces must support scanning, comparison, action, and interpretation without distorting the data.

### Procedure

1. Identify user questions and comparison tasks.
2. Define row entity, column semantics, units, precision, null behavior, and update timing.
3. Prioritize columns and actions by role and frequency.
4. Define sorting, filtering, search, pagination/virtualization, selection, bulk actions, and column control.
5. Align data according to type and comparison needs.
6. Design empty, loading, partial, stale, error, permission, and extreme-value states.
7. Define responsive behavior: reflow, priority columns, alternate view, or horizontal scroll.

### Critical checks

- units and aggregation are explicit;
- numbers are aligned for comparison;
- sorting state and scope are visible;
- sticky headers/columns do not obscure content;
- row and bulk actions are discoverable;
- selection survives or intentionally resets across filtering/pagination;
- dense spacing still supports target size and readability;
- charts do not smooth, truncate, or decorate data in misleading ways.

Avoid turning a professional table into disconnected cards merely to make it look spacious.

## 5. Forms

### Invariant

A form should help the user understand what is required, enter valid data efficiently, recover from errors, and trust the result.

### Procedure

1. Confirm whether every field is necessary and who owns the data.
2. Group fields by user mental model and task sequence.
3. Choose control by data type, option visibility, comparison need, independence, and frequency.
4. Define labels, instructions, examples, defaults, validation timing, dependencies, and permissions.
5. Design keyboard, focus, autofill, paste, format, localization, and assistive-technology behavior.
6. Specify all states and submission behavior.
7. Decide between one page and multiple steps based on task structure, not field count alone.

### Critical checks

- persistent labels remain available after entry;
- placeholder is not the only label or instruction;
- field width and grouping communicate expected input without reducing accessibility;
- errors identify the problem, location, and recovery;
- validation does not interrupt typing unnecessarily;
- required/optional logic is explicit;
- dependent fields and recalculations are predictable;
- save, autosave, cancel, and unsaved-change behavior are defined;
- summary and review are available for high-risk submissions.

### Control heuristics

- Radio buttons can improve visibility and comparison for a small set of mutually exclusive options.
- Dropdowns are useful when options are numerous or space is constrained, but searchable selection may be better for long lists.
- Switches communicate immediate independent state changes. They are not a general replacement for checkboxes.
- Native platform controls are candidates when they improve familiarity, accessibility, or input efficiency.

No fixed option count is universally binding.

## 6. Dialogs, popups, overlays, action sheets, and tooltips

### Invariant

Temporary layers must preserve context, focus, consequence, and a reliable exit path.

### Procedure

1. Decide whether interruption is necessary.
2. Choose the smallest layer that supports the task.
3. Define focus entry, focus trap where applicable, reading order, and focus return.
4. Define dismissal rules based on risk and unsaved work.
5. Keep action hierarchy explicit and labels consequential.
6. Design responsive transformation, such as dialog to sheet or full-screen flow.
7. Specify nested-layer policy and prevent uncontrolled stacking.

### Critical checks

- background is inert when required;
- context remains understandable;
- accidental outside click cannot destroy important work;
- Escape/back behavior is defined;
- destructive confirmations state the object and consequence;
- tooltips do not contain essential information that touch, keyboard, or screen-reader users cannot access;
- automatic marketing popups do not interrupt without product justification;
- overlays preserve adequate contrast without relying on a fixed opacity recipe.

## 7. Navigation

### Invariant

Navigation must make location, available destinations, and return paths understandable while supporting task frequency.

### Procedure

1. Model destinations, objects, hierarchy, cross-links, and permission effects.
2. Separate global, local, contextual, and in-flow navigation.
3. Rank destinations by frequency and importance.
4. Choose pattern based on viewport, hierarchy depth, number of destinations, labels, and role variation.
5. Define active, current, expanded, focus, hover, disabled, and permission states.
6. Test deep links, browser history/back, interrupted flows, and responsive transitions.

### Critical checks

- current location is visible;
- labels use user/domain language;
- icons do not replace unclear labels;
- hidden navigation does not conceal frequent destinations without reason;
- scrollable tabs clearly signal continuation;
- navigation does not reset user work unexpectedly;
- nested depth remains comprehensible;
- keyboard and screen-reader order match the visual structure.

Bottom tabs, sidebars, top bars, drawers, breadcrumbs, and contextual navigation are alternatives, not a universal ranking.

## 8. Motion and microinteractions

### Invariant

Motion must support feedback, causality, continuity, or orientation.

### Procedure

1. State the user-visible reason for motion.
2. Map object identity between states.
3. Choose duration/easing from distance, importance, and platform convention.
4. Make feedback immediate even if processing continues.
5. Define interruption, cancellation, and reduced-motion behavior.
6. Test at realistic device performance.

### Critical checks

- motion does not delay task completion;
- repeated motion does not create fatigue;
- progress reflects actual or clearly indeterminate status;
- success animation does not hide the resulting state;
- bounce and overshoot are restrained and contextual;
- loading, saving, and synchronization states are distinguishable.

Fixed easing and overshoot formulas are starter presets only.

## 9. Photography and illustration

### Invariant

Visual media must support content, brand, comprehension, or emotional context without reducing readability or truthfulness.

### Procedure

1. Define the media's job.
2. Choose authentic content and appropriate subject/crop.
3. Check focal point, text safe areas, responsive cropping, localization, and contrast.
4. Apply color treatment and overlays only as needed.
5. Provide alt text or decorative semantics.
6. Maintain a coherent illustration or photography system.

### Critical checks

- no misleading stock imagery or distorted data meaning;
- faces and gaze are composition tools, not guaranteed conversion mechanisms;
- text remains readable across crops and themes;
- important image content is not lost on narrow screens;
- media does not become a substitute for an empty-state explanation or actionable content;
- asset size and performance are bounded.

## 10. Interface language

### Invariant

Language is part of the interaction model. It must clarify state, action, consequence, and recovery.

### Procedure

1. Use the product glossary and domain language.
2. Prefer explicit action labels over generic labels such as "OK" or "Next" when consequence matters.
3. Write errors with cause, affected object, and recovery.
4. Keep labels stable across screens and channels.
5. Test truncation, pluralization, variables, localization, and tone.
6. Avoid dark patterns and shame-based negative actions.

### Critical checks

- title and action agree on the task;
- button label predicts the result;
- empty state explains why it is empty and what can be done;
- confirmation does not overclaim success;
- destructive wording is unambiguous;
- helper text is available before the error when it can prevent the error.

## 11. Design system, audit, handoff, and implementation QA

### Invariant

A design is complete only when its system relationship, implementation contract, and acceptance evidence are explicit.

### Procedure

1. Establish source authority.
2. Reuse existing components and tokens before proposing variation.
3. Record deviations and systemic impact.
4. Define anatomy, variants, states, content, behavior, responsive rules, and accessibility.
5. Provide realistic data and edge cases.
6. Review the rendered implementation on actual target conditions.
7. Feed implementation discoveries back into the design system or decision record.

### Audit dimensions

- component and token consistency;
- alignment and spacing;
- typography roles;
- color and semantic state;
- interactive target sizes;
- state completeness;
- responsive behavior;
- accessibility;
- content realism;
- visual and behavioral deltas from the approved design.

Handoff tools and implementation technologies are project choices. The required outcome is unambiguous shared evidence, not a particular tool.

## 12. Prototyping

### Invariant

Prototype fidelity must match the uncertainty being tested.

Choose fidelity based on whether the question concerns:

- concept and value;
- information structure;
- flow and navigation;
- interaction behavior;
- visual hierarchy and trust;
- motion;
- technical feasibility;
- realistic data and system integration.

A prototype should expose the relevant behavior without creating unnecessary production cost or false confidence.
