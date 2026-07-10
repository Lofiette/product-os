# Product Knowledge Quick Reference

Product Knowledge is optional and lazy. Canonical YAML lives under `.cpt/knowledge/artifacts/`; generated Markdown under `.cpt/knowledge/views/` is for reading and must not be edited as source.

## Hierarchy

```text
Product Map       -> where should the task look?
Area Map          -> what belongs to one product area?
Flow Map          -> how does one bounded behavior unfold?
Decision Record   -> what was decided and why?
API/Data Contract -> what frontend-facing contract constrains behavior?
Context Packet    -> what bounded context is needed for this task now?
```

## Modes

- `existing`: discover current behavior from current evidence.
- `greenfield`: record approved intent as planned/hypothesized and promote it as design, implementation, test, and runtime evidence appear.
- `redesign`: preserve current, target, and delta separately.

## Lifecycle

```text
planned -> confirmed -> validated
hypothesized -> inferred -> confirmed
confirmed/validated -> needs_review -> confirmed/validated
needs_review -> stale -> deprecated or reverified
```

The runtime enforces transitions and evidence rules. Generated analysis alone cannot confirm or validate a material claim.

## Core commands

```bash
python .cpt/bin/cpt_runtime.py knowledge-init ...
python .cpt/bin/cpt_runtime.py knowledge-status
python .cpt/bin/cpt_runtime.py knowledge-create ...
python .cpt/bin/cpt_runtime.py knowledge-claim-add ...
python .cpt/bin/cpt_runtime.py knowledge-claim-transition ...
python .cpt/bin/cpt_runtime.py knowledge-unknown-add ...
python .cpt/bin/cpt_runtime.py knowledge-link ...
python .cpt/bin/cpt_runtime.py knowledge-trigger-add ...
python .cpt/bin/cpt_runtime.py knowledge-stale-scan ...
python .cpt/bin/cpt_runtime.py knowledge-refresh ...
python .cpt/bin/cpt_runtime.py knowledge-packet-create ...
python .cpt/bin/cpt_runtime.py knowledge-task-assess ...
python .cpt/bin/cpt_runtime.py knowledge-render --all
python .cpt/bin/cpt_runtime.py knowledge-validate
```

## Task completion

Every new Standard Task records one of:

- `not_required`: no durable product knowledge changed;
- `planned`: updates are identified but incomplete;
- `applied`: required updates are complete;
- `deferred`: a bounded follow-up remains with rationale.

The runtime blocks completion while status is `not_assessed` or `planned`.

## Freshness

Review triggers use changed path globs and named events. Dependency propagation marks only affected artifacts `needs_review`. It does not reread or rewrite the whole knowledge base.

## Sanitization and sharing

Artifacts default to `internal` and `external_sharing: prohibited`. Reference secret locations rather than copying values. Before export:

```bash
python .cpt/bin/cpt_runtime.py knowledge-sanitize-check --external --artifact <id>
```

Use `knowledge-sharing-set` to record classification, redactions, notes, and sanitization status. Secret-pattern scanning is defense in depth, not a replacement for access control or repository secret scanners.

## Size policy

Target ranges are refactoring signals, not caps. Never truncate useful knowledge. If an artifact mixes abstraction levels, move lower-level detail to an existing child type and retain links plus a compact summary.
