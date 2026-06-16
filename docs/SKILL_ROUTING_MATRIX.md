# SKILL_ROUTING_MATRIX.md — 3.0 beta 2

Use this matrix after task classification. Prefer explicit skill IDs for critical workflows; do not rely only on implicit skill discovery.

## Runtime Kernel / Safe Autonomy

| Situation | Skills |
|---|---|
| User gives a new product/UI task | new-task-protocol, framework-loading |
| Need to inspect project without overload | bounded-discovery |
| Need pre-implementation scope | impact-map |
| Task changed durable knowledge | knowledge-update |
| End of task / context getting large | chronicle-compaction, context-prune |
| Runtime memory/tickets need checks | memory-integrity-check, task-ledger, ticket-router |

## Product Knowledge

| Situation | Skills |
|---|---|
| Existing product onboarding | product-knowledge-onboarding, bounded-discovery, knowledge-update |
| Greenfield product | greenfield-onboarding, product-knowledge-onboarding, product-planning |
| Redesign/migration | product-knowledge-onboarding, reference-fidelity, design-source-authority, impact-map |
| API/data shape prewarm | api-data-shape-prewarm, api-contract-review |
| Freshness review | knowledge-freshness-review, knowledge-update |
| Task-specific context | context-packet assembly through impact-map + knowledge-update |

## UI / design / DS

| Situation | Skills |
|---|---|
| UI prototype, no DS | design-recon, prototype-ui-kit, screen-redesign, state-matrix, ui-heuristic-audit |
| Existing DS in code | repo-recon, design-recon, design-system-manifest, design-system-compliance, ds-code-contract-enforcement |
| Module design for developer rebuild | design-recon, module-design, design-handoff-qa, handoff-docs |
| Implemented UI | design-system-compliance, component-contract-scan, visual-qa-loop, ui-heuristic-audit, design-qa |
| Reference screenshot/mock/example | reference-fidelity, screenshot-reference-comparison |
| DS source authority / generated manifest | design-source-authority, manifest-freeze-check |
| Prototype/demo content | content-realism-review |
| Debug/prototype controls visible | debug-control-review |
| Taste / good-bad examples | taste-calibration, example-taste-board, taste-review, creative-tension-review when needed |

## Frontend / implementation

| Situation | Skills |
|---|---|
| UI implementation in existing repo | repo-recon, frontend-integration-review, impact-map, implementation-review |
| API-dependent UI | api-data-shape-prewarm, api-contract-review, frontend-integration-review |
| Component refactor | refactoring-planning, component-contract-scan, implementation-review |
| Production UI change | visual-qa-loop, design-system-compliance, component-contract-scan, implementation-review |

## AI / risk / operations

| Situation | Skills |
|---|---|
| AI feature | ai-ml-planning, model-evaluation, ai-safety-review |
| AI tool actions | threat-modeling, privacy-impact-review, ai-safety-review, api-contract-review |
| Security/privacy risk | security-review, privacy-impact-review, threat-modeling |
| Production/release | production-service-planning, production-readiness-review, devops-release-planning, observability-planning |
| Incident | incident-review, observability-planning |

## Research / analytics / service

| Situation | Skills |
|---|---|
| UX research | ux-research-planning, research-ops if executing study |
| Market research | market-research-planning, external-evidence-protocol |
| CX/service journey | cx-journey-mapping, service-blueprint |
| Experiment/activation | experiment-design, growth-activation-planning, analytics-planning |

Rules:
- Use Tiny/Micro no-index path for obvious small tasks.
- Do not load all skills.
- If a required skill path is unknown, ask for bounded framework-index discovery.
- A skill does not imply a real subagent.
- Real subagents require approval.
