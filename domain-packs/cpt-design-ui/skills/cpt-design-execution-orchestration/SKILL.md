---
name: cpt-design-execution-orchestration
description: Use to build design artifacts through discovered provider-neutral tools with explicit fallbacks and independent QA.
---

# CPT Design Execution Orchestration

## Use when

- A design decision must become an inspectable artifact: audit, screenshots, visual directions, interactive prototype, coded frontend, source comparison, design-tool handoff, or hosted preview.
- The agent may have different tools, plugins, MCP servers, browser, image generation, code, or publishing capabilities and the workflow must remain portable.
- An optional vendor plugin, including OpenAI Product Design in Codex, may accelerate execution without owning the product decision.

## Do not use when

- Only product reasoning or a text specification is requested and no execution artifact is needed.
- The user explicitly requests a particular tool and its safe invocation path is already fully defined.
- External publication, destructive changes, or account actions lack required approval.

## Required inputs

- Approved or provisional Design Decision / Pattern Decision and intended learning question.
- Target artifact, fidelity, representative states, platforms, and acceptance criteria.
- Available tool/skill/plugin inventory or permission to inspect it.
- Source URLs/screenshots/design files/repository paths and authority classification.
- Design-system, accessibility, content, data, technical, security, and publishing constraints.
- Approval boundary for writes, external services, publishing, and irreversible actions.

## References

1. Read `references/DESIGN_EXECUTION_CAPABILITY_MODEL.md`.
2. Validate adapter manifests against `references/DESIGN_EXECUTION_ADAPTER_SCHEMA.json` conceptually or with the supplied validator.
3. Use only adapters that are actually discovered:
   - `references/adapters/generic-agent-tools.yaml`;
   - `references/adapters/openai-product-design.yaml` when the OpenAI Product Design plugin is visibly available.
4. Use `references/DESIGN_EXECUTION_BRIEF.md` and `references/EXECUTION_EVIDENCE_PACKET.md`.

## Method

1. Inventory observed capabilities. Record exact tool/skill/plugin names, inputs, outputs, read/write behavior, approval needs, and confidence. Never infer a capability from vendor reputation or a hidden skill count.
2. Translate the requested result into capability requirements such as live-source inspection, screenshot capture, visual generation, interaction prototyping, frontend implementation, source-diff QA, design export, annotation, or preview publishing.
3. Select the smallest adapter composition that satisfies the requirements. Rank by source fidelity, reversibility, evidence quality, design-system access, accessibility support, portability, cost, latency, and permission risk.
4. Keep Product Designer ownership separate from execution. Freeze the problem frame, pattern composition, visual contract, states, and acceptance criteria before delegating an expensive build unless the build itself is the learning experiment.
5. Create a staged execution plan with checkpoints and fallback paths. Each stage must state inputs, tool, expected artifact, evidence, failure handling, and approval boundary.
6. Execute or delegate in bounded stages. Preserve original sources, generated artifacts, prompts/briefs, assumptions, and tool provenance. Do not silently replace missing capabilities with a lower-fidelity claim.
7. Review outputs through the existing Product Designer, Design Quality Gate, Accessibility Gate, design-system checks, and Visual Acceptance Review. A tool's own QA is supporting evidence, not final acceptance.
8. Iterate from explicit findings. Send targeted deltas rather than restarting the whole design unless the interaction model is wrong.
9. Publish/export only after approval. Record location, visibility, expiry, ownership, and rollback/removal path.
10. Return an Execution Evidence Packet and update the design decision with observed limitations and residual risk.

## Output contract

Produce:

- `Capability Inventory` with observed/unavailable/uncertain capabilities.
- `Adapter Selection` with rationale, vendor-independent fallback, and approval boundary.
- `Design Execution Brief` with artifact, fidelity, sources, states, constraints, and acceptance criteria.
- `Staged Execution Plan` with checkpoints, failure handling, and stop conditions.
- `Execution Evidence Packet` with artifacts, provenance, comparisons, test evidence, limitations, and final verdict.

## Evidence standard

- An adapter manifest describes a possible mapping; only observed runtime availability proves it can be used.
- A generated screenshot, prototype, or code bundle does not prove task fit, accessibility, or design-system fidelity.
- Tool-produced QA cannot be the sole judge of the same tool's output.
- Missing source access must be reported as missing evidence, not filled by imagined inspection.

## Stop and escalate

- Required capability or source is unavailable and fallback would change the promised artifact or fidelity.
- External write, publication, paid service, credential use, or irreversible action lacks approval.
- Design ownership, acceptance criteria, or authoritative source is unresolved.
- The adapter requests broader permissions than the task requires.

## Failure modes to avoid

- Hard-coding the workflow to Codex or one vendor.
- Assuming an installed plugin is enabled, trusted, or capable of every advertised workflow.
- Letting the execution tool redefine the product problem or acceptance criteria silently.
- Publishing prototypes without visibility, ownership, expiry, or rollback records.
- Calling image-to-code a faithful implementation without source-diff and interaction QA.
- Hiding capability gaps behind polished output.
