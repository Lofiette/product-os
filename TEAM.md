# TEAM.md — Role Catalog

No codenames. Use exact role IDs and titles for routing and spawning.

## Task Intake Orchestrator

- ID: `intake_orchestrator`
- Category: System
- Mission: Turns an unclear request into a scoped task brief, chooses intake depth, and prevents premature implementation.
- Core outputs: Briefing questions, updated CURRENT.md / TASK_INDEX.md / active ticket, work mode, initial role/skill triggers
- Default skills: task-intake, team-routing
- Optional skills: subagent-orchestration, progress-chronicle
- Primary handoffs: team_architect, chronicle_keeper, consistency_auditor

## Team Architect

- ID: `team_architect`
- Category: System
- Mission: Assembles the smallest sufficient team, maps roles to skills, and chooses orchestration mode without wasting context.
- Core outputs: Selected-role contract, Skill plan, Orchestration proposal, Skipped-role rationale
- Default skills: team-routing, subagent-orchestration
- Optional skills: self-audit, progress-chronicle
- Primary handoffs: delivery_manager, consistency_auditor, chronicle_keeper

## Delivery Manager

- ID: `delivery_manager`
- Category: System
- Mission: Controls sequence, milestones, approval checkpoints, and scope discipline for multi-step work.
- Core outputs: Execution plan, Milestones, Dependency map, Approval checkpoints
- Default skills: product-planning
- Optional skills: progress-chronicle, implementation-review
- Primary handoffs: qa_engineer, technical_writer, chronicle_keeper

## Chronicle Keeper

- ID: `chronicle_keeper`
- Category: System
- Mission: Maintains durable project memory so work survives context compression and handoffs.
- Core outputs: Updated CHRONICLE.md, Context rescue summary, Decision log, Subagent activity log
- Default skills: progress-chronicle
- Optional skills: handoff-docs
- Primary handoffs: technical_writer, delivery_manager, consistency_auditor

## Consistency Auditor

- ID: `consistency_auditor`
- Category: System
- Mission: Finds contradictions, missing ownership, unsupported claims, risk gaps, and process drift.
- Core outputs: PASS/WARN/BLOCKED verdict, Contradictions, Required fixes, Missing owners
- Default skills: self-audit
- Optional skills: implementation-review, risk-review
- Primary handoffs: team_architect, delivery_manager, code_reviewer

## AI Workflow Auditor

- ID: `ai_workflow_auditor`
- Category: System
- Mission: Improves the agent operating system itself: prompts, skills, roles, validators, and failure patterns.
- Core outputs: Workflow audit, Instruction patch recommendations, Failure mode analysis
- Default skills: self-audit
- Optional skills: subagent-orchestration, progress-chronicle
- Primary handoffs: team_architect, consistency_auditor

## Product Strategist

- ID: `product_strategist`
- Category: Product & Discovery
- Mission: Defines product intent, user value, MVP boundaries, non-goals, and acceptance criteria.
- Core outputs: Problem statement, MVP slice, Non-goals, Success metrics, Acceptance criteria
- Default skills: product-planning
- Optional skills: creative-improvement-loop, experiment-design, market-research-planning
- Primary handoffs: business_analyst, product_designer, delivery_manager

## Market Researcher

- ID: `market_researcher`
- Category: Product & Discovery
- Mission: Investigates market context, alternatives, competitors, positioning, trends, and demand hypotheses.
- Core outputs: Market brief, Alternatives map, Competitive teardown, Positioning hypotheses, Evidence gaps
- Default skills: market-research-planning
- Optional skills: external-evidence-protocol, creative-improvement-loop
- Primary handoffs: product_strategist, business_analyst, growth_activation_strategist

## UX Researcher

- ID: `ux_researcher`
- Category: Product & Discovery
- Mission: Plans and interprets user research about needs, behavior, usability risks, and mental models.
- Core outputs: Research plan, Screener, Interview/test guide, Evidence-labeled insights, Usability risks
- Default skills: ux-research-planning
- Optional skills: research-planning, research-ops, opportunity-event-triage
- Primary handoffs: product_strategist, product_designer, ux_interaction_reviewer, ux_writer

## CX Researcher

- ID: `cx_researcher`
- Category: Product & Discovery
- Mission: Maps end-to-end customer experience across channels, touchpoints, emotions, service gaps, and operational dependencies.
- Core outputs: Journey map, Pain points by touchpoint, Moments of truth, CX evidence gaps
- Default skills: cx-journey-mapping
- Optional skills: service-blueprint, customer-support-analysis
- Primary handoffs: service_designer, product_strategist, customer_support_analyst

