---
name: cpt-task-planning
description: Use to discover bounded scope, select expertise, build an Impact Map, and request one approval lease before meaningful work.
---

# CPT Task Planning

## Use when

- A non-trivial task needs evidence, affected-scope discovery, expertise routing, or implementation approval.
- The user should not have to list every relevant file manually.

## Do not use when

- A Micro Change is obvious, local, reversible, low-risk, and has clear verification.
- The exact scope and lease are already approved and no new unknown appeared.

## Required inputs

- User outcome and active task acceptance criteria.
- Current Product Knowledge, repository boundaries, and runtime policy.
- Allowed discovery classes, context/tool budget, risk triggers, and available plugin catalog.

## Method

1. Restate the user outcome independently of any assumed implementation.
2. Define the decision-changing unknowns and a bounded read-only discovery envelope.
3. Start with paths, entrypoints, routes, symbols, manifests, or dependency edges; open only the smallest evidence set needed.
4. Separate confirmed, inferred, absent, and unknown findings. Stop when the plan is trustworthy, not when the repository is exhausted.
5. Map affected product areas, flows, users, contracts, shared patterns, files, and runtime knowledge.
6. Classify impact as local, shared-pattern, cross-area, API/data, migration, risk-sensitive, or unresolved.
7. Select the smallest plugins, skills, logical roles, gates, and execution mode that own distinct decisions or artifacts.
8. Prefer main-thread role lenses for tightly coupled work; propose workers only for independent bounded artifacts.
9. Define behavior, quality, regression, and knowledge-freshness verification.
10. Produce one Impact Map and request a scoped authorization lease for reads, writes, commands, delegation, forbidden operations, and expiry.

## Output contract

Produce a compact artifact containing:

- `Outcome and task boundary`
- `Discovery commands/files and deliberately excluded scope`
- `Confirmed findings, assumptions, and unknowns`
- `Affected-area/file/contract table with reason and confidence`
- `Selected plugins, skills, logical roles, gates, and execution mode`
- `Risks, rejected alternatives, verification, and knowledge updates`
- `Scoped approval lease request`

## Evidence standard

- Path names support candidates, not behavior claims.
- Every affected area or file needs a source: Product Knowledge, search result, import edge, contract, runtime evidence, or user decision.
- A selected capability must change a decision, artifact, risk gate, or verification step.

## Stop and escalate

- Unknowns could materially change product behavior, architecture, data, or risk.
- Discovery would exceed the approved path, depth, file, or output budget.
- Required plugin/skill is unavailable or metadata budget would be exceeded.
- The requested lease is broader than the evidence supports.

## Failure modes to avoid

- Broad repository scans before a decision question exists.
- Listing files without explaining systemic impact.
- Loading all roles or skills “just in case”.
- Treating every logical role as a worker.
- Performing an Impact Map as ceremony after implementation has already started.

## Expertise routing references

Use the canonical role layer only after the task profile and meaningful decisions are known:

- `references/EXPERTISE_BUNDLE.json`, which contains the compact role router, task profiles, selected deep methods, and gate contracts.

Routing procedure:

1. Choose the nearest routing profile.
2. Name the decisions and artifacts that require ownership.
3. Assign exactly one accountable role to each meaningful decision or artifact.
4. Add supporting roles only when they change evidence, risk detection, gate ownership, or independent challenge.
5. Use the compact router first. Consult deep method entries only for accountable owners or material specialists.
6. Validate that selected roles map to available canonical skills and required gates.
7. Keep roles in the main thread by default. Worker eligibility is not spawn permission.
8. Report skipped roles and stop conditions.

Do not install or invent one custom agent per logical role.

