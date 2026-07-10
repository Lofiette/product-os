# Task-Driven Knowledge Updates

Every Standard Task must account for durable knowledge before completion:

- `not_required`: the task changes no durable product knowledge;
- `planned`: affected artifacts are identified but not yet updated;
- `applied`: required updates are complete and validated;
- `deferred`: an explicit bounded follow-up remains, with rationale.

The runtime refuses to complete a new Alpha 5 task while knowledge update status is `not_assessed` or `planned`.

Update only affected artifacts. A local change must not trigger a broad remap. Context packets remain task-specific and should not become canonical product maps.
