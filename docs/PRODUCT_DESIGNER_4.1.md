# Product Designer 4.1

Patch ID: `product-designer-4.1`
Base package: `Product OS 4.0.0`
Status: integrated and deterministically validated; live-model, external-plugin, design-tool, and screenshot quality remain uncertified.

## Goal

Extend the Product Designer from product reasoning plus UI craft into a portable design operating layer with:

- human-behavior lenses and explicit interaction-pattern composition;
- dedicated form and long-process design;
- professional data, table, dashboard, bulk, keyboard, and partial-failure design;
- vendor-neutral execution orchestration for audits, visual directions, prototypes, image-to-code, visual QA, export, and preview publishing;
- an optional bridge to OpenAI Product Design when that plugin is visibly available in Codex;
- deterministic knowledge validation and expanded design-intelligence cases.

The Product Designer remains the accountable owner of the design decision. Tools and plugins are execution adapters.

## Source basis

### Visual craft

Michał Malewicz and Diana Malewicz, *Designing User Interfaces*, version 2.0. Product OS 4.0 transformed its visual craft into an operational canon and filtered contextual, dated, and unsupported claims.

### Interaction intelligence

Jenifer Tidwell, Charles Brewer, and Aynne Valencia, *Designing Interfaces*, third edition. 4.1 transforms:

- behavior patterns such as Safe Exploration, Satisficing, Deferred Choices, Habituation, Spatial Memory, Streamlined Repetition, and Keyboard Only;
- page types such as overview, focus, creation, and action;
- IA, navigation, workspace, list, command, recovery, and data-exploration patterns;
- the source pattern structure: what/problem, when/context, why/forces, how/procedure, and examples.

Historical screenshots and platform-specific examples are not treated as current visual authority.

### Form and inclusive interaction intelligence

Adam Silver, *Form Design Patterns* (2018). 4.1 transforms:

- the Question Protocol;
- problem-oriented rather than rigid rule-oriented form design;
- native-first and progressive-enhancement reasoning;
- labels, hints, input semantics, defaults, validation, errors, focus, announcements, and recovery;
- one-thing-per-page with contextual caveats;
- search, filters, upload, repeated entry, long processes, task lists, save/resume, and multi-actor work.

The source's jQuery, browser-version workarounds, historical ARIA implementations, exact conversion figures, and dated security/platform recipes are not current implementation authority.

## New canonical skills

### `cpt-interaction-pattern-selection`

Produces a Pattern Decision Record from:

- behavior lenses;
- page/workflow classification;
- contextual forces;
- candidate pattern compositions;
- structure, navigation, command, recovery, and re-entry decisions;
- evidence and falsification.

Knowledge assets:

- `INTERACTION_PATTERN_POLICY.md`
- `BEHAVIOR_LENSES.yaml` with 12 lenses
- three selective catalogs with 44 interaction patterns
- `PATTERN_DECISION_RECORD.md`

### `cpt-form-task-flow-design`

Produces a Form Task Flow Decision from:

- Question Protocol;
- flow mode selection;
- field and native/custom control semantics;
- validation, error, focus, announcement, and preservation behavior;
- search/filter/upload/repetition;
- review, confirmation, second-time use, save/resume, and long/multi-actor processes.

Knowledge assets:

- `FORM_KNOWLEDGE_POLICY.md`
- `FORM_FLOW_MODE_MATRIX.yaml` with 8 modes
- `FORM_PATTERN_CATALOG.yaml` with 24 patterns
- `FORM_ACCESSIBILITY_CONTRACT.md`
- `FORM_TASK_FLOW_DECISION.md`

### `cpt-professional-data-interface-design`

Produces a Professional Interface Contract for:

- dense lists and tables;
- dashboards and monitoring;
- bulk actions and selection scope;
- keyboard and expert acceleration;
- linked data views;
- audit, history, undo/cancel, partial success, and recovery;
- novice-to-expert progression.

Knowledge assets:

- `PROFESSIONAL_INTERFACE_POLICY.md`
- `PROFESSIONAL_TASK_MATRIX.yaml` with 7 workflow classes
- `PROFESSIONAL_REVIEW_CHECKLIST.md`

