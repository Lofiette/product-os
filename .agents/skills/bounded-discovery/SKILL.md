---
name: bounded-discovery
description: Perform scoped read-only discovery to find relevant product/code context without broad repository scans.
---

# bounded-discovery

Use after a concrete task is given and before implementation.

## Inputs

- Active ticket.
- Product area map / knowledge index if available.
- Approved discovery boundaries.

## Allowed discovery pattern

1. Start with path-level discovery when the area is unknown.
2. Move to targeted content reads only after approval or when bounded discovery policy already allows it.
3. Prefer known entrypoints from Product Knowledge: area maps, `Where To Look Next`, review triggers.
4. Do not follow imports recursively by default.
5. Stop when evidence is sufficient to produce an Impact Map.

## Output artifact

Discovery Brief:

- exact commands/files read;
- found relevant areas/files;
- evidence;
- unknowns;
- confidence;
- next targeted reads if needed;
- Impact Map or approval request for Impact Map.

## Failure modes

- If discovery is too broad, stop and narrow scope.
- If evidence is insufficient, report unknowns instead of guessing.
- If an approved directory does not exist, report it absent and do not broaden automatically.
