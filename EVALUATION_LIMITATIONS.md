# Product OS 4.1 evaluation limitations

Product OS 4.1 inherits the Product OS 4.0 executable baseline and validates the Evaluation Plane, not every model and client combination.

## No live-model certification in the build environment

The release can be built without a Codex CLI session or API credential. In that environment:

- the deterministic reference backend is required;
- live suites remain optional;
- a missing Codex CLI produces `SKIPPED`;
- live quality, latency, and token budgets remain unverified until a user runs them.

## Synthetic traces are not native transcripts

Reference traces are package-authored and intentionally bounded. They prove grader behavior, fixture integrity, runtime contracts, and regression logic. They do not prove native event ordering or model honesty.

## Live event normalization is best effort

Codex JSONL event shapes can evolve. The current normalizer supports supported command, file-change, message, error, and usage events. Unknown events are retained as generic records but may require future normalizer updates.

## Approval observability varies by host

Interactive clients, non-interactive CLI runs, and hosted CI can expose different approval evidence. The harness does not invent approval events that the host did not provide.

## Visual quality is not screenshot-certified yet

Reference-fidelity and accessibility cases grade structured evidence, bounded behavior, and filesystem/runtime outcomes. Pixel-level screenshot comparison and image-based graders remain future work.

## A deterministic score is a package baseline

A score of 100 from the reference backend means package-authored reference behavior satisfies the case contract. It is not a promise that every model will receive the same score.

## Optional live CI requires a trusted secret

The manual live-smoke workflow requires an API credential and must follow the user organization's secret, runner, and repository-trust policies. It uses read-only sandboxing and minimal repository permissions, but those choices do not replace organizational review.

## Design Intelligence is not part of the legacy executable baseline

The `evaluation/design-intelligence/` adjunct defines a 16-dimension Product Designer rubric and initial cases. It is structurally validated, but it does not yet provide live-model certification, rendered fixture baselines, screenshot grading, or calibrated human-judge reliability. Its scores must not be represented as live-model or screenshot certification.

## Product Designer 4.1 execution adapters are contracts, not live certifications

The capability model and generic/OpenAI Product Design adapter manifests validate portability, ownership, provenance, fallback, and approval rules. They do not prove that a plugin is installed, enabled, trusted, stable, or behaves as described in a particular Codex client. Only skills visibly exposed by the active runtime may be used, and provider-produced QA is not independent acceptance.

## Book-derived pattern catalogs are transformed judgment aids

The Tidwell and Silver catalogs are operational summaries with filtering boundaries. Their historical screenshots, code, browser behavior, ARIA recipes, conversion figures, and platform examples are not certified as current standards. Current implementation claims still require current project or official sources.
