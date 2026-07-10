# Freshness and Dependency Model

Artifacts declare review triggers using path globs and events. They may depend on other knowledge artifacts.

A freshness scan:

1. receives changed paths/events or a bounded Git diff;
2. marks directly matched artifacts and claims `needs_review`;
3. propagates review need to dependent artifacts;
4. never rewrites unrelated knowledge;
5. preserves unknowns and provenance;
6. regenerates human-readable projections.

Freshness is not age alone. An old artifact may remain current if its evidence and review triggers did not change. A new artifact may already need review if its source revision is unknown or contradicted.
