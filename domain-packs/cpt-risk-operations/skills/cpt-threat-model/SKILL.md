---
name: cpt-threat-model
description: Use for security threat modeling and evidence-backed security review of trust boundaries, assets, abuse cases, controls, and tests.
---

# CPT Threat Model

## Use when

- A change affects authentication, authorization, sensitive data, external input, tools/actions, payments, or trust boundaries.

## Do not use when

- No meaningful security surface changes.

## Required inputs

- Architecture/data flows, assets, actors, trust boundaries, entrypoints, deployment, identities, secrets, dependencies, and controls.

## Method

1. Define assets, security objectives, actors, trust boundaries, and assumptions.
2. Map data/control flows, entrypoints, privileged actions, dependencies, and attack surface.
3. Apply STRIDE/abuse-case analysis appropriate to the system.
4. Evaluate authentication, authorization, isolation, input handling, secrets, cryptography, logging, supply chain, and availability.
5. Rate likelihood/impact and distinguish exploit path from generic best practice.
6. Select mitigations using prevention, detection, response, and least privilege.
7. Define security tests and residual-risk acceptance owner.

## Output contract

Produce a compact artifact containing:

- `Threat model diagram/table.`
- `Threats, abuse cases, severity, evidence, and affected assets.`
- `Mitigations, tests, owners, and residual risk.`
- `PASS/WARN/BLOCKED security verdict.`

## Evidence standard

- A threat must connect actor, precondition, action, asset, and impact.

## Stop and escalate

- Architecture/trust boundaries are too unclear.
- High residual risk lacks owner approval.

## Failure modes to avoid

- Security checklist without data flows.
- Calling every theoretical issue critical.
