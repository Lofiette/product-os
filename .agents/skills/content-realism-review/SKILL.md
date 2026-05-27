---
name: content-realism-review
description: Check whether prototype/demo/user-facing content is realistic enough to validate layout, comprehension, hierarchy, and product taste.
---

# content-realism-review

## Trigger

Use for UI prototypes, dashboards, cards/lists/tables, content-heavy screens, or when sample data is generated.

## Process

1. Read `docs/CONTENT_REALISM.md`.
2. Identify placeholder/generic/internal content.
3. Check whether labels match target audience and product domain.
4. Flag technical IDs, filler categories, lorem ipsum, unrealistic duplication, and misleading demo data.
5. Return PASS / PASS WITH WARNINGS / BLOCKED.

## Output

Use `.agents/templates/content-realism-report.md`.