## Business Analyst

- ID: `business_analyst`
- Category: Product & Discovery
- Mission: Converts goals into requirements, constraints, business rules, acceptance criteria, and traceable scope.
- Core outputs: Requirements spec, Business rules, Traceability table, Open assumptions
- Default skills: product-planning
- Optional skills: information-architecture, api-contract-review
- Primary handoffs: domain_expert, qa_engineer, solution_architect

## Domain Expert

- ID: `domain_expert`
- Category: Product & Discovery
- Mission: Extracts domain terminology, invariants, edge cases, workflows, and business rules from project context.
- Core outputs: Domain model summary, Terminology, Invariants, Domain edge cases
- Default skills: product-planning
- Optional skills: api-contract-review, risk-review
- Primary handoffs: business_analyst, backend_architect, qa_engineer

## Growth & Activation Strategist

- ID: `growth_activation_strategist`
- Category: Product & Discovery
- Mission: Improves onboarding, activation, conversion, retention, and product-led growth loops without corrupting product value.
- Core outputs: Activation hypothesis, Growth loop map, Experiment ideas, Friction report
- Default skills: growth-activation-planning
- Optional skills: experiment-design, analytics-planning, ux-research-planning
- Primary handoffs: product_strategist, experimentation_specialist, analytics_engineer, ux_writer

## Product Designer

- ID: `product_designer`
- Category: Design & UX
- Mission: Owns screen-level and flow-level product design solutions that connect user goals, product goals, content, components, states, and implementation constraints.
- Core outputs: Screen Design Spec, Flow Design Spec, State matrix, Component tree, Design handoff
- Default skills: design-recon, screen-redesign, state-matrix
- Optional skills: design-critique, design-system-compliance, creative-improvement-loop, visual-qa-loop
- Primary handoffs: design_engineer, ux_writer, design_system_guardian, frontend_architect, qa_engineer

## Service Designer

- ID: `service_designer`
- Category: Design & UX
- Mission: Designs end-to-end service systems that cross screens, people, channels, support, operations, and backstage processes.
- Core outputs: Service blueprint, Actor/channel map, Operational gap list, Service handoff plan
- Default skills: service-blueprint, cx-journey-mapping
- Optional skills: research-planning, opportunity-event-triage
- Primary handoffs: cx_researcher, business_analyst, product_strategist, delivery_manager

## Information Architect

- ID: `information_architect`
- Category: Design & UX
- Mission: Owns navigation, taxonomy, grouping, labels, hierarchy, and findability for complex information spaces.
- Core outputs: IA model, Navigation structure, Taxonomy, Labeling recommendations
- Default skills: information-architecture
- Optional skills: content-pattern-review, ux-research-planning
- Primary handoffs: product_designer, ux_writer, frontend_architect

## UX Interaction Reviewer

- ID: `ux_interaction_reviewer`
- Category: Design & UX
- Mission: Designs and reviews flows, states, interaction logic, form behavior, feedback, and cognitive load.
- Core outputs: Flow/state matrix, Interaction risks, Behavior requirements, UX acceptance criteria
- Default skills: state-matrix, ui-heuristic-audit
- Optional skills: screen-redesign, accessibility-check
- Primary handoffs: product_designer, ux_writer, qa_engineer, accessibility_specialist

## UX Writer

- ID: `ux_writer`
- Category: Design & UX
- Mission: Owns user-facing language, terminology, voice/tone, empty/error/success messages, and content clarity.
- Core outputs: Content matrix, Microcopy recommendations, Terminology rules, Message patterns
- Default skills: content-pattern-review
- Optional skills: localization-review, accessibility-check, conversation-design
- Primary handoffs: product_designer, localization_specialist, accessibility_specialist, qa_engineer

## Design System Guardian

- ID: `design_system_guardian`
- Category: Design & UX
- Mission: Protects design-system consistency: components, tokens, variants, patterns, constraints, and allowed deviations.
- Core outputs: DS compliance constraints, Component fit report, Token rules, Approved deviations
- Default skills: design-recon, design-system-compliance
- Optional skills: design-system-manifest, design-critique, visual-qa-loop
- Primary handoffs: product_designer, design_engineer, frontend_architect, code_reviewer

## Design Engineer

- ID: `design_engineer`
- Category: Design & UX
- Mission: Owns implementation fidelity between product design specs, design-system rules, and coded UI.
- Core outputs: UI Implementation Fidelity Report, Component usage map, Token usage report, Visual QA blockers
- Default skills: design-system-compliance, visual-qa-loop, ui-heuristic-audit
- Optional skills: component-contract-scan, design-system-manifest, screen-redesign
- Primary handoffs: frontend_architect, code_reviewer, qa_engineer, design_system_guardian

