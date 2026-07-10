# Product Knowledge Schema Reference

## Artifact-level fields

| Field | Meaning |
|---|---|
| `schema_version` | Contract version expected by runtime validators. |
| `id` / `artifact_type` / `title` | Stable identity and canonical artifact category. |
| `mode` | `existing`, `greenfield`, or `redesign`. |
| `perspective` | `current`, `target`, `delta`, `planned`, or `mixed`. |
| `status` | Routing state: `draft`, `active`, `needs_review`, `stale`, `deprecated`. |
| `freshness` | Evidence freshness independent from artifact workflow status. |
| `confidence` | Overall artifact confidence; claim-level confidence remains authoritative for individual statements. |
| `scope` | Summary plus explicit in/out boundaries. |
| `owner_role` | One logical role accountable for the artifact. |
| `data_classification` | `public`, `internal`, `confidential`, or `restricted`. |
| `sharing` | External-sharing policy, sanitization state, redactions, and notes. |
| `source_revision` | Revision against which evidence was inspected. |
| `review_triggers` | Path/event conditions that invalidate current confidence. |
| `dependencies` | Typed edges to other knowledge artifacts. |
| `claims` | Falsifiable durable statements with lifecycle and evidence. |
| `unknowns` | Material unanswered questions, not hidden assumptions. |
| `size_guidance` | Soft profile and split strategy; never a truncation rule. |
| `content` | Artifact-type-specific structured payload. |

## Claim fields

A claim owns its own lifecycle, confidence, owner, evidence depth, evidence list, source revision, verification time, review triggers, and unknowns. Artifact confidence must never be used to silently promote a weaker claim.

## Evidence depth

Evidence depth describes where the claim was observed: approved decision, design artifact, source file, route, component, hook/store, API/type, test, runtime observation, external source, or other bounded evidence.

## Status versus lifecycle

Artifact `status` controls routing and review. Claim `lifecycle` controls epistemic state. An active artifact may contain planned or inferred claims, but material stale/needs-review claims should move the artifact out of `active` until reviewed.

## Canonical versus projection

YAML is canonical. Markdown projections are deterministic derived views. Any drift is a validation warning and must be repaired by regeneration, not by manually editing the view.
