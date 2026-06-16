# ROLE_ROUTING_MATRIX.md — 3.0 beta 2

Use this matrix after the Runtime Kernel has classified the task and selected the relevant Product Knowledge area. Do not load every role. Select the smallest useful set and explain skipped roles.

## Core routing principles

- Role = accountability / expert perspective, not automatically a real subagent.
- Default execution is role simulation unless an independent artifact or parallel review justifies a spawned subagent.
- Real subagents require explicit user approval.
- UI/product implementation must include frontend engineering responsibility. Do not route implementation as design-only work.
- If API/data/server behavior constrains UI, add API/data/backend roles.

## Runtime / task management

| Operation | Usually select | Notes |
|---|---|---|
| New task intake | intake_orchestrator, team_architect | Use `new-task-protocol`, ticketing, and bounded discovery. |
| Product knowledge onboarding | product_strategist, information_architect, domain_expert, consistency_auditor | Add frontend/data roles only when reading implementation evidence. |
| Context/memory maintenance | chronicle_keeper, delivery_manager, consistency_auditor | Use compact CHRONICLE, do not create archive logs by default. |
| Framework loading uncertainty | team_architect, consistency_auditor | Use bounded framework-index discovery, not broad scans. |

## Product / discovery / planning

| Operation | Core roles | Conditional roles |
|---|---|---|
| Existing product onboarding | product_strategist, information_architect, domain_expert | frontend_architect/frontend_engineer when code evidence is needed; api_contract_guardian for data contracts. |
| Greenfield product creation | product_strategist, product_designer, solution_architect, delivery_manager | ux_researcher, market_researcher, business_analyst, domain_expert, design_system_guardian, frontend_architect. |
| Redesign / migration | product_designer, information_architect, design_system_guardian, frontend_architect, delivery_manager | ux_researcher, visual_design_director, design_engineer, qa_engineer, code_reviewer. |
| Product scope / MVP shaping | product_strategist, business_analyst, delivery_manager | domain_expert, market_researcher, cx_researcher. |

## UI / UX / design

| Operation | Core roles | Conditional roles |
|---|---|---|
| Screen creation/redesign | product_designer, ux_writer, design_system_guardian | information_architect, visual_design_director, accessibility_specialist, data_visualization_designer. |
| UI prototype without DS | product_designer, design_engineer | design_system_guardian for lightweight local UI rules, ux_writer, qa_engineer. |
| Governed DS work | design_system_guardian, design_engineer | frontend_engineer for implementation, accessibility_specialist for production UI. |
| Visual/reference fidelity review | product_designer, design_engineer, visual_design_director | qa_engineer, design_system_guardian, ux_writer. |
| Design-only module handoff | product_designer, information_architect, design_system_guardian, ux_writer, design_engineer, qa_engineer | technical_writer if handoff docs are user-facing. |

## UI/product implementation in code

| Operation | Core roles | Conditional roles |
|---|---|---|
| Existing repo UI implementation | frontend_engineer, design_engineer, qa_engineer | frontend_architect if structural risk; design_system_guardian if DS exists; code_reviewer before final. |
| Systemic UI/code change | frontend_architect, frontend_engineer, design_engineer, code_reviewer, qa_engineer | product_designer/ux_writer when behavior/copy changes. |
| API-dependent UI | frontend_engineer, api_contract_guardian, qa_engineer | backend_architect if backend behavior may change; data_architect if entities/data model change. |
| Component refactor | frontend_architect, frontend_engineer, refactoring_specialist, code_reviewer | design_system_guardian/design_engineer if component is UI/DS-facing. |

## Architecture / API / data / operations

| Operation | Core roles | Conditional roles |
|---|---|---|
| Backend/API change | backend_architect, api_contract_guardian, qa_engineer | security_reviewer, privacy_compliance_reviewer, data_architect. |
| Data model / analytics | data_architect, analytics_engineer | product_strategist, privacy_compliance_reviewer, qa_engineer. |
| Production web service | solution_architect, frontend_architect, backend_architect, devops_release_engineer, qa_engineer | security, privacy, performance, observability, API/data roles by risk. |
| Incident / reliability | incident_investigator, observability_engineer, devops_release_engineer | backend/frontend architects, security if suspicious. |
| Performance | performance_engineer | frontend/backend architects, observability. |

## AI / agentic / conversational

| Operation | Core roles | Conditional roles |
|---|---|---|
| AI/ML feature | ai_ml_systems_architect, model_evaluation_specialist, ai_safety_reviewer | privacy, security, backend, frontend, product_designer. |
| Tool-using agent | ai_ml_systems_architect, ai_safety_reviewer, security_reviewer, privacy_compliance_reviewer, api_contract_guardian | model_evaluation, qa, backend/frontend architects. |
| Conversation UI | conversation_designer, ux_writer, product_designer | ai_safety_reviewer, frontend_engineer, qa_engineer. |

## Research / CX / growth / localization

| Operation | Core roles | Conditional roles |
|---|---|---|
| UX research only | ux_researcher | research-ops skill if execution planned; do not implement. |
| Market research | market_researcher | product_strategist, business_analyst. |
| CX journey/service | cx_researcher, service_designer | product_strategist, customer_support_analyst. |
| Growth/activation | growth_activation_strategist, experimentation_specialist, analytics_engineer | ux_writer, product_designer. |
| Localization | localization_specialist, ux_writer | product_designer, frontend_engineer. |
