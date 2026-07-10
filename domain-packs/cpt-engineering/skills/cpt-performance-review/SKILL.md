---
name: cpt-performance-review
description: Use to assess and measure performance risks across UI, API, data, and infrastructure; not to optimize without a baseline.
---

# CPT Performance Review

## Use when

- A task can affect latency, throughput, rendering, memory, bundle, query, or scale.

## Do not use when

- No performance-sensitive path changes and no reported performance problem exists.

## Required inputs

- User/system performance goal, workloads, baseline, budgets/SLOs, architecture, changed path, measurement tools, and environment.

## Method

1. Define user-visible and system metrics, percentiles, workload, and budget.
2. Establish baseline and reproduce under representative conditions.
3. Map critical path, waits, renders, queries, network, serialization, allocation, and contention.
4. Form hypotheses and instrument before optimizing.
5. Evaluate trade-offs, regressions, caching, batching, concurrency, and degradation behavior.
6. Measure before/after with variance and environment caveats.
7. Define monitoring and regression thresholds.

## Output contract

Produce a compact artifact containing:

- `Performance budget and baseline.`
- `Critical-path findings and evidence.`
- `Optimization options/trade-offs.`
- `Measurement results, monitoring, and verdict.`

## Evidence standard

- Synthetic microbenchmarks do not automatically predict user latency.

## Stop and escalate

- No reproducible baseline.
- Optimization would harm correctness or maintainability without justified gain.

## Failure modes to avoid

- Optimizing averages only.
- Caching without invalidation strategy.
