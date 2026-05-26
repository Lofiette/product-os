---
name: repo-recon
description: Map an existing repository before planning or implementation: stack, package manager, scripts, instructions, patterns, tests, generated files, and forbidden zones.
---


# repo-recon

## Purpose

Build a shallow but reliable map of an existing repository before changing it.

## Required inputs

- Current task from `TASK.md`.
- File tree, package/build config, existing instructions.
- User constraints.

## Procedure

1. Scan the top-level tree and important app/package directories.
2. Detect package manager and monorepo/tooling: npm/yarn/pnpm/bun, turbo/nx, Vite/Next/React/Vue/Angular/Svelte, backend frameworks.
3. Read scripts from package/config files: build, lint, test, typecheck, storybook, e2e.
4. Find project instructions: AGENTS.md, README, CONTRIBUTING, docs, local package instructions.
5. Identify generated/forbidden zones: generated code, dist/build, migrations, snapshots, vendor.
6. Locate relevant implementation patterns and tests for the requested area.
7. Do not load large source files until the relevant slice is known.

## Output schema

```markdown
## Repo Recon Brief

### Stack and tooling
### Package manager and scripts
### Project instructions found
### Relevant directories/files
### Existing patterns to reuse
### Tests/checks available
### Generated/forbidden zones
### Unknowns/blockers
### Recommended next roles/skills
```

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

