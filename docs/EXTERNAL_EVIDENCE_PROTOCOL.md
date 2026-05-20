# EXTERNAL_EVIDENCE_PROTOCOL.md

Use this when a role needs facts not present in the repository, uploaded files, or user-provided context.

## Rule

Do not invent external facts. If external research is unavailable in the environment, produce a research plan instead of conclusions.

## Required behavior

1. State what claim requires external evidence.
2. Identify likely source types: official docs, standards, competitor sites, app stores, analyst reports, academic papers, pricing pages, changelogs, regulations, support/community data.
3. Provide search queries or source list.
4. Mark any current statement as assumption or hypothesis.
5. Ask the user for permission or data if needed.

## Output schema

```markdown
## External evidence needed

### Claim or decision requiring evidence

### Why current context is insufficient

### Recommended sources

### Search queries

### Safe interim assumption

### Risk if we proceed without evidence
```
