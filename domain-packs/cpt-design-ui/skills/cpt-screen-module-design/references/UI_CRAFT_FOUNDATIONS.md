# UI Craft Foundations

Reference ID: `cpt-ui-craft-foundations-v1`
Source structure: *Designing User Interfaces*, chapters 3-12, 20, 24-30.
Policy dependency: `UI_KNOWLEDGE_POLICY.md`.

## 1. UI craft as functional design

The visual interface is the perceivable and interactive expression of product behavior. UI quality is not decoration added after UX. It changes readability, comprehension, confidence, error rate, perceived quality, and the user's ability to act.

A strong interface must be:

- useful for the target task;
- understandable without unnecessary explanation;
- readable and operable in the actual context;
- visually ordered and internally consistent;
- restrained enough that content and action remain primary;
- detailed enough that states, feedback, and boundaries feel intentional;
- feasible to implement and maintain.

Visual polish is part of product quality, but it never compensates for broken behavior or weak product value.

## 2. Evidence model for visual decisions

Every material UI decision must trace to at least one of:

- user or task evidence;
- product objective or risk;
- domain model or information structure;
- design-system rule;
- platform/accessibility requirement;
- validated product pattern;
- explicit hypothesis with a validation plan.

"Looks cleaner," "feels premium," "more modern," and "users expect it" are not sufficient rationale until converted into observable criteria.

## 3. Perceptual organization

### Proximity

Distance communicates grouping. Elements that belong to one object or decision should usually be closer to one another than to adjacent groups.

Operational checks:

- spacing within a group is smaller than spacing between groups;
- labels are visually attached to their controls and values;
- actions are attached to the object they affect;
- repeated groups use the same spacing logic;
- responsive layouts preserve group identity.

### Similarity

Shared visual properties imply shared role or behavior. Differences create emphasis or state.

Use similarity consistently across:

- action hierarchy;
- component families;
- status and semantic color;
- icon style;
- text roles;
- selected, active, disabled, and destructive states.

Do not create accidental similarity between interactive and non-interactive elements.

### Closure

People can recognize simplified or incomplete forms when the overall shape remains clear. Use closure to reduce icon and illustration complexity, not to hide necessary affordance or state.

### Continuity and alignment

Aligned edges and predictable trajectories improve scanning. Break continuity only to create intentional emphasis.

Check:

- repeated content aligns to stable anchors;
- text and controls follow a predictable reading path;
- outliers are intentional and explainable;
- scrolling and carousel content signals continuation;
- motion preserves object continuity.

### Common fate

Elements moving together are perceived as related. Use this for grouped transitions, expansion, reordering, drag-and-drop, and list changes. Do not animate related elements in contradictory directions without reason.

### Figure and ground

The user must distinguish content, controls, containers, background, and temporary layers.

Possible mechanisms:

- tonal difference;
- spacing and containment;
- border;
- elevation;
- shadow;
- blur;
- scale;
- motion;
- occlusion.

No single mechanism is mandatory. The chosen mechanism must fit the design system and remain perceptible in all supported themes and states.

### Isolation and serial position

An intentionally distinct item can attract attention, and edge positions in a sequence may receive more notice. Apply only when the highlighted item truly deserves priority. Do not turn every action into an anomaly.

### Symmetry and asymmetry

Symmetry can create stability and quick comprehension. Asymmetry can express priority, movement, density, or brand character. Evaluate balance, reading order, and task clarity instead of enforcing symmetry.

## 4. Hierarchy of attention

Before composing a screen, define the intended perception sequence:

1. Where am I?
2. What is the current state or object?
3. What information matters now?
4. What is the likely next action?
5. What consequences, constraints, or secondary actions matter?

Map the sequence to visual mechanisms:

- position;
- scale;
- weight;
- contrast;
- whitespace;
- grouping;
- color;
- motion;
- progressive disclosure.

Use the smallest number of mechanisms necessary. Multiple competing accents reduce signal quality.

### Hierarchy test

An evaluator should be able to identify the location, current state, primary information, primary action, and main groups without reading every word.

## 5. Grid, spacing, and rhythm

A grid is a consistency and coordination system, not a decorative overlay.

### Establish the spatial contract

Define or discover:

- layout container behavior;
- columns and gutters where relevant;
- outer margins;
- spacing tokens;
- component padding scale;
- vertical rhythm;
- responsive breakpoints or container queries;
- density modes;
- optical-correction allowances.

Use the project's tokens. An 8-point or 10-point scale is a contextual starting point only.

### Hierarchical spacing

Use smaller increments inside components and larger increments between sections or modules. Spacing should communicate semantic structure before borders are added.

### Test the grid against real content

Validate with representative screen types:

- long text;
- tables and dense data;
- forms;
- media;
- charts;
- empty and error states;
- localization expansion;
- narrow and wide viewports.

A grid that works only for a showcase screen is not a product grid.

