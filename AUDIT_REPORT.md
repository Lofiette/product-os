# Codex Product Operating System 4.0 Alpha 8 Audit

## Release status

**Package status:** deterministic release gate passed. Final ZIP hash and extracted-archive verification are published in the external release audit.

**Version:** `4.0.0-alpha.8`

**Phase:** Executable Evaluation Plane and CI.

Alpha 8 adds an executable, repository-isolated Evaluation Plane on top of the Runtime, Product Knowledge, Expertise, Enforcement, and Managed Worker Orchestration planes delivered in Alpha 1–7.

## Scope delivered

Alpha 8 includes:

- 20 executable evaluation cases across six synthetic fixture repositories;
- four suites: `offline-core`, `live-smoke`, `live-readonly`, and `live-full`;
- a deterministic reference backend for self-contained release gating;
- an optional live backend using structured `codex exec --json` output;
- an external-fixture preparation and grading path for trusted hosts or CI;
- JSON Schema contracts for cases, task results, and scorecards;
- trace, output, filesystem, runtime, budget, and deterministic-rubric graders;
- reviewed offline baseline comparison;
- four intentional mutation checks;
- cross-platform offline CI configuration;
- an optional, manually triggered read-only live smoke workflow;
- package-manifest exclusions for generated reports and runtime evaluation state.

## Evaluation inventory

| Item | Count |
|---|---:|
| Executable cases | 20 |
| Fixture repositories | 6 |
| Evaluation suites | 4 |
| Evaluation unit tests | 13 |
| Known-bad mutations | 4 |
| Total behavioral unit tests across the package | 98 |

The required `offline-core` suite covers:

- micro copy changes;
- systemic edit-mode changes;
- design-system UI implementation;
- API-dependent UI;
- existing-product onboarding;
- greenfield product creation;
- redesign and migration;
- reference fidelity;
- accessibility review;
- approval and external-module boundaries;
- micro-to-standard escalation;
- security-sensitive API work;
- incident investigation;
- Product Knowledge freshness propagation;
- compaction recovery;
- required-worker timeout and quorum;
- parallel-worktree scope violations;
- skill metadata budget;
- local ignored runtime and Git cleanliness.

## Deterministic release evidence

The reviewed reference baseline records:

```text
Cases:                    20 / 20 PASS
Average score:            100
Tool events:              119
Commands:                  71
Reads:                     38
Writes:                    10
Approval events:            4
Changed files:               5
Input tokens:           24,060
Output tokens:           6,170
```

Wall time is enforced by each case budget but is intentionally not used as a portable cross-platform regression baseline.

Baseline comparison must report:

```text
Status: PASS
Regressions: 0
```

Mutation testing must detect all four known-bad behaviors:

```text
unauthorized write
missing required output field
forbidden destructive command
resource regression
```

Expected result:

```text
Mutations detected: 4 / 4
```

## Package-wide regression evidence

Expected package checks:

```text
Distribution tests:       18 / 18
Skill tests:               5 / 5
Role tests:                4 / 4
Product Knowledge tests: 13 / 13
Enforcement tests:        21 / 21
Orchestration tests:      24 / 24
Evaluation Plane tests:   13 / 13
--------------------------------
Total:                    98 / 98
```

Expected deterministic reports:

```text
Skill trigger proxy:         135 / 135
Role routing proxy:          164 / 164
Knowledge lifecycle:          11 / 11
Enforcement policy:            5 / 5
Orchestration policy:          34 / 34
Enforcement integration:      13 / 13
Orchestration integration:    16 / 16
```

## Grading model

Each evaluation case is independently checked across six dimensions:

1. trace policy;
2. structured output contract;
3. actual filesystem changes;
4. runtime assertions;
5. token, tool, command, write, and wall-time budgets;
6. deterministic evidence and bounded-change rubric.

Critical failures cannot be averaged away. A forbidden write, destructive command, invalid structured result, or runtime-integrity failure forces a case failure regardless of the average score.

## Isolation and evidence quality

Every case runs in a fresh temporary Git repository with isolated `HOME` and `CODEX_HOME` directories. Only the plugins and optional worker pack explicitly requested by the case are projected into the fixture.

The reference backend emits a synthetic Codex-like trace authored by the package. It proves fixture setup, runtime contracts, graders, policies, and regression detection. It does **not** certify live model quality.

The live backend:

- requires a Codex CLI and credentials;
- requests schema-conforming final output;
- normalizes supported JSONL command, file-change, message, error, and usage events;
- marks structured model claims about reads and writes as reported evidence;
- corroborates actual writes with Git state where possible;
- treats a non-zero Codex exit as failure, not as skipped evidence.

## CI posture

The offline workflow uses least-privilege repository permissions and runs the required suite on:

- Ubuntu with Python 3.10;
- Ubuntu with Python 3.12;
- macOS with Python 3.12;
- Windows with Python 3.12.

The primary Linux/Python job also runs the complete package regression suite. Generated scorecards, comparisons, and mutation reports are uploaded as CI artifacts rather than added to the immutable package tree.

The optional live-smoke workflow is manual and read-only. It requires a trusted credential and organizational review; it is not part of the self-contained release gate.

## Packaging integrity requirements

The final distribution must satisfy all of the following:

- ZIP inventory exactly matches `MANIFEST.json` plus `MANIFEST.json` itself;
- every managed file size and SHA-256 matches the manifest;
- generated evaluation reports are excluded;
- `.cpt-eval-runs` and `.cpt-eval-live` are excluded;
- `__pycache__`, `.pyc`, `.pyo`, and tool caches are excluded;
- validators do not create bytecode inside the package tree;
- the package can be extracted into a clean directory and revalidated there;
- local installation, doctor, runtime validation, offline evaluations, baseline comparison, mutation checks, and Git-clean verification pass from the extracted copy.

The archive SHA-256 is published in the external release audit because a ZIP cannot safely contain its own final hash without creating a circular artifact dependency.

## Known limitations

Alpha 8 does not claim live-model certification in the build environment.

The following still require external live runs:

- model decision quality across supported models;
- actual token and latency budgets;
- native subagent event ordering;
- cancellation delivery by the host;
- reconnect behavior across Codex clients;
- screenshot- or image-based visual grading;
- behavioral consistency under real interactive approvals.

JSONL event normalization is best effort and may need updates when Codex event schemas evolve. Missing native trace evidence is surfaced as reduced observability rather than silently converted into proof.

## Release conclusion

Alpha 8 passed the deterministic Evaluation Plane release gate with:

- all 98 behavioral tests passed;
- all static validators passed;
- `offline-core` reported 20/20 PASS;
- baseline comparison reported zero regressions;
- mutation testing detected 4/4 known-bad behaviors;
- the final ZIP inventory and hashes were exact;
- extracted-package static, installation, doctor, runtime, Git-cleanliness, and representative evaluation checks passed.

Live scorecards are additive evidence and must remain clearly separated from deterministic package certification.
