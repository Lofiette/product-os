---
name: repo-recon
description: Use before planning, implementation, or review in an existing repository when the task may touch files, architecture, scripts, dependencies, tests, or conventions.
---

# Repo Recon Skill

Do not inspect the whole repository deeply. Build just enough situational awareness to avoid wrong assumptions.

## Process

1. Shallow file-tree scan.
2. Detect package manager, language, framework, platform, and monorepo layout.
3. Read scripts for build, test, lint, typecheck, format, storybook, e2e, or dev server.
4. Locate project instructions: `AGENTS.md`, README, docs, contributing files, local conventions.
5. Identify generated/vendor/build files and forbidden zones.
6. Locate likely relevant source areas and tests.
7. Find existing patterns before proposing new components, APIs, utilities, or tests.
8. Return a compact Repo Recon Brief.
9. Stop before loading large files unless directly relevant to the selected plan.

## Output schema

```text
Repo Recon Brief
- Repository type:
- Detected stack:
- Package manager:
- Key scripts:
- Relevant directories:
- Existing patterns to reuse:
- Tests/checks available:
- Generated/forbidden zones:
- Risks/unknowns:
- Recommended next files to inspect:
- Tier impact:
```

## Stop conditions

Stop and ask if:
- repo stack contradicts user assumptions;
- no safe verification path is visible;
- requested change touches generated/forbidden files;
- secrets or private credentials appear required;
- risk gates trigger.
