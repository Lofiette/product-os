# Workflows Area Map

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: first compact map for Workflows / Flow editor from approved Phase 2, Phase 3A, and Phase 3B evidence
evidence:
- Phase 2 path-only scan
- Phase 3A: `src/app/layout.tsx`, `src/app/page.tsx`, `src/components/layout/AppShell.tsx`, `src/components/layout/Header.tsx`, `src/components/auth/AuthGuard.tsx`
- Phase 3B: `src/app/flows/page.tsx`, `src/app/flows/new/page.tsx`, `src/app/flows/[flowName]/page.tsx`
unknowns:
- `FlowList`, `GraphEditor`, `ExecutionDialog`, hooks, store, API, and detailed validation behavior are not read yet.
- Creation/save/rename/delete behavior needs verification.
- Detailed DSL semantics are not mapped.
review_trigger: changes to workflow routes, editor header, flow editor hooks/components, execution dialog, or DSL shape

## Area Summary

Workflows appears to cover listing workflows, creating a new workflow, editing a workflow as a graph, validating/saving it, and running an existing workflow.

Claim status: inferred from approved route files and app shell evidence. Confidence: medium.

## Confirmed Surfaces

| Surface | Purpose | Claim status | Confidence |
|---|---|---|---|
| `/flows` | Workflow list surface rendering `FlowList` | confirmed | high |
| `/flows/new` | New workflow graph editor | confirmed | high |
| `/flows/[flowName]` | Existing workflow graph editor | confirmed | high |
| `/` | Redirects to `/flows` | confirmed | high |

## Actors And Access

| Claim | Claim status | Confidence |
|---|---|---|
| Workflows are inside authenticated workspace chrome when auth is required. | confirmed | high |
| Primary actor is likely a workflow builder/operator. | inferred | medium |
| Editor pages hide global workspace navigation. | confirmed | high |

## Visible States And Modes

| State / Mode | Claim status | Confidence |
|---|---|---|
| New workflow starts from an initialized graph with start and end nodes. | confirmed | high |
| New workflow title is `Новый рабочий процесс`. | confirmed | high |
| Existing workflow title comes from route `flowName`. | confirmed | high |
| Editor supports save and validate actions. | confirmed | high |
| Existing workflow editor supports run action. | confirmed | high |
| Run can be disabled when validation state is invalid. | confirmed | medium |
| Save/loading/dirty states exist. | confirmed | medium |
| Execution result may create a trace path/error-node status in editor context. | confirmed | medium |

## Candidate Flows For Future Flow Maps

| Future flow map | Current status | Next evidence needed |
|---|---|---|
| `flows/view-list` | placeholder | `src/components/flows/FlowList.tsx` |
| `flows/create-new` | placeholder | `useFlowEditor`, save behavior, `FlowList` entry points |
| `flows/edit-existing` | placeholder | `GraphEditor`, `useFlowEditor`, editor store |
| `flows/validate` | placeholder | `useValidation`, validation utilities/API |
| `flows/run-existing` | placeholder | `ExecutionDialog`, execution API, run result shape |
| `flows/return-to-list` | placeholder | already partly confirmed by route files |

## Boundaries

Inside current area map:

- workflow list route
- new workflow route
- existing workflow editor route
- top-level save/validate/run affordances
- high-level editor/session states visible in approved files

Outside current area map until approved:

- detailed `GraphEditor` internals
- full DSL semantics
- API persistence behavior
- flow run history behavior
- component palette and property panels
- validation implementation

## Where To Look Next

- To understand the list surface: `src/components/flows/FlowList.tsx`
- To understand editor composition: `src/components/editor/GraphEditor.tsx`
- To understand run behavior: `src/components/execution/ExecutionDialog.tsx`
- To understand save/load behavior: `src/lib/hooks/useFlowEditor.ts`
- To understand validation: `src/lib/hooks/useValidation.ts`
