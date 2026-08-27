# Product OS Executable Evaluation Plane

This directory contains executable, repository-isolated evaluations for the Runtime, Knowledge, Expertise, Enforcement, and Worker Orchestration planes.

## Evidence levels

- **Reference backend**: deterministic package-authored actions. Proves harness, policies, runtime contracts, fixtures, and graders. It does not certify model quality.
- **Live backend**: optional `codex exec --json` runner using the same fixtures, output schema, and graders.
- **External backend**: prepare a fixture for a trusted host or the official Codex GitHub Action, then grade its structured output and normalized JSONL trace.

## Suites

- `offline-core`: 21 required self-contained cases.
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

For a local ChatGPT-authenticated Codex CLI, point the harness at the existing
credential file without copying it into the retained report directory:

```powershell
$env:CPT_EVAL_CODEX_AUTH_FILE = Join-Path $env:USERPROFILE ".codex\auth.json"
python tools/cpt_eval.py run --suite live-smoke --backend live --report-dir .cpt-eval-live/smoke
Remove-Item Env:CPT_EVAL_CODEX_AUTH_FILE
```

The harness copies that file into a short-lived operating-system temp directory
and removes the copy after each case. It never writes credential contents to a
trace or scorecard. It activates `cpt-core` plus each case-declared domain plugin
through the isolated local marketplace before execution. Each non-interactive case
uses only that temporary profile and the CLI's non-interactive
`--approve-for-me` mode, which uses a workspace-write
sandbox so commands cannot pause for an unavailable human approval. Read-only
case contracts are still enforced by trace and Git-diff grading, but these runs
do not certify a native read-only sandbox boundary.
It also removes inherited `CODEX_*` desktop-session variables before launching
the independent CLI process. Set
`CPT_EVAL_KEEP_RAW_TRACE=1` only for local diagnostics; raw event streams can
contain source excerpts and must not be published without review. Do not commit
or upload a live Codex home.

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
