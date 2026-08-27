---
name: cpt-professional-data-interface-design
description: Use to design dense professional data interfaces, bulk actions, keyboard workflows, permissions, and partial-failure recovery.
---

# CPT Professional Data Interface Design

## Use when

- Experienced users repeatedly inspect, compare, edit, approve, monitor, or act on many records.
- The interface contains dense lists/tables, bulk selection, advanced filters, dashboards, exceptions, queues, linked visualizations, or multi-object workspaces.
- Novice learnability must coexist with expert speed, keyboard operation, role/permission variation, auditability, and high data volume.

## Do not use when

- The task is a simple consumer page, short form, or isolated visualization with no professional workflow.
- Metric semantics are unresolved; use `cpt-data-visualization-review` or the data owner first.
- Only styling of an approved table component remains.

## Required inputs

- User roles, expertise, frequency, throughput, decisions, and consequences.
- Object/data model, volume, cardinality, relationships, freshness, quality, and permissions.
- Selection, bulk-action, exception, review, audit, and partial-success semantics.
- Existing components, tokens, responsive constraints, keyboard conventions, and technical limits.
- Operational evidence: task observation, support issues, error rates, latency, and current workarounds.

## References and selective loading

1. Read `references/PROFESSIONAL_INTERFACE_POLICY.md`.
2. Use `references/PROFESSIONAL_TASK_MATRIX.yaml` to classify the workflow.
3. Use `references/PROFESSIONAL_REVIEW_CHECKLIST.md` before acceptance.
4. Invoke `cpt-interaction-pattern-selection`, `cpt-form-task-flow-design`, and `cpt-data-visualization-review` only for the relevant subproblem.

## Method

1. Define the professional decision and unit of work: what the user must notice, compare, decide, change, and verify per minute, hour, or case.
2. Model objects, fields, hierarchy, selection identity, permissions, lifecycle, freshness, exceptions, and audit requirements before choosing a table, cards, dashboard, or workspace.
3. Classify the workflow: monitor/triage, browse/compare, review/approve, configure, create repeatedly, investigate linked data, or operate a multi-workspace tool.
4. Define the novice-to-expert progression. Keep essential conventions discoverable while providing shortcuts, bulk operations, saved views, templates, history, and customization only where repeated work justifies them.
5. Design density from task value. Preserve comparison columns, stable alignment, spatial memory, and scan paths; remove decorative chrome and accidental complexity rather than useful data.
6. Specify search, sort, filters, grouping, column configuration, pagination/virtualization, selection scope, and action scope. Make hidden-row and cross-page effects explicit.
7. Specify command hierarchy, keyboard model, focus, repeat-last, macros/templates, undo/cancel, review, audit, and destructive boundaries.
8. Design loading, empty, stale, offline, conflict, permission, partial result, partial failure, and extreme-data behavior. Never collapse partial success into a generic success state.
9. For dashboards and linked data, map every metric/visual to a decision, expose definitions and freshness, synchronize selection deliberately, and provide exact values plus accessible alternatives.
10. Stress performance, narrow widths, zoom, long/localized data, many columns, many selections, role changes, latency, and interrupted sessions.
11. Produce implementation and acceptance evidence, including representative realistic datasets and keyboard/throughput tests.

## Output contract

Produce a `Professional Interface Contract` containing:

- `Decision cadence, users, throughput, risk, and workflow classification.`
- `Object/data/selection/permission model and representative data.`
- `Information architecture, density, comparison, and responsive model.`
- `Search/filter/sort/group/column/selection/action semantics.`
- `Keyboard, shortcuts, bulk, repeat, undo/cancel, audit, and recovery.`
- `Dashboard/linked-view mapping where applicable.`
- `State/extreme-data/performance matrix and acceptance evidence.`
- `Novice/expert trade-offs, residual risks, gates, and falsification criteria.`

## Evidence standard

- More whitespace is not automatically simpler, and more density is not automatically expert-friendly.
- A table is justified by comparison and operations, not by the existence of rows in a database.
- A dashboard is justified by decisions and action, not by available metrics.
- Throughput claims require observed workflow or test evidence.

## Stop and escalate

- Metric, selection, permission, audit, or source-of-truth semantics are unresolved.
- Bulk or automated actions cross an unapproved risk boundary.
- Performance constraints make the proposed data model infeasible without engineering ownership.

## Failure modes to avoid

- Cardifying structured rows and destroying comparison.
- Hiding frequent expert actions to make the screen look clean.
- Ambiguous select-all scope across filters/pages.
- Pointer-only row actions or hover-only critical controls.
- Losing sort/filter/selection/workspace state after inspection or error.
- Treating partial failure as success or forcing full restart.
- Building dashboards with undefined metrics or no route to action.
