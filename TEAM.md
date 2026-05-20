# TEAM.md — Maximum Role Catalog

Use this file to understand the available subagents and their boundaries. Do not activate every role by default. Select the smallest sufficient lineup.

## Role catalog

| Role ID | Role | Category | Responsibility |
|---|---|---|---|
| `task-intake-orchestrator` | Task Intake Orchestrator | System | Runs adaptive briefing, updates TASK.md, chooses work mode, and prevents premature implementation. |
| `team-architect` | Team Architect | System | Selects the optimal subagent lineup, resolves role boundaries, and controls collaboration topology. |
| `chronicle-keeper` | Chronicle Keeper | System | Maintains CHRONICLE.md so work survives context compression and handoffs. |
| `consistency-auditor` | Consistency Auditor | System | Checks role outputs, plans, scope, files, and instructions for contradictions before approval or delivery. |
| `product-strategist` | Product Strategist | Product & Discovery | Defines product goal, user value, MVP scope, non-goals, acceptance criteria, and trade-offs. |
| `market-researcher` | Market Researcher | Product & Discovery | Plans and synthesizes market, competitor, category, positioning, and adoption research. |
| `ux-researcher` | UX Researcher | Product & Discovery | Plans user research, hypotheses, interview guides, usability tests, personas, JTBD, and insight synthesis. |
| `cx-researcher` | CX Researcher | Product & Discovery | Maps end-to-end customer experience across touchpoints, service gaps, emotional journey, and support loops. |
| `business-analyst` | Business Analyst | Product & Discovery | Clarifies business rules, stakeholders, constraints, process flows, requirements, and success metrics. |
| `domain-expert` | Domain Expert | Product & Discovery | Extracts domain concepts, invariants, terminology, edge cases, and business logic risks. |
| `ux-interaction-reviewer` | UX Interaction Reviewer | Design & UX | Reviews flows, states, interaction logic, cognitive load, usability, and scenario completeness. |
| `ux-writer` | UX Writer | Design & UX | Owns interface copy, tone, labels, errors, empty states, onboarding, and content clarity. |
| `design-system-guardian` | Design System Guardian | Design & UX | Protects consistency through components, tokens, variants, patterns, and design-system governance. |
| `visual-design-director` | Visual Design Director | Design & UX | Defines visual direction, hierarchy, composition, brand feel, UI polish, and visual coherence. |
| `accessibility-specialist` | Accessibility Specialist | Design & UX | Audits WCAG-oriented accessibility: semantics, keyboard, focus, labels, contrast, errors, and motion. |
| `solution-architect` | Solution Architect | Engineering | Chooses cross-platform architecture, integration boundaries, trade-offs, and system decomposition. |
| `frontend-architect` | Frontend Architect | Engineering | Owns web UI architecture, state, routing, rendering, data fetching, typing, and frontend tests. |
| `backend-architect` | Backend Architect | Engineering | Owns backend services, domain boundaries, persistence, validation, reliability, and API behavior. |
| `mobile-architect` | Mobile Architect | Engineering | Owns mobile/native/cross-platform architecture, navigation, offline, device capabilities, and release constraints. |
| `api-contract-guardian` | API Contract Guardian | Engineering | Protects API contracts, versioning, schemas, errors, compatibility, pagination, and integration expectations. |
| `data-architect` | Data Architect | Engineering | Owns data models, schemas, storage, migrations, retention, lineage, and analytics readiness. |
| `analytics-engineer` | Analytics Engineer | Engineering | Defines product metrics, tracking plans, events, funnels, dashboards, and measurement caveats. |
| `security-reviewer` | Security Reviewer | Risk & Operations | Finds evidence-backed security risks in auth, authorization, secrets, injection, abuse, and isolation. |
| `privacy-compliance-reviewer` | Privacy & Compliance Reviewer | Risk & Operations | Reviews personal data, consent, retention, regulatory risk, data minimization, and compliance-sensitive flows. |
| `performance-engineer` | Performance Engineer | Risk & Operations | Reviews latency, rendering, bundle, query efficiency, caching, scalability, and measurement plans. |
| `qa-engineer` | QA Engineer | Quality | Defines verification strategy, test coverage, edge cases, regression risk, and manual test plans. |
| `code-reviewer` | Code Reviewer | Quality | Reviews diffs for correctness, scope control, maintainability, test adequacy, and merge readiness. |
| `refactoring-specialist` | Refactoring Specialist | Quality | Plans minimal behavior-preserving refactors with staged verification and rollback. |
| `dependency-curator` | Dependency Curator | Risk & Operations | Assesses new dependencies for necessity, maintenance, licenses, security, bundle impact, and alternatives. |
| `migration-planner` | Migration Planner | Risk & Operations | Plans database/data/config migrations, backward compatibility, rollout, rollback, and verification. |
| `devops-release-engineer` | DevOps & Release Engineer | Risk & Operations | Plans CI/CD, deployment, environments, feature flags, rollout, rollback, and release gates. |
| `observability-engineer` | Observability Engineer | Risk & Operations | Defines logs, metrics, traces, alerts, dashboards, SLO signals, and incident visibility. |
| `incident-investigator` | Incident Investigator | Risk & Operations | Triage incidents, reconstruct timelines, find root causes, mitigations, and follow-up actions. |
| `technical-writer` | Technical Writer | Handoff | Creates PR descriptions, developer docs, changelogs, decision records, and handoff summaries. |
| `ai-workflow-auditor` | AI Workflow Auditor | System | Audits whether the Codex workflow followed intake, routing, approvals, evidence, and chronicle rules. |

## Always-consider system roles

- `task-intake-orchestrator`: always at the start of a new task or major scope change.
- `team-architect`: always when more than one specialist role may be needed.
- `chronicle-keeper`: always for work that lasts beyond one response or changes files.
- `consistency-auditor`: always before approval, implementation, and final delivery for complex work.

## Ownership boundaries

- Product Strategist owns product intent. UX Interaction Reviewer owns flow usability. UX Writer owns interface language.
- Market Researcher studies external market/category evidence. UX Researcher studies users and usability. CX Researcher studies end-to-end customer/service experience.
- Design System Guardian owns component/token consistency. Visual Design Director owns art direction and visual coherence. Accessibility Specialist owns accessibility.
- Solution Architect owns cross-system trade-offs. Frontend, Backend, Mobile, API, and Data roles own their implementation domains.
- Security Reviewer owns adversarial security risk. Privacy & Compliance Reviewer owns personal data and regulatory sensitivity.
- QA Engineer owns verification strategy. Code Reviewer owns post-diff review. Consistency Auditor owns process and contradiction checks.
- Technical Writer documents outcomes, but Chronicle Keeper preserves project memory.

## Minimum team patterns

- Tiny copy/UI change: Task Intake Orchestrator, UX Writer or UX Interaction Reviewer, Chronicle Keeper, Code Reviewer if a diff exists.
- UI feature: Product Strategist, UX Interaction Reviewer, UX Writer, Design System Guardian, Frontend Architect, QA Engineer, Code Reviewer.
- Research/discovery: Product Strategist, Market Researcher, UX Researcher, CX Researcher as relevant, Business Analyst, Chronicle Keeper.
- Technical feature: Product Strategist, Solution Architect, relevant engineering architects, QA Engineer, Code Reviewer.
- High-risk production change: add Security Reviewer, Privacy & Compliance Reviewer, Performance Engineer, DevOps & Release Engineer, Observability Engineer as triggered.
