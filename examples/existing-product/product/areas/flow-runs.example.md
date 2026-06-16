# Flow Runs Area Map

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: first compact map for Flow runs from approved Phase 2, Phase 3A, and Phase 3B route evidence
evidence:
- Phase 2 path-only scan
- Phase 3A app shell/auth reads
- Phase 3B batch: `src/app/flow-runs/page.tsx`
unknowns:
- `FlowRunsPage` internals are not read.
- Run statuses, filters, result details, and relationship to workflow execution need verification.
review_trigger: changes to `/flow-runs`, flow run components, execution dialog, or run history behavior

## Area Summary

Flow runs appears to be the top-level area for viewing workflow execution runs.

Claim status: inferred from route name, nav label `Запуски`, and `FlowRunsPage`. Confidence: medium.

## Confirmed Surfaces

| Surface | Purpose | Claim status | Confidence |
|---|---|---|---|
| `/flow-runs` | Flow runs surface rendering `FlowRunsPage` | confirmed | high |

## Actors And Access

| Claim | Claim status | Confidence |
|---|---|---|
| Flow runs is inside authenticated workspace chrome when auth is required. | confirmed | high |
| Primary actor likely reviews workflow execution history/results. | inferred | medium |

## Candidate Flows For Future Flow Maps

| Future flow map | Current status | Next evidence needed |
|---|---|---|
| `flow-runs/view-list` | placeholder | `src/components/flow-runs/FlowRunsPage.tsx` |
| `flow-runs/inspect-run` | placeholder | run details component/API evidence |
| `flow-runs/from-workflow-run` | placeholder | `ExecutionDialog` and run history evidence |

## Where To Look Next

- To understand run list/status/result behavior: `src/components/flow-runs/FlowRunsPage.tsx`
- To connect workflow execution to run history: `src/components/execution/ExecutionDialog.tsx`
