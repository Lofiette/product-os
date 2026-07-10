# Product Knowledge Architecture

CPT Product Knowledge is a typed routing and evidence layer, not a second repository and not an encyclopedia.

## Canonical and generated forms

Canonical state is YAML under `.cpt/knowledge/artifacts/` plus `.cpt/knowledge/index.yaml`.
Markdown files under `.cpt/knowledge/views/` are generated projections. Edit canonical YAML, then render views.

## Artifact hierarchy

- `product_map`: routes future tasks to areas, flows, contracts, and decisions.
- `area_map`: routes work inside one product area without narrating all implementation details.
- `flow_map`: captures one bounded user/system flow and its states, data touchpoints, and failures.
- `decision_record`: preserves an approved decision, alternatives, and consequences.
- `api_data_contract`: captures frontend-facing contracts without becoming backend documentation.
- `context_packet`: task-specific evidence assembled from existing knowledge and fresh bounded discovery.

No artifact may absorb the responsibility of the next level. Parent artifacts link downward instead of copying child detail.

## Storage modes

- `existing`: knowledge is discovered from current product evidence.
- `greenfield`: knowledge begins as planned or hypothesized and gains confidence through approved decisions, implementation, tests, and observations.
- `redesign`: baseline (`current`), intended target (`target`), and transition (`delta`) remain distinguishable.

## Quality principle

Size guidance is advisory. Never remove useful knowledge merely to hit a line count. Split mixed abstraction levels, preserve provenance, and keep routing value.
