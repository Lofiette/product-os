# REPO_RECON.md — Existing Repository Reconnaissance

Run Repo Recon before implementation or review in an existing repository when the task may touch files, architecture, scripts, dependencies, tests, or conventions.

## Purpose

Understand the repository just enough to avoid wrong assumptions. Repo Recon is not a full codebase audit.

## Repo Recon protocol

1. Shallow file-tree scan.
2. Detect package manager, language, framework, and platform.
3. Read package/build/test/lint/typecheck scripts.
4. Locate project instructions: `AGENTS.md`, README, contributing docs, local docs.
5. Identify generated files, build output, vendored files, lockfiles, and forbidden zones.
6. Locate relevant source areas, tests, components, API contracts, or config.
7. Find existing patterns before proposing new ones.
8. Return a compact Repo Recon Brief.
9. Load large files only when they are directly relevant to the selected plan.

## Repo Recon Brief schema

```text
Repository type:
Detected stack:
Package manager:
Key scripts:
Relevant directories:
Existing patterns to reuse:
Tests/checks available:
Generated/forbidden zones:
Risks/unknowns:
Recommended next files to inspect:
```

## Stop conditions

Stop and ask when:
- the repo structure conflicts with the user’s stated stack;
- no safe verification command is obvious;
- the requested change touches forbidden/generated files;
- environment secrets or private credentials appear required;
- risk gates are triggered.
