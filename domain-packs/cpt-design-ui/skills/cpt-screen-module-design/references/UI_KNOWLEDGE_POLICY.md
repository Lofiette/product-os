# UI Knowledge Policy

Policy ID: `cpt-ui-knowledge-policy-v1`
Primary source: Michał Malewicz and Diana Malewicz, *Designing User Interfaces*, version 2.0, 419 pages.
Scope: Product Designer and Visual Design Director reasoning, screen/module design, visual critique, and design-quality evaluation.

## Purpose

This policy converts a human-oriented UI design book into bounded operational knowledge. It preserves the source's terminology, chapter structure, practical craft orientation, and emphasis on precision while preventing contextual recipes, dated technology, unsupported causal claims, or stylistic preferences from becoming universal rules.

The source remains a reference, not a governing design system. Project evidence, current platform guidance, product constraints, accessibility requirements, and the authoritative design system take precedence.

## Source authority order

Use the first applicable source in this order:

1. Verified user and product evidence.
2. Approved product strategy, requirements, and domain constraints.
3. Authoritative design-system components, patterns, tokens, and content rules.
4. Current platform and accessibility requirements supplied by the project.
5. This UI craft canon.
6. Contextual heuristics from the source book.
7. Historical examples and style references.

Never override a higher-authority source merely because the book offers a familiar recipe.

## Knowledge classes

### `CANONICAL_INVARIANT`

A durable quality principle that should influence most interface work. Examples include explicit hierarchy, perceptual grouping, readable typography, state completeness, consistent component anatomy, and visible interaction feedback.

Canonical invariants are still subject to product context. They define an outcome, not a mandatory visual technique.

### `CONTEXTUAL_HEURISTIC`

A useful starting point whose applicability depends on audience, task, device, expertise, frequency, risk, density, brand, and design-system constraints. Numeric defaults belong here unless they are supplied by an authoritative project source.

A heuristic must be expressed as:

- intended outcome;
- conditions where it is likely useful;
- conditions where it may fail;
- evidence needed to accept it;
- alternative mechanisms.

### `PROJECT_AUTHORITY`

A project-specific component, token, pattern, guideline, or validated decision. This class overrides the general book-derived canon within its approved scope.

### `HISTORICAL_CONTEXT`

A dated tool, platform component, screen resolution, design trend, asset format workflow, or technology-specific recommendation. Historical context may explain why a pattern exists but must not govern a current solution without fresh project evidence.

### `QUARANTINED_CLAIM`

A causal, psychological, demographic, conversion, performance, or universal quality claim that lacks sufficient provenance in the supplied source. It may be stored as an unverified hypothesis, but it must not justify a design decision or gate verdict.

## Interpretation rules

1. Extract the invariant before the recipe.
   - Example: replace "cards should cast a shadow" with "layer and container boundaries must be perceivable." Shadow remains one possible mechanism.
2. Treat numbers as defaults, not truth.
   - Grid steps, target sizes, line lengths, opacity values, tab counts, and form widths must defer to the project system and current platform constraints.
3. Separate observation from explanation.
   - A source may correctly notice an effect while offering an uncertain causal story. Preserve the observation as a hypothesis and discard unsupported causality.
4. Do not convert correlation into conversion claims.
   - Claims that a shadow, color, inner effect, or visual style increases conversion require project evidence before use.
5. Do not infer user psychology from color alone.
   - Color may communicate semantics through learned conventions, culture, brand, context, and contrast. It does not deterministically create a specific emotion or action.
6. Do not use style as evidence.
   - "Modern," "premium," "friendly," or "serious" must be translated into observable composition, typography, density, material, motion, content, and interaction criteria.
7. Prefer mechanisms that survive style changes.
   - Hierarchy, grouping, reading order, affordance, feedback, task efficiency, and error resistance matter more than current decoration.
8. Apply accessibility as a design constraint, not a final checklist.
9. Preserve expert efficiency in professional products.
   - Simplicity does not mean removing useful information or actions. It means reducing accidental complexity and making necessary complexity legible.
