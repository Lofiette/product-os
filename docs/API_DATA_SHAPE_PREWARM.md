# API/Data Shape Prewarm

API/Data Shape Prewarm captures frontend-facing contracts that affect UI and product decisions without doing a backend deep dive.

## Levels

1. Shared API boundary: client, proxy, auth, error shape.
2. Core data types: entities, statuses, filters, secret/write-only fields.
3. Area API behavior: endpoint paths, methods, mutations, caching.
4. Backend semantics: validation, scoring, permissions, side effects.

Prewarm usually covers levels 1–2. Levels 3–4 are task-driven.

## Output

- API/data implications in `PRODUCT_MAP` or area maps.
- Evidence rows in `KNOWLEDGE_INDEX`.
- Unknowns for endpoint/mutation/backend semantics.
