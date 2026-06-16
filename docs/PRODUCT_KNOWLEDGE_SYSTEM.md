# Product Knowledge System

Product Knowledge is a compact routing and evidence layer for product work. It replaces long chat memory and bloated chronicles with navigable maps.

## Artifact hierarchy

```text
PRODUCT_MAP            -> where to start
KNOWLEDGE_INDEX        -> what evidence exists and how fresh/confident it is
areas/<area>.md        -> area-level routing and known boundaries
flows/<flow>.md        -> scenario-level behavior map
decisions/<ADR>.md     -> durable decisions and trade-offs
context/packets/*.md   -> task-specific bounded evidence packets
```

No artifact should absorb the job of the next layer.

- `PRODUCT_MAP` routes to areas.
- `AREA_MAP` routes to flows/components/hooks/API.
- `FLOW_MAP` describes scenario behavior.
- `CONTEXT_PACKET` assembles exactly what a task needs.

## Soft target sizes

Target sizes are recommendations, not truncation rules.

Never delete useful knowledge just to fit a line count. If a file grows, preserve correctness and propose splitting detail into child artifacts.

## Confidence model

Every product knowledge artifact should include:

- `freshness`: `current`, `needs-review`, or `stale`;
- `confidence`: `high`, `medium`, or `low`;
- `last_verified`;
- `scope`;
- `evidence`;
- `unknowns`;
- `review_trigger`.

## Knowledge sources

- Existing-product evidence from approved repo reads.
- Greenfield evidence from user brief and approved decisions.
- Redesign evidence from current-state, target-state, and approved deltas.
- Implementation evidence from changed files and verification.

## Operating principle

Baseline all core areas. Operationally prewarm only high-value/high-complexity areas. Deepen everything else task-driven.