10. Record uncertainty.
    - When evidence is missing, label the decision as a hypothesis and define validation.

## Accepted filtering decisions

The following decisions are approved for this Product Designer implementation.

### Quarantined or rewritten

- Miller's `7 +/- 2` is not a navigation or option-count limit. Use choice complexity, grouping, search, familiarity, expertise, and task cost instead.
- Golden Ratio formulas are optional generators, not objective laws of beauty, typography, spacing, or color balance.
- Symmetry is one means of order. Intentional asymmetry is allowed and often necessary for hierarchy.
- F-pattern and Z-pattern are observations from specific layouts, not universal templates.
- Deterministic color psychology, fixed color-to-industry rules, and unverified claims such as "90% of liking comes from color" are quarantined.
- Demographic claims about color channels and fixed color-vision percentages are not operational design knowledge.
- Serif versus sans-serif and named-font prohibitions are replaced by legibility, language, rendering, brand, and task criteria.
- Pure black is not prohibited. Contrast, display behavior, theme, visual language, and accessibility determine its use.
- Rounded corners do not automatically make a product friendly, and sharp corners do not automatically make it serious.
- Gaze direction in photography is a possible attention hypothesis, not a universal marketing rule.
- Claims that inner shadows improve conversion, flat design is always a fixed percentage slower, or shadows inherently make controls more clickable are quarantined unless verified in context.
- CSS is not reduced to H1, H2, P, and Span, and it is not treated as "not code."
- Design-system governance is not restricted to developer-only edits, code-only documentation, or date-only versioning.
- High-fidelity prototypes are not universally preferred. Fidelity follows the learning question.

### Contextual heuristics

- Touch target sizes, mobile type sizes, line lengths, grid scales, navigation counts, tab counts, form widths, step thresholds, dropdown-to-radio thresholds, modal dismissal behavior, shadow opacity, overlay opacity, and animation curves remain starting points only.
- One-column forms are a safe default for simple linear flows. Dense professional workflows may need structured multi-column layouts.
- Bottom navigation is a candidate for frequent mobile destinations, not a default for every product.
- Icon labels may be omitted only when meaning is established in the actual context and error cost is low.
- A limited type system is preferred, but the number of styles follows semantic roles and product needs.
- The aesthetic-usability effect remains a useful principle, but polish never substitutes for task success or reliability.

### Historical context only

- 2019 device resolutions and platform-specific component examples.
- Tool references such as Sketch v60, InVision Inspect, Avocode, and version-specific handoff workflows.
- Neumorphism and "Modern Design" as current trends.
- Fixed asset export recipes such as mandatory `@2x` PNG and JPG-first photography.
- React/CSS as universal design-system implementation choices.
- The book's specific team composition as the only valid product-design or design-system model.

## Operational decision test

Before applying a source-derived rule, answer:

1. What outcome is the rule trying to create?
2. What user, task, platform, density, expertise, frequency, and risk conditions apply?
3. Does the project design system already define the mechanism?
4. Is the claim an invariant, heuristic, historical example, or quarantined hypothesis?
5. What alternative mechanisms could create the same outcome?
6. What rendered or behavioral evidence would show that the choice works?
7. What would falsify the decision?

If these questions cannot be answered, do not present the rule as a design rationale.

## Loading policy

- For any material screen/module design task, load this policy and `UI_CRAFT_FOUNDATIONS.md`.
- Load only the relevant sections of `UI_CRAFT_PATTERNS.md` for the controls and surfaces being designed.
- Before final recommendation or visual acceptance, load `UI_CRAFT_REVIEW_RUBRIC.md`.
- Use `UI_DESIGN_DECISION_TEMPLATE.md` for the final design artifact.
- For a micro change with an authoritative design-system pattern, avoid loading unrelated chapters.

## Provenance boundary

The derived canon summarizes and operationalizes the supplied book. It does not reproduce the book and does not claim external scientific verification. Items requiring current standards, platform behavior, or empirical confirmation must be supplied by the project or researched separately.
