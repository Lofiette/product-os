# Codex Product Operating System 4.0 Alpha 8

## External Release Audit

**Version:** `4.0.0-alpha.8`  
**Phase:** Executable Evaluation Plane and CI  
**Release status:** deterministic Alpha release gate passed  

## Final archive

```text
File: codex-product-os-4.0-alpha8-evaluation-v0.8.zip
Size: 727,004 bytes
SHA-256: d8f3df3033b96f08e212da8fdfd89bfd4ff9d1f66e1b7398b47d9bdfb0148a48
Managed manifest files: 504
ZIP members: 505 (504 managed files + MANIFEST.json)
```

ZIP CRC validation passed. ZIP inventory exactly matches `MANIFEST.json` plus the manifest itself.

## Package-wide release evidence

The final monolithic release suite completed successfully with exit code `0` and the final marker:

```text
ALPHA 8 COMPLETE TEST SUITE PASSED: 98 behavioral cases
```

Behavioral tests:

```text
Distribution:       18 / 18
Skills:              5 / 5
Roles:               4 / 4
Product Knowledge:  13 / 13
Enforcement:         21 / 21
Orchestration:       24 / 24
Evaluation Plane:   13 / 13
--------------------------------
Total:              98 / 98
```

Deterministic evaluation evidence:

```text
Offline executable cases:      20 / 20 PASS
Average deterministic score:   100
Baseline comparison:           PASS
Regressions:                   0
Known-bad mutations detected:  4 / 4
```

Supporting expert/runtime reports:

```text
Skill trigger proxy:        135 / 135
Role routing proxy:         164 / 164
Knowledge lifecycle:         11 / 11
Enforcement policy:           5 / 5
Orchestration policy:         34 / 34
Enforcement integration:     13 / 13
Orchestration integration:   16 / 16
```

## Static and integrity validation

Passed on the final source tree and again from the extracted ZIP:

```text
Distribution validation
Evaluation asset validation
Skill validation
Role validation
Product Knowledge asset validation
Product Knowledge runtime validation
Enforcement validation
Orchestration validation
Python syntax validation without bytecode generation
JavaScript/MJS syntax validation
Package universality scan
Manifest size/hash/inventory validation
Bytecode/cache exclusion
```

## Extracted-package checks

The final archive was extracted into a clean directory. The extracted package passed:

```text
all static validators;
local-mode installation in an isolated Git repository;
doctor;
runtime validation;
Git-cleanliness verification;
representative executable evaluations:
  - micro_copy_change: PASS, score 100
  - compaction_recovery: PASS, score 100
```

The complete `offline-core` suite had already passed 20/20 in the final monolithic source-tree release run. The representative extracted checks verify that packaging, extraction, installation, and evaluation execution remain operational from the ZIP without claiming a second redundant full 20-case run.

## Alpha 8 scope delivered

Alpha 8 turns the previous scenario layer into an executable Evaluation Plane:

- 20 executable cases;
- six synthetic fixture repositories;
- four suites: `offline-core`, `live-smoke`, `live-readonly`, `live-full`;
- deterministic reference backend;
- optional `codex exec --json` live backend;
- external fixture preparation and grading;
- JSON Schema output contracts;
- trace, output, filesystem, runtime, budget, and deterministic-rubric graders;
- reviewed regression baseline;
- mutation testing;
- cross-platform offline CI;
- optional manual live-smoke workflow.

## Final defects caught before release

The release process caught and fixed several real packaging/evaluation defects:

1. Generated evaluation reports initially conflicted with immutable manifest inventory.
2. Python validators using `py_compile` polluted the package tree with `__pycache__` and `.pyc`; validation now uses non-polluting AST parsing.
3. An early manifest became stale after Evaluation Plane tests expanded from 7 to 13 cases.
4. Runtime reports and temporary evaluation state were separated from canonical package assets.
5. ZIP construction was constrained to exact manifest inventory.

## Honest limitations

This release provides deterministic package and harness certification, not live-model certification.

The build environment did not execute real Codex model sessions or native subagent threads. External live runs are still required to certify:

- model decision quality;
- actual token and latency budgets;
- native subagent event ordering;
- cancellation delivery;
- reconnect behavior across Codex clients;
- screenshot/image-based visual grading;
- behavior under real interactive approvals.

The live runner, JSONL normalizer, output schemas, GitHub Action workflow, skip/failure semantics, and live-suite contracts are included and statically tested.

## Release conclusion

Alpha 8 is accepted as the deterministic baseline for the Evaluation Plane. The next planned workstream is release-level live evaluation, cross-client evidence, and final system integration toward Beta/RC quality.
