# Executable Evaluation Plane

Beta 1 turns CPT scenarios into executable, repository-isolated evaluations. Each case defines a fixture repository, task prompt, activation profile, allowed and forbidden actions, expected runtime state, output contract, and resource budgets.

## Evidence levels

- **Reference backend** executes package-authored actions and emits a synthetic Codex-like JSONL trace. It proves the harness, fixtures, runtime contracts, policies, and graders. It does **not** certify live model quality.
- **Live backend** optionally invokes `codex exec --json` in an isolated fixture, requests schema-conforming final output, and grades the resulting JSONL event stream and Git state.
- **External backend** prepares a portable fixture for a trusted host or CI action and grades returned structured output plus an optional normalized trace.

## Suites

| Suite | Required | Backend | Purpose |
|---|---:|---|---|
| `offline-core` | yes | reference | All 21 deterministic release-gate cases. |
| `live-smoke` | no | live | Small live checks for bounded read-only and micro work. |
| `live-readonly` | no | live | Read-only reasoning, review, and planning behavior. |
| `live-full` | no | live | Optional full behavior set including approved workspace writes. |

## Coverage

The 21 cases cover:

- micro copy change;
- systemic edit-mode change;
- design-system UI implementation;
- API-dependent UI;
- existing-product onboarding;
- greenfield product creation;
- redesign or migration;
- reference fidelity;
- accessibility review;
- approval boundaries;
- external-module boundaries;
- micro-to-standard escalation;
- security-sensitive API work;
- incident investigation;
- Product Knowledge stale propagation;
- compaction recovery;
- required-worker timeout and quorum;
- parallel-worktree scope violation;
- skill metadata budget;
- local ignored runtime and Git cleanliness.
- offline release-readiness contract.

## Required offline release gate

```bash
python tools/validate_evaluation.py
python tools/cpt_eval.py run   --suite offline-core   --backend reference   --report-dir .cpt-eval-runs/offline
python tools/cpt_eval.py compare-baseline   --current .cpt-eval-runs/offline/offline-core-reference-scorecard.json   --baseline evaluation/executable/baselines/offline-core-alpha8.json   --output .cpt-eval-runs/offline/baseline-comparison.json
python tools/cpt_eval.py mutate   --scorecard .cpt-eval-runs/offline/offline-core-reference-scorecard.json   --output .cpt-eval-runs/offline/mutation-report.json
```

Generated reports belong under `.cpt-eval-runs/`, `.cpt-eval-live/`, or another external report directory. They are intentionally excluded from the immutable package manifest.

## Run selected cases

```bash
python tools/cpt_eval.py run   --suite offline-core   --backend reference   --report-dir /tmp/cpt-eval   --case systemic_edit_mode_change   --case api_dependent_ui
```

## Optional live Codex execution

```bash
python tools/cpt_eval.py run   --suite live-smoke   --backend live   --report-dir .cpt-eval-live/smoke
```

If the Codex CLI is unavailable, live cases are `SKIPPED`. A non-zero `codex exec` exit is a failure, not a skip.

## External execution

```bash
python tools/cpt_eval.py prepare-external   --case reference_fidelity   --output-dir /tmp/cpt-external
```

After execution on a trusted host:

```bash
python tools/cpt_eval.py grade-external   --case reference_fidelity   --workspace /tmp/cpt-external/workspace   --output /tmp/cpt-external/output.json   --trace /tmp/cpt-external/trace.jsonl   --report /tmp/cpt-external/graded.json
```

A missing trace reduces observability. Structured model claims about file activity remain marked as reported evidence; actual writes are corroborated through Git state where possible.

## Graders

Every case is checked across six dimensions:

1. trace policy;
2. structured output contract;
3. actual filesystem changes;
4. runtime assertions;
5. token, tool, write, and wall-time budgets;
6. deterministic evidence and bounded-change rubric.

Critical failures cannot be averaged away:

- forbidden write;
- forbidden destructive command;
- invalid output schema;
- runtime integrity failure.

## Baseline and mutations

The reviewed baseline is:

```text
evaluation/executable/baselines/offline-core-alpha8.json
```

Comparison detects missing cases, status or score regression, and token/tool/command/write regressions. Wall time is enforced by each case budget but is not used as a portable cross-platform baseline.

Four known-bad mutations must be detected:

- unauthorized write;
- missing required output field;
- forbidden destructive command;
- resource regression.

## CI

`.github/workflows/offline-evals.yml` runs the required deterministic suite on Linux, macOS, and Windows. The primary Linux/Python job also runs the complete package regression suite.

`.github/workflows/live-smoke.yml` is manual and optional. It executes a bounded read-only case through the official Codex GitHub Action and grades the structured output. Reduced trace visibility is reported rather than hidden.
