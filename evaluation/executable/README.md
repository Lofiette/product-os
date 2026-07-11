# CPT OS Alpha 9 Executable Evaluation Plane

This directory contains executable, repository-isolated evaluations for the Runtime, Knowledge, Expertise, Enforcement, and Worker Orchestration planes.

## Evidence levels

- **Reference backend**: deterministic package-authored actions. Proves harness, policies, runtime contracts, fixtures, and graders. It does not certify model quality.
- **Live backend**: optional `codex exec --json` runner using the same fixtures, output schema, and graders.
- **External backend**: prepare a fixture for a trusted host or the official Codex GitHub Action, then grade its structured output and normalized JSONL trace.

## Suites

- `offline-core`: 20 required self-contained cases.
- `live-smoke`: a small optional live subset.
- `live-readonly`: optional live read-only cases.
- `live-full`: optional live cases including approved workspace writes.

## Commands

```bash
python tools/cpt_eval.py list
python tools/cpt_eval.py run --suite offline-core --backend reference --report-dir .cpt-eval-runs/offline
python tools/cpt_eval.py compare-baseline   --current .cpt-eval-runs/offline/offline-core-reference-scorecard.json   --baseline evaluation/executable/baselines/offline-core-alpha8.json
python tools/cpt_eval.py mutate   --scorecard .cpt-eval-runs/offline/offline-core-reference-scorecard.json   --output .cpt-eval-runs/offline/mutation-report.json
```

Live execution is optional:

```bash
python tools/cpt_eval.py run --suite live-smoke --backend live --report-dir .cpt-eval-live/smoke
```

If `codex` is absent, live cases are reported as `SKIPPED`. A non-zero `codex exec` exit is a failure, not a skip.

## Grading

Every case can constrain:

- reads and writes;
- required and forbidden commands;
- Git changes;
- runtime state;
- Product Knowledge freshness;
- worker quorum and worktree behavior;
- structured output;
- input/output tokens, tools, commands, writes, and elapsed time.

Critical violations cannot be hidden by an average score.

## Runtime artifacts

Generated reports belong under `.cpt-eval-runs/`, `.cpt-eval-live/`, or another external report directory. They are intentionally excluded from the immutable package manifest.
