---
name: manifest-freeze-check
description: Freeze or classify DS manifest authority before implementation and detect manifest changes that could self-validate UI work.
---

# manifest-freeze-check

## Trigger

Use when `DESIGN_SYSTEM_MANIFEST.json`, component registry, token manifest, or DS docs are created/changed/used for compliance.

## Process

1. Read `docs/MANIFEST_FREEZE_POLICY.md`.
2. Identify baseline manifest path.
3. Determine if the manifest existed before implementation.
4. Detect whether it changed during the task using git diff if available.
5. If changed, require explicit approval before using the new manifest as authority.
6. Report what compliance can and cannot be proven.

## Suggested script

Run `node scripts/check-design-source-authority.mjs` if available.

## Output

Include manifest path, baseline status, changed status, authority state, and verdict.