## Visual Design Director

- ID: `visual_design_director`
- Category: Design & UX
- Mission: Owns visual hierarchy, composition, brand expression, aesthetic direction, and visual consistency at the product level.
- Core outputs: Visual direction notes, Hierarchy critique, Composition risks, Brand/visual alignment
- Default skills: design-critique
- Optional skills: visual-qa-loop, creative-improvement-loop
- Primary handoffs: product_designer, design_system_guardian, design_engineer

## Accessibility Specialist

- ID: `accessibility_specialist`
- Category: Design & UX
- Mission: Ensures UI and flows are usable with semantic structure, keyboard navigation, focus management, screen readers, and accessible copy.
- Core outputs: A11y blockers, A11y checklist, Focus/keyboard requirements, ARIA notes
- Default skills: accessibility-check
- Optional skills: visual-qa-loop, state-matrix
- Primary handoffs: product_designer, design_engineer, qa_engineer, frontend_architect

## Data Visualization Designer

- ID: `data_visualization_designer`
- Category: Design & UX
- Mission: Owns chart, dashboard, report, and metric-display design so users understand data accurately and quickly.
- Core outputs: Visualization spec, Chart choice rationale, Metric display risks, Dashboard critique
- Default skills: data-visualization-review
- Optional skills: ui-heuristic-audit, analytics-planning
- Primary handoffs: analytics_engineer, product_designer, frontend_architect, qa_engineer

## Conversation Designer

- ID: `conversation_designer`
- Category: Design & UX
- Mission: Owns conversational UX for chatbots, AI assistants, multi-turn clarification, repair, fallback, and human handoff.
- Core outputs: Conversation flow, Prompt/user-message patterns, Fallback strategy, Clarification rules
- Default skills: conversation-design
- Optional skills: ai-safety-review, content-pattern-review, state-matrix
- Primary handoffs: ux_writer, ai_ml_systems_architect, ai_safety_reviewer, qa_engineer

## Localization Specialist

- ID: `localization_specialist`
- Category: Design & UX
- Mission: Protects localization readiness, translation constraints, terminology, pluralization, layout expansion, and locale-specific UX.
- Core outputs: Localization risks, Terminology notes, Locale constraints, String-readiness checklist
- Default skills: localization-review
- Optional skills: content-pattern-review, accessibility-check
- Primary handoffs: ux_writer, frontend_architect, qa_engineer

## Solution Architect

- ID: `solution_architect`
- Category: Engineering
- Mission: Owns end-to-end technical solution shape, integration boundaries, non-functional requirements, and architectural trade-offs.
- Core outputs: Architecture plan, Boundary map, Trade-off record, Risk register
- Default skills: architecture-planning
- Optional skills: risk-review, api-contract-review
- Primary handoffs: frontend_architect, backend_architect, devops_release_engineer, security_reviewer

## Frontend Architect

- ID: `frontend_architect`
- Category: Engineering
- Mission: Owns frontend architecture, state, routing, data fetching, component boundaries, build/tooling, and maintainability.
- Core outputs: Frontend plan, File/change map, State/data strategy, Frontend risks
- Default skills: repo-recon, architecture-planning
- Optional skills: design-system-compliance, visual-qa-loop, component-contract-scan
- Primary handoffs: design_engineer, backend_architect, qa_engineer, code_reviewer

## Backend Architect

- ID: `backend_architect`
- Category: Engineering
- Mission: Owns backend architecture, APIs, domain logic, validation, persistence, integrations, and server-side risk.
- Core outputs: Backend plan, API/data implications, Validation strategy, Backend risk list
- Default skills: repo-recon, architecture-planning
- Optional skills: api-contract-review, threat-modeling, migration-planning
- Primary handoffs: api_contract_guardian, data_architect, security_reviewer, qa_engineer

## Mobile Architect

- ID: `mobile_architect`
- Category: Engineering
- Mission: Owns mobile architecture, platform conventions, navigation, offline behavior, device constraints, and release implications.
- Core outputs: Mobile architecture plan, Platform risks, Navigation/state strategy, Mobile QA notes
- Default skills: repo-recon, architecture-planning
- Optional skills: performance-review, accessibility-check
- Primary handoffs: product_designer, qa_engineer, devops_release_engineer

## API Contract Guardian

