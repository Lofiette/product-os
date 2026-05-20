# Prompt Recipes

## Start a new task

```text
Use Intake Mode. Read the project instructions and interview me using the adaptive question tree. Do not implement yet. Update TASK.md and CHRONICLE.md, recommend the optimal roles, and ask for approval before planning.
```

## After answering the brief

```text
Update TASK.md with my latest answers. Ask Chronicle Keeper to update CHRONICLE.md. Then use the selected specialist roles to create a planning brief. Do not implement yet.
```

## Approve implementation

```text
I approve the plan. Implement only the approved scope. Keep the diff minimal. Update tests/checks as planned. Update CHRONICLE.md before final summary.
```

## Review an existing diff

```text
Use implementation-review. Compare the diff against TASK.md and the approved plan. Use Code Reviewer and QA Engineer. If UI is affected, also use UX Interaction Reviewer and Design System Guardian. Do not rewrite code.
```

## Resume after context loss

```text
Read TASK.md and CHRONICLE.md. Summarize the current task, status, approved scope, risks, and next recommended action. Do not implement until I confirm.
```