### `cpt-design-execution-orchestration`

Produces a Capability Inventory, Design Execution Brief, staged plan, and Execution Evidence Packet for:

- live URL and screenshot inspection;
- research synthesis;
- visual directions;
- interactive prototypes;
- responsive frontend and image-to-code;
- visual-diff QA;
- design export, annotations, and hosted previews.

It uses a capability model rather than a hard-coded provider. It includes:

- generic host-agnostic adapter;
- optional OpenAI Product Design adapter;
- adapter schema;
- evidence and approval contracts.

## OpenAI Product Design bridge

The adapter maps only skills that are visibly observed in the current runtime, including the user-observed names:

- Get Context;
- Research;
- Ideate;
- Audit;
- Design QA;
- Image To Code.

Rules:

1. The plugin is optional and Codex-specific.
2. Installation does not prove enablement or availability.
3. Hidden or undocumented skills are never assumed.
4. CPT owns problem framing, pattern selection, visual contract, states, and acceptance.
5. Plugin QA is supporting evidence, followed by CPT gates and independent review.
6. Every capability has a generic fallback or an explicit statement of quality loss.

## Product Designer method changes

The role now follows:

1. Frame the problem.
2. Reconstruct the domain model.
3. Classify human behavior, page type, and workflow.
4. Select and compose patterns.
5. Prioritize information and action.
6. Establish the visual craft contract.
7. Define the target artifact and execution lane.
8. Generate materially different alternatives.
9. Compose and specify.
10. Complete and stress states.
11. Run adversarial critique.
12. Execute, validate, and hand off.

## Quality-gate changes

The Product Design Quality Gate now blocks:

- pattern copying without contextual fit;
- unnecessary or premature form questions;
- lost input, incomplete validation/focus/recovery, or misleading custom controls;
- professional interfaces that remove comparison or expert actions for cosmetic simplicity;
- ambiguous selection scope, draft/publish, or partial-success semantics;
- assumed tools, hidden plugin behavior, unapproved external writes, or provider self-QA as the only verdict.

## Evaluation expansion

Design Intelligence grows from 12 to 20 cases. New cases cover:

- multi-workspace pattern composition;
- form reduction through the Question Protocol;
- accessible server-validation recovery;
- long multi-actor regulated processes;
- linked data investigation;
- portable execution without a vendor plugin;
- optional OpenAI Product Design bridge;
- image-to-code fidelity and uncertainty.

## Universality boundary

The environment continues to work without Codex plugins, external services, design tools, image generation, browser automation, or hosting. Missing execution capability reduces the available artifact, not the honesty of the result. The fallback is an implementation-ready decision and handoff with `INSUFFICIENT_EVIDENCE` for claims that require rendering or external inspection.

## Deterministic validation snapshot

Validated on 2026-08-20 against the complete patched package:

- Product Designer vNext2 knowledge: **PASS** with 12 behavior lenses, 44 interaction patterns, 8 form modes, 24 form patterns, 7 professional workflow classes, and 2 execution adapters.
- Active skill structure and migration: **49 skills**, **95/95 legacy mappings**, **4 explicit greenfield skills**, **6 plugins**.
- Skill trigger proxy: **147/147**.
- Logical expertise model: **50 roles**, **25 gates**, **14 routing profiles**.
- Role routing proxy: **164/164**.
- Design Intelligence structure: **16 dimensions**, **20 cases**.
- Behavioral and migration tests: **116/116**.
- Product Knowledge lifecycle: **11/11**.
- Enforcement policy: **5/5**.
- Orchestration policy and integration: **34/34** and **16/16**.
- Offline executable evaluation: **21/21**, average reference score **100**, baseline regressions **0**, mutation detection **4/4**.
- Release plane: **BETA_READY**, 33 trial tracks, 9 release gates.
- Skill discovery metadata: `cpt-design-ui` **3450 chars**; `ui-implementation` profile **6554 chars**, below the 7000-character profile limit.

These results certify package structure, deterministic behavior, routing, migration, evaluation mechanics, and portability contracts. They do not certify the judgment of every live model, a specific OpenAI Product Design plugin release, external design-tool integration, or rendered visual quality.