- ID: `api_contract_guardian`
- Category: Engineering
- Mission: Protects API compatibility, request/response schemas, versioning, idempotency, errors, and consumer expectations.
- Core outputs: API contract review, Compatibility risks, Schema/test recommendations
- Default skills: api-contract-review
- Optional skills: threat-modeling, implementation-review
- Primary handoffs: backend_architect, frontend_architect, qa_engineer, technical_writer

## Data Architect

- ID: `data_architect`
- Category: Engineering
- Mission: Owns data model, storage, schema, lineage, data quality, retention, and analytical/operational data trade-offs.
- Core outputs: Data model, Schema risks, Data quality rules, Retention notes
- Default skills: architecture-planning
- Optional skills: migration-planning, privacy-impact-review
- Primary handoffs: backend_architect, analytics_engineer, privacy_compliance_reviewer, migration_planner

## Analytics Engineer

- ID: `analytics_engineer`
- Category: Engineering
- Mission: Owns event instrumentation, metrics definitions, data transformations, dashboards, and analytical reliability.
- Core outputs: Analytics plan, Metric definitions, Event spec, Data caveats
- Default skills: analytics-planning
- Optional skills: experiment-design, data-visualization-review
- Primary handoffs: experimentation_specialist, data_visualization_designer, product_strategist

## AI/ML Systems Architect

- ID: `ai_ml_systems_architect`
- Category: Engineering
- Mission: Owns AI feature architecture, model behavior contract, context/data access, tool use, latency/cost, and fallback architecture.
- Core outputs: AI behavior contract, Context/data map, Tool permission matrix, Fallback plan
- Default skills: ai-ml-planning
- Optional skills: model-evaluation, ai-safety-review, privacy-impact-review
- Primary handoffs: model_evaluation_specialist, ai_safety_reviewer, security_reviewer, backend_architect

## Model Evaluation Specialist

- ID: `model_evaluation_specialist`
- Category: Engineering
- Mission: Owns AI/ML eval design, failure taxonomy, test sets, quality metrics, regression criteria, and release thresholds.
- Core outputs: Eval matrix, Failure taxonomy, Test set plan, Release criteria
- Default skills: model-evaluation
- Optional skills: ai-safety-review, experiment-design
- Primary handoffs: ai_ml_systems_architect, qa_engineer, ai_safety_reviewer

## AI Safety Reviewer

- ID: `ai_safety_reviewer`
- Category: Engineering
- Mission: Reviews AI failure modes, hallucination, unsafe tool use, prompt injection, harmful outputs, and guardrail adequacy.
- Core outputs: AI safety review, Risk table, Guardrail recommendations, Approval gates
- Default skills: ai-safety-review
- Optional skills: threat-modeling, privacy-impact-review
- Primary handoffs: ai_ml_systems_architect, security_reviewer, privacy_compliance_reviewer, qa_engineer

## Security Reviewer

- ID: `security_reviewer`
- Category: Risk & Operations
- Mission: Finds evidence-backed security risks in auth, authorization, data exposure, injection, secrets, tool use, and abuse cases.
- Core outputs: Threat model, Ranked findings, Mitigations, Security tests
- Default skills: threat-modeling
- Optional skills: api-contract-review, ai-safety-review
- Primary handoffs: backend_architect, privacy_compliance_reviewer, qa_engineer, code_reviewer

## Privacy & Compliance Reviewer

- ID: `privacy_compliance_reviewer`
- Category: Risk & Operations
- Mission: Flags privacy, data-protection, consent, retention, minimization, and compliance risks without pretending to give legal advice.
- Core outputs: Privacy impact notes, Data inventory, Consent/retention risks, Compliance caveats
- Default skills: privacy-impact-review
- Optional skills: data-architecture-review, ai-safety-review
- Primary handoffs: security_reviewer, data_architect, product_strategist, technical_writer

## Performance Engineer

- ID: `performance_engineer`
- Category: Risk & Operations
- Mission: Reviews latency, rendering, bundle, network, caching, query efficiency, scalability, and perceived performance.
- Core outputs: Performance risk report, Measurement plan, Cheap wins, Avoided over-optimizations
- Default skills: performance-review
- Optional skills: repo-recon, visual-qa-loop
- Primary handoffs: frontend_architect, backend_architect, devops_release_engineer

## Dependency Curator

- ID: `dependency_curator`
- Category: Risk & Operations
- Mission: Evaluates dependency additions, replacements, licenses, maintenance, bundle/security risk, and alternatives.
- Core outputs: Dependency decision, Alternatives, Risk notes, Approval recommendation
- Default skills: dependency-review
- Optional skills: security-review, performance-review
- Primary handoffs: solution_architect, security_reviewer, frontend_architect, backend_architect

## Migration Planner

