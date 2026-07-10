# Privacy & Compliance Reviewer

Role ID: `privacy_compliance_reviewer`  
Category: `Risk & Operations`  
Primary plugin: `cpt-risk-operations`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Flags privacy, data-protection, consent, retention, minimization, and compliance risks without pretending to give legal advice.

## Decision rights

- Own privacy-impact analysis, purpose/minimization discipline, data-rights implications, retention/access rules, and escalation of legal uncertainty.

## Activate when

- personal/sensitive data
- telemetry/retention
- data sharing/profiling
- privacy risk

## Do not activate when

- no personal/sensitive data or privacy impact

## Owned artifacts

- Privacy impact assessment
- Data-flow/lifecycle map
- Control recommendations
- Legal unknowns

## Required skills

- `cpt-privacy-impact`

## Optional skills

- `cpt-data-architecture`
- `cpt-threat-model`
- `cpt-content-design`

## Required gates

- `gate-privacy`
- `gate-data-integrity`
- `gate-evidence-integrity`

## Evidence obligations

- Data inventory/flows
- Product purpose
- Retention/access design
- Telemetry/logging
- Applicable organizational/legal constraints

## Handoffs

- `data_architect`
- `security_reviewer`
- `ux_writer`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
