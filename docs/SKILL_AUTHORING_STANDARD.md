# Skill Authoring Standard

This standard defines an active CPT skill as an operational method, not a title or a five-step placeholder.

## One skill, one decision-shaped job

A skill should own one repeatable method and one recognizable output contract. Split a skill when two parts:

- have different triggering language;
- require different evidence;
- produce independently useful artifacts;
- have different stop conditions or risk;
- are commonly used separately.

Consolidate skills when they are aliases, sequential fragments of one method, or cannot make a useful decision independently.

## Required structure

Every active `SKILL.md` must include:

1. YAML frontmatter with exact folder-matching `name` and a discriminative `description`.
2. `Use when` with positive conditions.
3. `Do not use when` with nearby but incorrect cases.
4. `Required inputs` including runtime, product, code, evidence, and approval prerequisites.
5. A domain-specific `Method` expressed as imperative steps.
6. A named `Output contract` whose fields can be checked.
7. `Evidence standard` defining what supports or cannot support a claim.
8. `Stop and escalate` conditions.
9. `Failure modes to avoid`.
10. `agents/openai.yaml` with interface metadata and invocation policy.
11. At least two positive and one negative trigger cases in the central evaluation registry.

## Description rules

The frontmatter description is part of the initial Codex skill-discovery surface. It should:

- lead with `Use to ...` or another trigger-forward phrase;
- name the decision or artifact;
- distinguish the closest competing skill;
- mention a critical non-trigger when confusion is likely;
- avoid generic claims such as “help with quality”;
- remain concise enough for the active-pack metadata budget.

## Method depth

A method must encode professional judgment, not universal workflow boilerplate. It should name the domain-specific sequence, trade-offs, evidence checks, and stopping logic an expert would use. “Read files, analyze, report” is never sufficient.

## Output contract

The output contract should support downstream work. Prefer explicit sections or typed fields such as:

- decision and scope;
- evidence and confidence;
- alternatives and rationale;
- findings with severity/impact/fix;
- acceptance or release verdict;
- unresolved unknowns and next owner.

Do not require long prose when a matrix, state model, risk register, or contract is more precise.

## Evidence and confidence

Skills must separate:

- user-approved decisions;
- observed runtime/code/product evidence;
- inferred relationships;
- hypotheses;
- missing evidence.

A passing build, scanner, or single metric cannot prove a broader product or quality claim unless the skill explicitly defines that boundary.

## Invocation policy

Use implicit invocation only when the workflow is focused, common, low-surprise, and has distinctive trigger language. Use explicit-only invocation for workflows that are expensive, broad, easily over-triggered, or require deliberate user intent, including real delegation, framework audits, and broad ideation.

## Scripts and references

Instruction-only is preferred for judgment-heavy work. Add scripts when deterministic behavior improves evidence or enforcement. A script must document false positives, false negatives, and what it does not prove. Put long method references, standards, examples, or domain tables in `references/` so initial instructions remain focused.

## Author review checklist

Before release, verify:

- the skill is not an alias of another active skill;
- its nearest competitor has a clear boundary;
- its output contract is independently useful;
- method steps are domain-specific;
- stop conditions protect scope and evidence quality;
- metadata remains within the intended activation profile;
- positive and negative trigger cases pass;
- no product-, organization-, or design-system-specific name is baked into universal core instructions.
