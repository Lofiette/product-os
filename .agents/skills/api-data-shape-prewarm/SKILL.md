---
name: api-data-shape-prewarm
description: Map frontend-facing API boundary and data shapes at contract level without performing backend deep dives.
---

# api-data-shape-prewarm

Use when API/data shapes affect UI/product work or during Product Knowledge onboarding.

## Levels

1. Shared boundary: API client, proxy, auth/token/error behavior.
2. Core frontend-facing types: entities, statuses, filters, timestamps, write-only fields, open-ended backend strings.
3. Area API behavior: endpoint paths, methods, mutations, caching, side effects. Use only when task-driven.
4. Backend semantics: validation, scoring, persistence, permissions. Use only when explicitly needed.

## Procedure

1. Start with path scan for `api`, `hooks`, `store`, `types` candidates.
2. Read shared client/proxy and core type files only after approval.
3. Extract UI implications, not backend documentation.
4. Update Product Knowledge only with frontend-facing constraints.
5. Leave endpoint/mutation details task-driven unless future tasks repeatedly need them.

## Output

API/Data Contract Brief:

- files read;
- shared API/client behavior;
- proxy/boundary behavior;
- core entities and fields affecting UI;
- error/loading/status implications;
- task-driven unknowns;
- recommended knowledge updates.
