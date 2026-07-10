# Evidence and Provenance

Evidence types are explicit:

- user-approved decision
- design artifact
- source file
- route
- component
- hook/store
- API/type contract
- test
- runtime observation
- external source
- other bounded evidence

Every evidence item stores source, optional locator, summary, source revision, and observation time.

Canonical product behavior should prefer repository evidence, approved decisions, tests, and runtime observations. Semantic retrieval may suggest sources but never replaces the original evidence.

`source_revision` identifies what version was inspected. A material claim with no meaningful source revision cannot be treated as fully validated.
