# RUNTIME_DECISION_TREE.md — v1.5 Runtime Kernel

Use this as the lightweight execution algorithm after bootstrap. The goal is to preserve quality while avoiding unnecessary context, roles, and questions.

## Runtime loop

1. **Classify request**
   - Tiny, Fast Lane, Standard, Complex, High-risk, or Exception.
   - Existing repo? If yes and implementation/review may touch files, run `repo-recon` before specialist planning.
   - Review-only? Keep read-only until the user explicitly switches to implementation.

2. **Choose intake depth**
   - Micro Intake: 0–2 questions.
   - Fast Lane Intake: 1–3 questions.
   - Standard Intake: 3–7 questions.
   - Complex/High-risk Intake: 5–9 questions plus targeted follow-up.
   - Ask only decision-impact questions.

3. **Classify contributors**
   - Active specialist role: counts against role budget and owns an artifact.
   - System service: does not count if it only performs compact intake, chronicle, routing, or review service work.
   - Consulted role card: does not count if no output artifact is produced.

4. **Build selected-role contract**
   Every active specialist needs:
   - why selected;
   - artifact owned;
   - decision supported;
   - evidence required;
   - stop condition;
   - full playbook needed: yes/no.

5. **Load context progressively**
   Bootstrap docs → routing docs → role cards → selected full playbooks/skills → repo/code files.
   Large context is justified only when it can change the next decision or required artifact.

6. **Plan and gate**
   - Tiny/Fast Lane: inline plan or short plan.
   - Standard: planning brief.
   - Complex/High-risk: specialist findings + risk/consistency gates.
   - Do not change approved scope without user approval.

7. **Verify and review by level**
   Use `docs/REVIEW_LEVELS.md`.

8. **Chronicle compactly**
   Use `docs/CHRONICLE_POLICY.md`.

## Tiny/Fast implicit approval rule

If the user explicitly asks to implement, no risk gate is triggered, the change is reversible, and the task is Tiny/Fast Lane, the user request counts as implementation approval. Still summarize the intended change before or during implementation when ambiguity exists.

## Escalate tier when

- risk triggers appear;
- repo recon contradicts assumptions;
- user changes scope;
- new opportunity event affects acceptance criteria or architecture;
- verification cannot be performed;
- more than the role budget is required.

## De-escalate tier when

- the answer is already clear;
- risk gates are absent;
- role outputs cannot change the decision;
- a role card is enough;
- the task is review-only or copy-only.
