# EVIDENCE_POLICY.md — Evidence, assumptions, and claims

This kit must distinguish what is known, what is inferred, and what is merely hypothesized.

## Evidence levels

1. **Repository evidence**: code, tests, docs, configs, logs, diffs, data files in the current project.
2. **User-provided evidence**: explicit user statements, uploaded materials, pasted requirements, screenshots, interview notes.
3. **External evidence**: web, official docs, research papers, public market data, verified sources.
4. **Derived inference**: conclusion logically drawn from evidence; must say it is an inference.
5. **Assumption**: useful working belief not yet validated.
6. **Hypothesis**: testable proposition proposed for research, experiment, or implementation validation.

## Hard rules

- Do not invent market facts, competitor claims, pricing, user behavior, legal status, metrics, incidents, benchmarks, or production constraints.
- Do not call assumptions “findings”.
- Do not call stakeholder opinions “user insights”.
- Do not call AI/model behavior “safe” or “accurate” without eval evidence and scope.
- Do not claim legal or compliance certainty; identify risks and recommend qualified review when needed.
- When evidence is missing, state what evidence is needed and the smallest way to get it.

## Required labels for research roles

Market Researcher, UX Researcher, CX Researcher, Analytics Engineer, Customer Support Analyst, Experimentation Specialist, and Domain Expert must label outputs as:

- Evidence-backed finding
- Inference
- Assumption
- Hypothesis
- Open question

## Examples

Bad: “Users want bulk editing.”
Good: “Hypothesis: bulk editing may reduce repetitive work for power users. Evidence needed: interviews or usage logs showing repeated single-item edits.”

Bad: “This market is growing quickly.”
Good: “Open question: market growth requires external evidence. Current task only provides an internal assumption that demand exists.”
