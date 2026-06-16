# Models Area Map

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: first compact map for Models from approved Phase 2, Phase 3A, and Phase 3B route evidence
evidence:
- Phase 2 path-only scan
- Phase 3A app shell/auth reads
- Phase 3B batch: `src/app/models/page.tsx`, `src/app/models/new/page.tsx`, `src/app/models/[modelName]/page.tsx`
unknowns:
- `ModelList` and `ModelForm` internals are not read.
- Model provider/type/configuration fields and validation need verification.
review_trigger: changes to model routes, model list/form components, or model configuration behavior

## Area Summary

Models appears to cover model listing, model creation entry, and model detail/edit by model name.

Claim status: confirmed for route surfaces; model semantics need verification. Confidence: medium.

## Confirmed Surfaces

| Surface | Purpose | Claim status | Confidence |
|---|---|---|---|
| `/models` | Model list surface rendering `ModelList` | confirmed | high |
| `/models/new` | Model creation entry using `ModelList initialCreateOpen` | confirmed | high |
| `/models/[modelName]` | Model detail/edit surface using decoded model name | confirmed | high |

## Actors And Access

| Claim | Claim status | Confidence |
|---|---|---|
| Models is inside authenticated workspace chrome when auth is required. | confirmed | high |
| Primary actor likely configures models used by workflows. | inferred | medium |

## Candidate Flows For Future Flow Maps

| Future flow map | Current status | Next evidence needed |
|---|---|---|
| `models/view-list` | placeholder | `src/components/models/ModelList.tsx` |
| `models/create` | placeholder | `ModelList` create mode |
| `models/edit` | placeholder | `src/components/models/ModelForm.tsx` |
| `models/close-create` | placeholder | behavior for `closeCreateHref="/models"` |

## Where To Look Next

- To understand list/create behavior: `src/components/models/ModelList.tsx`
- To understand model detail/edit behavior: `src/components/models/ModelForm.tsx`
