# CONTENT_REALISM.md

Prototype content must be realistic enough to validate comprehension, layout, and hierarchy.

## Rule

Do not validate UI quality on placeholder data that hides product problems.

Bad validation content:
- `Категория 1`, `Категория 2` without domain meaning;
- raw technical IDs exposed to non-technical users;
- duplicated names that obscure hierarchy;
- lorem ipsum or generic filler;
- internal pipeline/node labels unless the product is explicitly developer-facing.

Good validation content:
- realistic names;
- plausible statuses;
- domain-specific labels;
- representative empty/error/edge cases;
- content that tests long labels, overflow, and scanning behavior.

## Blocking conditions

`BLOCKED` if content makes it impossible to judge:
- primary action clarity;
- card/list hierarchy;
- user comprehension;
- target audience fit;
- copy tone;
- density.

## Required output

Use `.agents/templates/content-realism-report.md`.
