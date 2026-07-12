# Beta 1 Limitations

Beta 1 validates the Evaluation Plane, not every model and client combination.

## No live-model certification in the build environment

The release can be built without a Codex CLI session or API credential. In that environment:

- the deterministic reference backend is required;
- live suites remain optional;
- a missing Codex CLI produces `SKIPPED`;
- live quality, latency, and token budgets remain unverified until a user runs them.

## Synthetic traces are not native transcripts

Reference traces are package-authored and intentionally bounded. They prove grader behavior, fixture integrity, runtime contracts, and regression logic. They do not prove native event ordering or model honesty.

## Live event normalization is best effort

Codex JSONL event shapes can evolve. Beta 1 normalizes supported command, file-change, message, error, and usage events. Unknown events are retained as generic records but may require future normalizer updates.

## Approval observability varies by host

Interactive clients, non-interactive CLI runs, and hosted CI can expose different approval evidence. The harness does not invent approval events that the host did not provide.

## Visual quality is not screenshot-certified yet

Reference-fidelity and accessibility cases grade structured evidence, bounded behavior, and filesystem/runtime outcomes. Pixel-level screenshot comparison and image-based graders remain future work.

## A deterministic score is a package baseline

A score of 100 from the reference backend means package-authored reference behavior satisfies the case contract. It is not a promise that every model will receive the same score.

## Optional live CI requires a trusted secret

The manual live-smoke workflow requires an API credential and must follow the user organization's secret, runner, and repository-trust policies. It uses read-only sandboxing and minimal repository permissions, but those choices do not replace organizational review.
