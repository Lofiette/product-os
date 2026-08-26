---
name: cpt-screen-module-design
description: Use to create or redesign screens, flows, modules, or prototypes with product reasoning, patterns, UI craft, states, execution, and handoff.
---

# CPT Screen Module Design

## Use when

- The task requires a new or redesigned product interface.
- A module must be designed for later implementation or built as an inspectable prototype.
- Requirements or evidence need to become a coherent interaction and visual solution.
- No design system exists and a minimal consistent prototype contract is needed.

## Do not use when

- The task is visual QA of an already implemented screen with no design decision remaining.
- Only information architecture is changing and a screen solution is intentionally deferred.
- The implementation spec is complete, approved, and no product-design judgment is requested.

## Required inputs

- User and product goals.
- Target roles, context, expertise, frequency, risk, and environment.
- Area/flow knowledge and research evidence.
- Domain objects, data shape, permissions, selection/action scope, and known states.
- Design recon, authoritative design-system sources, and platform constraints.
- Content, API/technical boundaries, and validation needs.
- Reference/taste evidence when a material visual direction remains open.
- Target artifact and available execution capabilities when build/audit/prototype work is requested.

## UI craft references

For material interface design:

1. Read `references/UI_KNOWLEDGE_POLICY.md`.
2. Read `references/UI_CRAFT_FOUNDATIONS.md`.
3. Read only the relevant sections of `references/UI_CRAFT_PATTERNS.md`.
4. Before final recommendation, use `references/UI_CRAFT_REVIEW_RUBRIC.md`.
5. Structure the final artifact with `references/UI_DESIGN_DECISION_TEMPLATE.md`.

For a bounded micro change governed by an authoritative component or pattern, load only the policy and relevant targeted section.

## Method

### 1. Frame

Define the actual user task, product outcome, entry context, success condition, scope, non-goals, evidence, assumptions, and constraints. Do not start with a requested screen if the request may encode the wrong solution.

### 2. Model

Map domain objects, relationships, actions, permissions, data ownership, lifecycle, navigation, selection, and state transitions. Separate domain truth from UI representation.

### 3. Classify and select patterns

Use `cpt-interaction-pattern-selection` for material decisions. Classify page/workflow type, behavior lenses, and contextual forces, then select a pattern composition for structure, navigation, commands, recovery, and re-entry.

Use `cpt-form-task-flow-design` when forms, search, filters, upload, repeated entry, validation, or long processes are material. Use `cpt-professional-data-interface-design` for dense tables/lists, dashboards, bulk work, linked data, or expert operation.

### 4. Prioritize

Determine what the user must notice, understand, decide, and do. Define primary information, primary action, comparison fields, secondary actions, risk/consequence communication, and expert accelerators.

### 5. Establish the visual contract

Discover or define:

- intended perception order;
- grouping and layout model;
- grid, spacing scale, and density;
- typography roles;
- color and semantic emphasis;
- surfaces and boundaries;
- iconography, media, and motion;
- responsive and input-method behavior.

Use governed system sources. When no system exists, create the smallest local contract that can remain consistent.

### 6. Choose the execution lane

If the task needs a live-source audit, visual directions, interactive prototype, coded frontend, image-to-code, visual diff, design export, or hosted preview, use `cpt-design-execution-orchestration` to inventory actual capabilities, select a portable adapter/fallback, and record approvals.

Do not make a vendor plugin a required dependency. An observed OpenAI Product Design plugin may be used as an optional Codex adapter under CPT ownership and gates.

### 7. Explore distinct models

Generate materially different alternatives, not cosmetic variants. Compare problem fit, pattern fit, task efficiency, expert throughput, error resistance, evidence, design-system fit, accessibility, scalability, execution feasibility, and implementation cost.

### 8. Compose and specify

Define screen/module anatomy, component tree, content, interactions, responsive behavior, and realistic data. Include selected pattern IDs, flow mode where applicable, and selection/action semantics for data-heavy interfaces.

### 9. Complete states

Use `cpt-interaction-state-model` to cover applicable initial, loading, empty, partial, populated, success, error, stale, offline, permission, disabled, destructive, interrupted, draft, saving, queued, published, conflict, and responsive states, including transitions and recovery.

### 10. Stress the design

Test the solution against:

- novice, expert, first-time, and second-time use;
- high-frequency and repeated work;
- error, interruption, branch change, and re-entry;
- extreme, missing, stale, conflicting, or localized content;
- permissions, roles, selection scope, and partial success;
- keyboard, touch, pointer, zoom, and assistive technology;
- narrow, wide, resized, and multi-workspace contexts;
- implementation, rendering, network, and performance constraints.

### 11. Adversarial critique

Assume the solution is competent but mediocre. Use the review rubric to find unnecessary UI, copied pattern logic, false simplicity, ambiguous hierarchy, weak defaults, premature questions, expert inefficiency, novice traps, hidden state loss, inconsistent controls, vendor lock-in, accidental complexity, and unsupported rationale.

Change the design or explicitly accept the trade-off with evidence.

### 12. Decide, execute, and verify

Produce the selected direction, pattern composition, rationale, visual contract, state/responsive matrix, system relationship, accessibility/content requirements, residual risks, validation plan, and implementation acceptance evidence.

When execution occurs, attach the Capability Inventory, Design Execution Brief, artifacts, provenance, comparisons, limitations, and approval/rollback record.

A polished screen is not proof. Define how the decision could be falsified. A generated artifact and its provider's own QA do not replace independent acceptance.

## Output contract

Produce a compact but complete `UI Design Decision` containing:

- problem frame, evidence, assumptions, and confidence;
- object/action/state model;
- behavior lenses, page/workflow classification, and pattern composition;
- alternatives and selection criteria;
- screen/module anatomy and component tree;
- visual contract and intended perception order;
- conditional form/professional-interface contract;
- state and responsive matrix;
- content, accessibility, data, permission, and technical constraints;
- capability inventory and execution lane when applicable;
- adversarial critique and changes made;
- validation, gates, handoff criteria, falsification, and stop condition.

## Evidence standard

- Product and behavior claims must trace to evidence or explicit hypothesis status.
- Pattern names and source screenshots are not proof of fit.
- Visual decisions must trace to the design system, project criteria, source-derived invariant, or explicit testable hypothesis.
- Numeric UI recipes are contextual defaults unless the project makes them authoritative.
- Current standards and platform behavior must come from current project sources or separate research.
- Execution availability must be observed in the runtime; missing capabilities must not be imagined.

## Stop and escalate

- Product outcome, object model, page/workflow type, or key behavior is unresolved.
- Required evidence is contradictory or missing for a consequential decision.
- A component or pattern decision changes product/design-system scope without an owner.
- Form, selection, permission, metric, draft/publish, or partial-success semantics are undefined.
- Required execution capability, source, approval, or rendering evidence is unavailable.

## Failure modes to avoid

- Starting from the requested screen.
- Producing cosmetic alternatives.
- Copying a named pattern or visual reference.
- Treating form design as field arrangement.
- Cardifying professional data and losing comparison.
- Hiding expert actions for visual cleanliness.
- Letting an execution provider silently change the design decision.
- Claiming visual PASS from text or self-generated QA alone.
