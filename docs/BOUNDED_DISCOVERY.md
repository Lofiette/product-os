# Bounded Discovery

Bounded discovery lets Codex find relevant context without making the user list every file and without reading the whole repository.

## Default allowed discovery after a concrete task

- Targeted search in approved source directories.
- Small relevant file reads.
- Path-only scan before content reads when area is unknown.
- `git diff --stat` before full diffs.
- Impact Map reporting.

## Requires approval

- Broad repository scans.
- Reading root historical memory.
- Reading external/design-system/reference modules broadly.
- Build/test/lint.
- Real subagents.
- Any implementation edit.

## Output

Bounded discovery must produce:

- exact commands/files read;
- evidence;
- unknowns;
- Impact Map or discovery brief;
- next recommended reads;
- approval request before implementation.
