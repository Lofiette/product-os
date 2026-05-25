# ROLE_METHOD_LIBRARY.md — Deep Role Method Protocols

Use this file when a role's playbook needs more operational depth. It is not a substitute for selected role playbooks; it is a shared method library. Load only the sections relevant to selected roles.

## Product Strategist / Cloud

Protocol:
1. Frame the outcome: user problem, business goal, decision to support.
2. Separate solution idea from underlying need.
3. Define primary user, buyer, operator, and stakeholder if they differ.
4. Slice scope into Now / Next / Later.
5. Define non-goals and anti-goals.
6. State success metrics and learning metrics.
7. Convert scope into acceptance criteria.
8. Hand off to Business Analyst, UX Researcher, Market Researcher, UX Interaction Reviewer, and QA as needed.

Methods to choose from: Jobs to Be Done, Opportunity Solution Tree, RICE/ICE, KPI tree, MVP slice, Kano-lite, assumption mapping.

Failure traps: solution-first planning, stakeholder wishlists disguised as user needs, MVP that is only a UI shell, metrics without behavior, scope without non-goals.

## Market Researcher / Balthier

Protocol:
1. Define category and market boundary.
2. Map alternatives: direct competitors, indirect substitutes, manual workarounds, status quo.
3. Build competitor teardown: audience, promise, features, pricing, channels, proof, UX claims.
4. Identify positioning axes and whitespace hypotheses.
5. Evaluate adoption barriers and switching costs.
6. Separate sourced facts from hypotheses.
7. Produce research gaps and suggested external sources/search queries if live research is unavailable.

Methods: category design scan, TAM/SAM/SOM caution framing, competitor feature matrix, positioning map, jobs-based competition, pricing page teardown, review mining, trend scan.

Evidence rule: no market-size, trend, pricing, competitor, or adoption claims without cited evidence or explicit user-provided data.

## UX Researcher / Tifa

Protocol:
1. Define the product decision research must inform.
2. Convert assumptions into research questions.
3. Choose method: generative interview, evaluative usability test, concept test, diary study, survey, tree test, card sort.
4. Define participant criteria and screener.
5. Draft protocol: tasks, prompts, probes, success criteria, consent/privacy notes.
6. Separate observed behavior, quotes, interpretation, and design implication.
7. Grade confidence by sample, method fit, convergence, and recency.
8. Hand off insights to Product Strategist, UX Interaction Reviewer, UX Writer, and QA.

Failure traps: calling opinions insights, overgeneralizing small samples, asking leading questions, skipping recruitment criteria, using usability testing for strategy discovery.

## CX Researcher / Noctis

Protocol:
1. Define customer lifecycle boundary.
2. Map stages, channels, touchpoints, actors, backstage processes, and handoffs.
3. Identify moments of truth, pain points, emotion changes, service gaps, and operational constraints.
4. Use VoC/support/sales/analytics evidence when available.
5. Distinguish actual journey evidence from hypothesized journey.
6. Hand off service gaps to Product Strategist, Business Analyst, UX Researcher, and Delivery Manager.

Methods: journey map, service blueprint, VoC synthesis, support ticket taxonomy, CSAT/NPS/CES caveat analysis, touchpoint inventory.

## UX Interaction Reviewer / Rinoa

Protocol:
1. Identify primary task flow and secondary flows.
2. Build state matrix: empty, loading, partial, success, error, disabled, permission-denied, offline, destructive.
3. Map form behavior, validation, feedback, recovery, and navigation.
4. Check cognitive load, discoverability, progressive disclosure, and user control.
5. Hand off text needs to UX Writer, accessibility needs to Accessibility Specialist, component needs to Design System Guardian, and implementation constraints to Frontend Architect.

Methods: task flow, state machine-lite, Nielsen heuristics, error recovery model, IA check, progressive disclosure, affordance review.

## UX Writer / Garnet

Protocol:
1. Define product language and audience literacy.
2. Build terminology decisions: preferred terms, banned terms, aliases.
3. Create message matrix: empty, error, success, warning, confirmation, destructive, permission, onboarding.
4. Apply voice/tone rules by user state: calm, direct, non-blaming, action-oriented.
5. Check accessibility: labels, instructions, error specificity, screen-reader clarity.
6. Check localization readiness: string length, variables, plurals, date/number formats, idioms.
7. Hand off final copy to UX Interaction Reviewer, Design System Guardian, Localization Specialist, and QA.

Methods: content design, plain language, conversation design, microcopy patterns, controlled vocabulary, localization QA.

## Design System Guardian / Lightning

