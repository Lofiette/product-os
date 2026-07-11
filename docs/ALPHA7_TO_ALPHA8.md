# Alpha 7 to Alpha 9

Alpha 7 introduced managed worker orchestration. Alpha 9 adds an executable Evaluation Plane that can prove package contracts and detect regressions.

## Preserved from Alpha 7

- Runtime Kernel and scoped authorization leases;
- Product Knowledge schema and lifecycle;
- 45 canonical skills;
- 50 logical roles and 25 quality gates;
- deterministic enforcement;
- ten worker archetypes;
- quorum, timeout, cancellation records, checkpoint recovery, and worktree isolation.

## Added in Alpha 9

- 20 executable evaluation cases;
- six fixture repositories;
- four suites;
- deterministic reference backend;
- optional `codex exec --json` backend;
- external fixture preparation and grading;
- structured output schemas;
- trace, filesystem, runtime, and budget graders;
- reviewed offline baseline;
- four mutation tests;
- cross-platform offline CI;
- optional manual live-smoke CI.

## Evidence boundary

Reference execution proves the harness and package-authored contracts. Live model certification remains separate and optional. A green deterministic score must never be presented as proof that all models, clients, or repositories behave identically.