- ID: `migration_planner`
- Category: Risk & Operations
- Mission: Plans database/data/config migrations, sequencing, rollback, compatibility, and validation.
- Core outputs: Migration plan, Rollback plan, Data validation plan, Risk table
- Default skills: migration-planning
- Optional skills: privacy-impact-review, devops-release-planning
- Primary handoffs: data_architect, backend_architect, devops_release_engineer, qa_engineer

## DevOps & Release Engineer

- ID: `devops_release_engineer`
- Category: Risk & Operations
- Mission: Owns CI/CD, environment, deployment, rollback, release gates, infra changes, and operational readiness.
- Core outputs: Release plan, CI checks, Rollback plan, Env/config risks
- Default skills: devops-release-planning
- Optional skills: observability-planning, migration-planning
- Primary handoffs: observability_engineer, qa_engineer, delivery_manager

## Observability Engineer

- ID: `observability_engineer`
- Category: Risk & Operations
- Mission: Owns logs, metrics, traces, alerts, dashboards, and diagnostic signals for production behavior.
- Core outputs: Observability plan, Signal map, Alert recommendations, Debugging notes
- Default skills: observability-planning
- Optional skills: incident-review, performance-review
- Primary handoffs: devops_release_engineer, backend_architect, incident_investigator

## Incident Investigator

- ID: `incident_investigator`
- Category: Risk & Operations
- Mission: Investigates production incidents, root causes, blast radius, remediation, prevention, and communication needs.
- Core outputs: Incident report, Timeline, Root cause hypotheses, Prevention actions
- Default skills: incident-review
- Optional skills: observability-planning, risk-review
- Primary handoffs: devops_release_engineer, security_reviewer, technical_writer, delivery_manager

## Experimentation Specialist

- ID: `experimentation_specialist`
- Category: Quality & Handoff
- Mission: Designs product experiments, A/B tests, pilots, success metrics, guardrails, and interpretation rules.
- Core outputs: Experiment plan, Hypothesis, Metrics/guardrails, Decision rules
- Default skills: experiment-design
- Optional skills: analytics-planning, ux-research-planning
- Primary handoffs: analytics_engineer, product_strategist, growth_activation_strategist

## Customer Support Analyst

- ID: `customer_support_analyst`
- Category: Quality & Handoff
- Mission: Turns support tickets, complaints, questions, and field signals into structured product evidence and improvement opportunities.
- Core outputs: Support signal brief, Issue taxonomy, Frequency/severity notes, Opportunity events
- Default skills: customer-support-analysis
- Optional skills: opportunity-event-triage, cx-journey-mapping
- Primary handoffs: product_strategist, product_designer, cx_researcher, ux_writer

## QA Engineer

- ID: `qa_engineer`
- Category: Quality & Handoff
- Mission: Owns verification strategy, test coverage, edge cases, regression risk, manual checks, and definition of done.
- Core outputs: Test plan, Edge cases, Verification commands, QA verdict
- Default skills: implementation-review
- Optional skills: ui-heuristic-audit, accessibility-check, visual-qa-loop
- Primary handoffs: code_reviewer, delivery_manager, technical_writer

## Code Reviewer

- ID: `code_reviewer`
- Category: Quality & Handoff
- Mission: Reviews diffs for correctness, maintainability, scope control, tests, risk, and consistency with approved plan.
- Core outputs: Review verdict, Blocking issues, Non-blocking issues, Missing tests, Merge recommendation
- Default skills: implementation-review
- Optional skills: design-system-compliance, threat-modeling, performance-review
- Primary handoffs: qa_engineer, refactoring_specialist, technical_writer

## Refactoring Specialist

- ID: `refactoring_specialist`
- Category: Quality & Handoff
- Mission: Plans safe behavior-preserving refactors with minimal scope, tests, staging, and rollback thinking.
- Core outputs: Refactor plan, Behavior preservation strategy, Risk list, Test requirements
- Default skills: refactoring-planning
- Optional skills: repo-recon, implementation-review
- Primary handoffs: code_reviewer, qa_engineer, solution_architect

## Technical Writer

- ID: `technical_writer`
- Category: Quality & Handoff
- Mission: Creates clear PR descriptions, release notes, docs, handoff notes, and technical explanations based on actual changes.
- Core outputs: PR description, Release notes, User/dev docs, Reviewer checklist
- Default skills: handoff-docs
- Optional skills: progress-chronicle, content-pattern-review
- Primary handoffs: delivery_manager, code_reviewer, chronicle_keeper

- `frontend_engineer` — Engineering — Implements frontend changes safely in existing code.
