---
name: cpt-privacy-impact
description: Use to map personal/sensitive data, purpose, access, sharing, retention, rights, consent, and privacy risk; not as legal advice.
---

# CPT Privacy Impact

## Use when

- A feature collects, derives, stores, shares, or deletes personal/sensitive data.

## Do not use when

- No personal or linkable data is involved.

## Required inputs

- Data inventory/flows, users/subjects, purpose, legal/compliance context, consent/notice, processors, access, retention, deletion, and security controls.

## Method

1. Classify data categories, sensitivity, subjects, source, purpose, necessity, and expected use.
2. Map collection, derivation, storage, access, sharing, cross-border movement, retention, deletion, backup, and logging.
3. Apply minimization, purpose limitation, access control, transparency, consent/choice, and user-rights analysis.
4. Identify inferred/profiling data, secondary use, model training, re-identification, and vulnerable-subject risks.
5. Review vendor/processors, contracts, incident response, and data localization where relevant.
6. Propose design and operational mitigations and determine when qualified legal/compliance review is needed.
7. Record residual risk and owner.

## Output contract

Produce a compact artifact containing:

- `Data inventory and flow map.`
- `Purpose/necessity/retention/access analysis.`
- `Privacy risks, mitigations, rights/notice needs, and residual risk.`
- `Escalation/approval requirements.`

## Evidence standard

- Legal conclusions must be escalated; the skill identifies issues and evidence.

## Stop and escalate

- Data purpose or retention cannot be justified.
- High-risk processing lacks qualified review.

## Failure modes to avoid

- Treating encrypted data as non-personal.
- Collecting fields “for future use”.
