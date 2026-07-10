---
name: cpt-knowledge-lifecycle
description: Use to create, validate, refresh, render, or update typed hierarchical Product Knowledge and task-specific context packets.
---

# CPT Knowledge Lifecycle

## Use when

- Onboarding an existing, greenfield, or redesign product.
- A task changes product areas, flows, decisions, frontend-facing contracts, or review triggers.
- Knowledge may be stale after code, design, product, API, or runtime changes.
- A task needs a bounded context packet rather than broad repository rereading.

## Do not use when

- A temporary finding belongs only in the active task.
- A Micro Change has no durable product implication.
- The requested output is an ungrounded product narrative.

## Required inputs

- `.cpt/knowledge/index.yaml` when initialized.
- Relevant canonical YAML artifacts, not the whole knowledge tree.
- Source revision, changed paths/events, user-approved decisions, and implementation/verification evidence.
- Active task knowledge-update status.

## Method

1. Choose mode: existing discovery, greenfield construction, redesign baseline/target/delta, targeted refresh, or post-task update.
2. Route from Product Map and Knowledge Index to the smallest affected artifacts.
3. Classify every durable claim as planned, hypothesized, inferred, confirmed, validated, needs_review, stale, or deprecated.
4. Attach evidence depth and source revision. Never upgrade certainty from prose alone.
5. Keep parent artifacts navigational and move lower-level detail to existing child types without deleting useful knowledge.
6. Use path/event review triggers and artifact dependencies for targeted freshness scans.
7. Update only affected artifacts, regenerate deterministic Markdown views, and record task knowledge-update status.
8. Before Standard Task completion, mark knowledge `not_required`, `applied`, or explicitly `deferred`.

## Runtime commands

```bash
python .cpt/bin/cpt_runtime.py knowledge-init ...
python .cpt/bin/cpt_runtime.py knowledge-create ...
python .cpt/bin/cpt_runtime.py knowledge-claim-add ...
python .cpt/bin/cpt_runtime.py knowledge-claim-transition ...
python .cpt/bin/cpt_runtime.py knowledge-stale-scan ...
python .cpt/bin/cpt_runtime.py knowledge-render --all
python .cpt/bin/cpt_runtime.py knowledge-validate
python .cpt/bin/cpt_runtime.py knowledge-task-assess ...
```

## Output contract

Return:

- artifacts created, updated, marked stale, deprecated, or left untouched;
- claim lifecycle/confidence changes and supporting evidence;
- source revisions, review triggers, dependencies, and unresolved unknowns;
- generated view status;
- compact task knowledge-update summary.

## Evidence standard

- Canonical project files, approved decisions, tests, and runtime observations outrank semantic recall or generated summaries.
- `validated` requires test or runtime-observation evidence.
- Greenfield knowledge must distinguish planned intent from implementation and validation.
- Redesign knowledge must distinguish current baseline, target, and delta.

## Stop and escalate

- A material claim has conflicting or untraceable evidence.
- Sensitive values are detected or sharing policy is incompatible with classification.
- Source revision is missing for a claim proposed as validated.
- The update requires a new artifact category or broad remap without approval.
- Canonical YAML and generated view disagree after regeneration.

## Failure modes to avoid

- Turning Product Map into an encyclopedia.
- Refreshing the whole knowledge base after a local change.
- Treating vector-search snippets as canonical evidence.
- Editing generated Markdown views instead of canonical YAML.
- Cutting useful knowledge merely to satisfy a target size.
- Exporting internal knowledge without an explicit sanitization review.


## Freshness enforcement

When hooks are trusted and enabled, project writes may trigger targeted freshness scans. Treat those marks as review signals, not automatic proof that knowledge is wrong. When hooks are unavailable, run a targeted stale scan before task completion if durable product behavior changed.
