# PROMPT_RECIPES.md

## Start a new task
Use `FIRST_PROMPT.md`.

## After answering intake
Update `TASK.md` and `CHRONICLE.md`, select the smallest sufficient team, load only selected playbooks, create a planning brief, run Consistency Auditor, then ask for approval.

## Approve implementation
I approve the plan. Implement only the approved scope. Respect all risk gates. Update tests and CHRONICLE.md before final summary.

## Resume after context loss
Read `TASK.md` and `CHRONICLE.md`. Summarize current phase, approved scope, risks, files touched, verification status, and next recommended action. Do not implement until I confirm.

## Run self-audit
Run `python scripts/validate_kit.py` and summarize any structural or content warnings.


## Opportunity event

```text
A new idea/signal appeared: [describe]. Treat this as an opportunity event. Classify source, evidence level, affected decision, and impact. If it can improve the current plan, run one appropriate creative method and produce a Creative Enhancement Brief. Do not change approved scope without my approval.
```