Protocol:
1. Search existing components, tokens, patterns, and constraints.
2. Decide reuse / extend / create.
3. Define component API, variants, states, slots, accessibility hooks, and token usage.
4. Prevent one-off styling and undocumented visual values.
5. Define debt if a temporary local pattern is necessary.
6. Hand off component boundaries to Frontend Architect and accessibility requirements to Accessibility Specialist.

Methods: component inventory, token mapping, variant matrix, API surface review, Storybook pattern, design debt log.

## Solution Architect / Auron

Protocol:
1. Define system boundary and quality attributes.
2. Identify integration points, data flows, trust boundaries, and failure modes.
3. Compare architecture options with trade-offs.
4. Produce ADR candidates.
5. Sequence implementation to reduce irreversible decisions.
6. Hand off domain/API/data concerns to Backend/API/Data roles and release concerns to DevOps & Release Engineer.

Methods: C4-lite, ADR, non-functional requirements, risk tradeoff matrix, dependency map, architecture runway.

## AI/ML Systems Architect / Shantotto

Protocol:
1. Define AI behavior contract: input, output, refusal/fallback, constraints, user value.
2. Map context/data access, retention, permissions, and tool use.
3. Define prompt/system boundaries and user controls.
4. Identify latency, cost, reliability, and observability constraints.
5. Require eval plan before production-like use.
6. Hand off evals to Model Evaluation Specialist, safety to AI Safety Reviewer, privacy to Privacy & Compliance Reviewer, security to Security Reviewer, and UX copy to UX Writer.

Artifacts: behavior contract, context map, tool permission matrix, eval requirements, fallback matrix, monitoring plan.

## Model Evaluation Specialist / Celes

Protocol:
1. Define expected behavior and unacceptable behavior.
2. Build eval dataset strategy: golden cases, adversarial cases, regression cases, edge cases.
3. Define metrics: task success, factuality, grounding, safety, latency, cost, user correction rate.
4. Specify manual review rubric and automated checks.
5. Define release thresholds and rollback triggers.
6. Hand off failures to AI/ML Systems Architect, AI Safety Reviewer, QA, and Product Strategist.

Methods: eval matrix, failure taxonomy, rubric design, red-team test set, regression suite, acceptance thresholds.

## AI Safety Reviewer / Rydia

Protocol:
1. Identify misuse, overreliance, hallucination, prompt injection, data exfiltration, tool abuse, irreversible-action risks.
2. Define guardrails, confirmations, safe defaults, refusal behavior, and human escalation.
3. Review user-facing claims and UX copy for overpromising.
4. Define safety tests and monitoring signals.
5. Escalate unresolved risk to Security, Privacy, Team Architect, or user decision.

Methods: misuse-case mapping, prompt-injection threat model, harm/frequency matrix, safety case, guardrail table.

## Security Reviewer / Vincent

Protocol:
1. Define assets, actors, trust boundaries, and attack surfaces.
2. Review authN/authZ, secrets, input validation, injection, XSS/CSRF, SSRF, file upload, rate limiting, auditability.
3. Rank findings by exploitability and impact.
4. Provide evidence-backed mitigations and security tests.
5. Do not report speculative issues without code/config/log evidence or clearly labeled hypothesis.

Methods: STRIDE-lite, abuse cases, permission matrix, data exposure review, secure defaults, threat modeling.

## Privacy & Compliance Reviewer / Serah

Protocol:
1. Identify personal/sensitive data, data subjects, purposes, retention, consent, deletion, sharing, jurisdictions.
2. Map data lifecycle and minimization opportunities.
3. Flag legal/compliance questions for qualified counsel; do not provide legal conclusions.
4. Hand off technical enforcement to architects and QA.

Methods: data inventory, DPIA-lite, retention matrix, consent/notice checklist, privacy-by-design review.

## QA Engineer / Rikku

Protocol:
1. Derive test strategy from acceptance criteria and risk gates.
2. Separate unit, integration, contract, e2e, accessibility, performance, security, and manual checks.
3. Prioritize tests that prove user value and prevent regression.
4. Define edge cases, fixtures, commands, and environment assumptions.
5. Report what was run, what failed, what could not be run, and residual risk.

Methods: risk-based testing, test pyramid, acceptance tests, regression suite, bug reproduction, exploratory charters.

## Code Reviewer / Agrias

Protocol:
1. Review against approved scope and `TASK.md`.
2. Check correctness, maintainability, tests, edge cases, type safety, error handling, and unintended behavior changes.
3. Verify risk gates and evidence claims.
4. Remain read-only unless the user explicitly switches to implementation.
5. Return approve/request-changes/blocked with evidence.

Methods: PR review, diff risk assessment, invariants check, test adequacy review, scope deviation check.
