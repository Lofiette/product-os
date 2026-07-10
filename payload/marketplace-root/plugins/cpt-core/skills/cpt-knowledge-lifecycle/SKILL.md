---
name: cpt-knowledge-lifecycle
description: Use to create, validate, refresh, or update hierarchical Product Knowledge; not as a substitute for current code or task evidence.
---

# CPT Knowledge Lifecycle

## Use when

- Onboarding an existing, greenfield, or redesign product.
- A completed task changes product areas, flows, decisions, contracts, or review triggers.
- Knowledge may be stale after code or product changes.

## Do not use when

- The task does not affect durable product knowledge.
- A temporary finding belongs only in the active task or context packet.

## Required inputs

- Knowledge artifact registry and schemas.
- Source revision, changed paths, user-approved decisions, and implementation/verification evidence.
- Existing confidence, freshness, unknowns, and review triggers.

## Method

1. Choose lifecycle mode: existing discovery, greenfield creation, redesign delta, targeted refresh, or post-task update.
2. Route from Product Map to the smallest affected area, flow, decision, contract, or context packet.
3. Classify each claim as planned, hypothesized, inferred, confirmed, validated, needs-review, stale, or deprecated.
4. Attach evidence depth and source revision; never upgrade confidence from prose alone.
5. Update only affected artifacts and preserve unknowns that remain unresolved.
6. Keep parent artifacts navigational; move detail to child artifacts without deleting useful knowledge to meet size targets.
7. Mark review triggers using paths or decisions that can be checked later.
8. Summarize the durable change in runtime state without copying the full artifact.

## Output contract

Produce a compact artifact containing:

- `Artifacts created, updated, marked stale, or left untouched.`
- `Claim-level confidence/freshness changes and evidence.`
- `Review triggers and unresolved unknowns.`
- `Compact knowledge-update summary for task completion.`

## Evidence standard

- Canonical files and approved decisions outrank semantic recall or generated summaries.
- Greenfield knowledge must distinguish planned from implemented and validated.

## Stop and escalate

- Source revision is unknown for a material claim.
- Conflicting evidence cannot be reconciled.
- The update would require a new artifact category or broad remap without approval.

## Failure modes to avoid

- Turning Product Map into an encyclopedia.
- Refreshing the whole knowledge base after a local change.
- Treating vector-search snippets as canonical evidence.