### Optical correction

Mathematical centering is not always perceptual centering. Icons, letterforms, asymmetric shapes, and mixed weights may need bounded optical adjustment. Record deviations and keep them systematic.

## 6. Density and complexity

Do not equate quality with whitespace. Determine density from:

- user expertise;
- task frequency;
- decision risk;
- information volatility;
- comparison needs;
- screen size and viewing distance;
- input method;
- cost of navigation;
- accessibility and zoom needs.

For professional tools, high density can improve performance when grouping, alignment, typography, and interaction hierarchy remain strong.

Reduce accidental complexity, not necessary domain complexity.

## 7. Screen and device context

Before designing, identify:

- device class and viewport range;
- pixel density only when relevant to assets;
- input methods: touch, pointer, keyboard, pen, remote, assistive technology;
- viewing distance;
- posture and one-handed reach;
- orientation and window resizing;
- platform conventions;
- environmental constraints such as glare, low contrast, movement, or intermittent connectivity.

Responsive design is not shrinking the desktop. Preserve task priority and relationships while changing layout, navigation, density, and interaction mechanics.

## 8. Object and surface construction

Treat interface objects as explicit boxes with:

- content;
- internal spacing;
- boundary or fill;
- external spacing;
- size constraints;
- alignment;
- state;
- interactive hit area;
- responsive behavior.

### Radius, border, fill, shadow, and blur

These are mechanisms, not quality rules.

Choose them to communicate:

- containment;
- hierarchy;
- interactivity;
- focus;
- selection;
- state;
- depth;
- brand character.

Keep their token use and geometry consistent. Avoid effects that compete with content or make boundaries ambiguous.

## 9. Typography

Typography carries hierarchy, tone, density, and interaction meaning.

### Build semantic roles

Define roles such as:

- display or page title;
- section heading;
- body;
- label;
- value;
- metadata;
- helper text;
- control label;
- code or tabular data.

Do not map the system to a fixed H1/H2/P/Span set. Use product semantics and tokens.

### Legibility checks

Evaluate:

- language and script coverage;
- character differentiation;
- x-height and cap-height;
- weight at the actual size;
- line height;
- line length;
- letter spacing;
- contrast;
- alignment;
- number formatting;
- tabular numerals where comparison matters;
- truncation and wrapping;
- zoom and reflow;
- rendering on target platforms.

Serif and sans-serif are context choices, not readability guarantees.

### Hierarchy and restraint

Use a limited, coherent type system. The exact number of families, weights, and sizes follows semantic need. Avoid style proliferation without a role.

## 10. Color and contrast

Color has four primary interface jobs:

1. identity and brand expression;
2. hierarchy and emphasis;
3. semantic state;
4. data differentiation.

### Semantic color

Define roles rather than hard-coded hues:

- background and surfaces;
- primary and secondary content;
- interactive accent;
- focus;
- success;
- warning;
- error;
- information;
- selected and disabled states.

Never communicate meaning with color alone.

### Palette construction

A coherent palette requires:

- enough tonal range for hierarchy;
- accessible foreground/background pairs;
- clear semantic state colors;
- support for themes;
- predictable behavior in data visualization;
- consistency with images and illustration;
- restraint in accent use.

Color-wheel schemes and 60/30/10 can generate options, but they do not prove quality.

### Contrast

Meet the applicable project accessibility target. Also inspect glare, dark mode, large text, disabled states, focus visibility, overlays, and low-quality displays.

Pure black and pure white are allowed when they satisfy the product's visual and accessibility requirements.

## 11. Visual style and restraint

Choose style from:

- product category and trust requirements;
- audience and context;
- brand;
- platform;
- information density;
- interaction model;
- accessibility;
- implementation cost and longevity.

Trends are references, not authority.

### Subtraction pass

Before finalizing:

1. Remove one decorative element.
2. Remove one redundant boundary.
3. Reduce one competing emphasis.
4. Merge one duplicated label or action where safe.
5. Verify that meaning, state, and affordance remain clear.

If removal improves clarity, keep it removed. If removal damages comprehension, restore it with rationale.

## 12. Motion and microinteraction

Motion should explain change, preserve continuity, provide feedback, or support orientation.

For every animation, define:

- trigger;
- affected object;
- start and end state;
- duration and easing;
- interruption behavior;
- reduced-motion alternative;
- performance constraint;
- functional reason.

Avoid decorative delay, excessive bounce, contradictory movement, and animation that hides state change.

## 13. Design as a tested hypothesis

A polished screen is not proof.

Define how the design will be evaluated through an appropriate combination of:

- expert critique;
- prototype walkthrough;
- usability testing;
- accessibility testing;
- analytics;
- task success and time;
- error and recovery observation;
- preference or trust measures when relevant;
- implementation review.

Match prototype fidelity to the learning question. Do not use high fidelity by default when a lower-fidelity artifact can test the uncertainty more efficiently.
