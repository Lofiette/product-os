---
name: cpt-ai-safety-review
description: Use to review AI-specific misuse, harmful behavior, prompt injection, tool abuse, uncertainty, escalation, and safety controls.
---

# CPT AI Safety Review

## Use when

- AI generates consequential content, accesses private context, or can call tools/actions.

## Do not use when

- The system is deterministic and has no AI behavior.

## Required inputs

- AI behavior/tool contract, users, data/context, threat model, domains, policies, evaluation evidence, and operational controls.

## Method

1. Identify affected users, foreseeable misuse, harmful outputs/actions, and high-impact failure modes.
2. Map prompt injection, data exfiltration, instruction conflicts, tool escalation, autonomy, and irreversible action paths.
3. Review uncertainty communication, refusal, safe completion, confirmation, fallback, and human oversight.
4. Define content/action boundaries, permissions, rate limits, monitoring, and abuse response.
5. Create adversarial and safety eval cases across relevant risk slices.
6. Assess residual risk, deployment constraints, incident response, and stop criteria.

## Output contract

Produce a compact artifact containing:

- `AI safety hazard/abuse-case register.`
- `Controls and human-oversight design.`
- `Safety eval cases and monitoring.`
- `PASS/WARN/BLOCKED verdict with residual risk.`

## Evidence standard

- Safety claims require behavior/eval evidence, not policy text alone.

## Stop and escalate

- High-impact action lacks confirmation/rollback/human control.
- Safety evaluation cannot cover the intended domain.

## Failure modes to avoid

- Treating generic content filtering as complete safety.
- Ignoring prompt injection because the model is “internal”.
