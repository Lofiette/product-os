# UI_REVIEW_PACKET.md

A UI Review Packet is the preferred input for UI review subagents. It keeps spawned reviewers bounded, fast, and evidence-based.

## When to use

Use this before asking Product Designer, Design Engineer, Design System Guardian, UX Writer, Accessibility Specialist, or QA Engineer to review an existing rendered UI.

## Required packet fields

```markdown
# UI Review Packet

## Target
URL / route:
Task goal:
Work mode:
Design-system mode:

## Evidence
Screenshot(s):
Viewport(s):
Changed files:
Relevant components:
Relevant DS docs/manifest:
Console errors:
Build/lint/test status:

## Expected review focus
Primary user goal:
Primary action:
States to check:
Design-system strictness:
Taste profile / good-bad examples:
Known constraints:

## Reviewer limits
Read-only: yes/no
Max findings:
Do not inspect beyond:
Stop condition:
```

## Reviewer output

Each reviewer must return a compact verdict and at most 5 findings. Findings must use:

```text
claim → evidence → impact → fix
```

## Current page review default

For a current rendered page, the main thread should build this packet first, then either:

- run a main-thread multi-lens review, or
- spawn at most two reviewer agents by default, or
- ask user approval for broader parallel review.
