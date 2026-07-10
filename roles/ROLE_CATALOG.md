# Role Catalog

The 4.0 role library preserves 50 logical accountability lenses. Roles do not equal workers. Select the smallest set that changes decision quality, evidence, risk detection, or acceptance.

## Design & UX

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `accessibility_specialist` | Ensures UI and flows are usable with semantic structure, keyboard navigation, focus management, screen readers, and accessible copy. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `conversation_designer` | Owns conversational UX for chatbots, AI assistants, multi-turn clarification, repair, fallback, and human handoff. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `data_visualization_designer` | Owns chart, dashboard, report, and metric-display design so users understand data accurately and quickly. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `design_engineer` | Owns implementation fidelity between product design specs, design-system rules, and coded UI. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `design_system_guardian` | Protects design-system consistency: components, tokens, variants, patterns, constraints, and allowed deviations. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `information_architect` | Owns navigation, taxonomy, grouping, labels, hierarchy, and findability for complex information spaces. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `localization_specialist` | Protects localization readiness, translation constraints, terminology, pluralization, layout expansion, and locale-specific UX. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `product_designer` | Owns screen-level and flow-level product design solutions that connect user goals, product goals, content, components, states, and implementation constraints. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `service_designer` | Designs end-to-end service systems that cross screens, people, channels, support, operations, and backstage processes. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `ux_interaction_reviewer` | Designs and reviews flows, states, interaction logic, form behavior, feedback, and cognitive load. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `ux_writer` | Owns user-facing language, terminology, voice/tone, empty/error/success messages, and content clarity. | `cpt-design-ui` | `main_thread_lens` | `conditional` |
| `visual_design_director` | Owns visual hierarchy, composition, brand expression, aesthetic direction, and visual consistency at the product level. | `cpt-design-ui` | `main_thread_lens` | `conditional` |

## Engineering

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `ai_safety_reviewer` | Reviews AI failure modes, hallucination, unsafe tool use, prompt injection, harmful outputs, and guardrail adequacy. | `cpt-ai-agentic` | `main_thread_lens` | `conditional` |
| `ai_ml_systems_architect` | Owns AI feature architecture, model behavior contract, context/data access, tool use, latency/cost, and fallback architecture. | `cpt-ai-agentic` | `main_thread_lens` | `conditional` |
| `api_contract_guardian` | Protects API compatibility, request/response schemas, versioning, idempotency, errors, and consumer expectations. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `analytics_engineer` | Owns event instrumentation, metrics definitions, data transformations, dashboards, and analytical reliability. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `backend_architect` | Owns backend architecture, APIs, domain logic, validation, persistence, integrations, and server-side risk. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `data_architect` | Owns data model, storage, schema, lineage, data quality, retention, and analytical/operational data trade-offs. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `frontend_architect` | Owns frontend architecture, state, routing, data fetching, component boundaries, build/tooling, and maintainability. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `frontend_engineer` | Implements frontend changes safely in existing code: components, routing, state, data flow, UI integration, maintainability, and regression avoidance. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `mobile_architect` | Owns mobile architecture, platform conventions, navigation, offline behavior, device constraints, and release implications. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `model_evaluation_specialist` | Owns AI/ML eval design, failure taxonomy, test sets, quality metrics, regression criteria, and release thresholds. | `cpt-ai-agentic` | `main_thread_lens` | `conditional` |
| `solution_architect` | Owns end-to-end technical solution shape, integration boundaries, non-functional requirements, and architectural trade-offs. | `cpt-engineering` | `main_thread_lens` | `conditional` |

## Product & Discovery

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `business_analyst` | Converts goals into requirements, constraints, business rules, acceptance criteria, and traceable scope. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `cx_researcher` | Maps end-to-end customer experience across channels, touchpoints, emotions, service gaps, and operational dependencies. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `domain_expert` | Extracts domain terminology, invariants, edge cases, workflows, and business rules from project context. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `growth_activation_strategist` | Improves onboarding, activation, conversion, retention, and product-led growth loops without corrupting product value. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `market_researcher` | Investigates market context, alternatives, competitors, positioning, trends, and demand hypotheses. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `product_strategist` | Defines product intent, user value, MVP boundaries, non-goals, and acceptance criteria. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `ux_researcher` | Plans and interprets user research about needs, behavior, usability risks, and mental models. | `cpt-product-research` | `main_thread_lens` | `conditional` |

## Quality & Handoff

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `code_reviewer` | Reviews diffs for correctness, maintainability, scope control, tests, risk, and consistency with approved plan. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `customer_support_analyst` | Turns support tickets, complaints, questions, and field signals into structured product evidence and improvement opportunities. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `experimentation_specialist` | Designs product experiments, A/B tests, pilots, success metrics, guardrails, and interpretation rules. | `cpt-product-research` | `main_thread_lens` | `conditional` |
| `qa_engineer` | Owns verification strategy, test coverage, edge cases, regression risk, manual checks, and definition of done. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `refactoring_specialist` | Plans safe behavior-preserving refactors with minimal scope, tests, staging, and rollback thinking. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `technical_writer` | Creates clear PR descriptions, release notes, docs, handoff notes, and technical explanations based on actual changes. | `cpt-engineering` | `main_thread_lens` | `conditional` |

## Risk & Operations

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `dependency_curator` | Evaluates dependency additions, replacements, licenses, maintenance, bundle/security risk, and alternatives. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `devops_release_engineer` | Owns CI/CD, environment, deployment, rollback, release gates, infra changes, and operational readiness. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `incident_investigator` | Investigates production incidents, root causes, blast radius, remediation, prevention, and communication needs. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `migration_planner` | Plans database/data/config migrations, sequencing, rollback, compatibility, and validation. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `observability_engineer` | Owns logs, metrics, traces, alerts, dashboards, and diagnostic signals for production behavior. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `performance_engineer` | Reviews latency, rendering, bundle, network, caching, query efficiency, scalability, and perceived performance. | `cpt-engineering` | `main_thread_lens` | `conditional` |
| `privacy_compliance_reviewer` | Flags privacy, data-protection, consent, retention, minimization, and compliance risks without pretending to give legal advice. | `cpt-risk-operations` | `main_thread_lens` | `conditional` |
| `security_reviewer` | Finds evidence-backed security risks in auth, authorization, data exposure, injection, secrets, tool use, and abuse cases. | `cpt-risk-operations` | `main_thread_lens` | `conditional` |

## System

| Role | Mission | Plugin | Default execution | Worker eligible |
|---|---|---|---|---|
| `ai_workflow_auditor` | Improves the agent operating system itself: prompts, skills, roles, validators, and failure patterns. | `cpt-core` | `main_thread_lens` | `conditional` |
| `chronicle_keeper` | Maintains durable project memory so work survives context compression and handoffs. | `cpt-core` | `main_thread_lens` | `never` |
| `consistency_auditor` | Finds contradictions, missing ownership, unsupported claims, risk gaps, and process drift. | `cpt-core` | `main_thread_lens` | `conditional` |
| `delivery_manager` | Controls sequence, milestones, approval checkpoints, and scope discipline for multi-step work. | `cpt-core` | `main_thread_lens` | `never` |
| `intake_orchestrator` | Turns an unclear request into a scoped task brief, chooses intake depth, and prevents premature implementation. | `cpt-core` | `main_thread_lens` | `never` |
| `team_architect` | Assembles the smallest sufficient team, maps roles to skills, and chooses orchestration mode without wasting context. | `cpt-core` | `main_thread_lens` | `never` |

