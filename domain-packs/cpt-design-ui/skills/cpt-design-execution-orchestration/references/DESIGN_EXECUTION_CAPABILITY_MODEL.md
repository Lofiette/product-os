# Design Execution Capability Model

Model ID: `cpt-design-execution-capabilities-v1`

The execution plane is capability-based, not vendor-based. A host may expose capabilities through built-in tools, plugins, skills, MCP servers, browser automation, image generation, design tools, code execution, or publishing services.

## Capability IDs

- `context.confirm`: play back the brief, sources, constraints, unknowns, and acceptance criteria.
- `research.synthesize`: organize supplied research into findings and design implications.
- `source.live.inspect`: inspect a live URL or running product, including flows and states.
- `source.screenshot.inspect`: audit screenshots or captured states.
- `visual.direction.generate`: create materially different visual/concept directions.
- `prototype.interactive.build`: produce an interactive prototype from a design decision or static source.
- `frontend.responsive.build`: implement a responsive frontend artifact.
- `source.image.to.code`: reconstruct a UI from an image with explicit uncertainty and design-system mapping.
- `qa.visual.diff`: compare rendered output against an authoritative visual source and representative states.
- `artifact.design.export`: transfer structured design output into a design tool or editable artifact.
- `artifact.annotate`: attach review findings to an artifact or screen.
- `preview.publish`: host or share an interactive preview with visibility and rollback controls.

## Adapter selection

For every required capability record:

- observed provider/tool/skill;
- evidence of availability;
- input and output formats;
- source fidelity;
- write/external side effects;
- approval needs;
- accessibility and design-system support;
- expected cost/latency;
- fallback and quality loss.

Prefer the smallest reversible composition. A single integrated plugin may be efficient, but an equivalent generic composition must remain documented when portability is a success criterion.

## Ownership boundary

The Product Designer owns problem framing, pattern selection, visual contract, states, trade-offs, and acceptance. Execution adapters own bounded artifact production. Review and gates remain independent of the adapter where feasible.
