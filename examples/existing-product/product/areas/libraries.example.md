# Libraries Area Map

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: first compact map for Libraries from approved Phase 2, Phase 3A, and Phase 3B route evidence
evidence:
- Phase 2 path-only scan
- Phase 3A app shell/auth reads
- Phase 3B batch: `src/app/libraries/page.tsx`, `src/app/libraries/[name]/page.tsx`, `src/app/libraries/[name]/documents/[docId]/page.tsx`
unknowns:
- Library and document component internals are not read.
- Creation/edit/delete/upload/chunk/retrieval behavior needs verification.
review_trigger: changes to library routes, library/document components, or retrieval/document behavior

## Area Summary

Libraries appears to cover library listing, library detail by name, and document detail within a library.

Claim status: confirmed for route surfaces; deeper library semantics need verification. Confidence: medium.

## Confirmed Surfaces

| Surface | Purpose | Claim status | Confidence |
|---|---|---|---|
| `/libraries` | Library list surface rendering `LibraryList` | confirmed | high |
| `/libraries/[name]` | Library detail surface using decoded library name | confirmed | high |
| `/libraries/[name]/documents/[docId]` | Document detail surface using decoded library name and document ID | confirmed | high |

## Actors And Access

| Claim | Claim status | Confidence |
|---|---|---|
| Libraries is inside authenticated workspace chrome when auth is required. | confirmed | high |
| Primary actor likely manages knowledge/document libraries. | inferred | medium |

## Candidate Flows For Future Flow Maps

| Future flow map | Current status | Next evidence needed |
|---|---|---|
| `libraries/view-list` | placeholder | `src/components/libraries/LibraryList.tsx` |
| `libraries/open-library` | placeholder | `LibraryDetailPage` |
| `libraries/open-document` | placeholder | `DocumentDetailPage` |
| `libraries/manage-documents` | placeholder | library/document components |
| `libraries/retrieval-test` | placeholder | retrieval UI evidence |

## Where To Look Next

- To understand library list actions: `src/components/libraries/LibraryList.tsx`
- To understand library detail behavior: `src/components/libraries/LibraryDetailPage.tsx`
- To understand document/chunk behavior: `src/components/libraries/DocumentDetailPage.tsx`
