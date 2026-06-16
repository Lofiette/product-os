# PRODUCT_MAP

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: MVP navigation map from Phase 2 path discovery and Phase 3A app shell/top-nav reads
evidence:
- Phase 2 path-only scan: `rg --files src`, `rg --files app`, `rg --files components`, `rg --files lib`, `rg --files styles`
- Phase 3A targeted reads: `src/app/layout.tsx`, `src/app/page.tsx`, `src/components/layout/AppShell.tsx`, `src/components/layout/Header.tsx`, `src/components/auth/AuthGuard.tsx`
unknowns:
- Page responsibilities are not confirmed beyond app shell/top navigation.
- Area behavior, empty/error states, and detailed flows need Phase 3B reads.
- Permissions beyond authenticated/unauthenticated are unknown.
review_trigger: changes to app shell, top navigation, auth guard, route tree, or product metadata

## Product

- Name: `Платформа ОКО`
- Description: visual editor for graph-based agent scenarios
- Default route: `/` redirects to `/flows`
- Primary actor: authenticated workspace user, likely a workflow builder/operator
- Auth model: auth may be required; unauthenticated users are redirected to `/login` when required

## Top Navigation

| Surface | Label | Confidence | Where to look next |
|---|---|---|---|
| `/flows` | Рабочие процессы | high | Phase 3B: `src/app/flows/page.tsx` |
| `/flow-runs` | Запуски | high | Phase 3B: `src/app/flow-runs/page.tsx` |
| `/libraries` | Библиотеки | high | Phase 3B: `src/app/libraries/page.tsx` |
| `/models` | Модели | high | Phase 3B: `src/app/models/page.tsx` |
| `/login` | Login/auth | medium | Phase 3B: `src/app/login/page.tsx` |

## Candidate Product Areas

| Area | Current evidence | Confidence | Future artifact |
|---|---|---|---|
| Workflows | Product description, `/flows` nav, flow route paths | medium | area map later |
| Flow editor | Editor/header affordances and editor path names | medium | area map later |
| Flow runs | `/flow-runs` nav and route path | medium | area map later |
| Libraries | `/libraries` nav and library/document/chunk paths | medium | area map later |
| Models | `/models` nav and model route paths | medium | area map later |
| Auth/session | `AuthGuard`, profile/logout in app shell | medium | area map later if needed |
| Workspace shell | App shell, top nav, theme/profile controls | high | context packet if UI shell work starts |

## Top Flows To Map Later

| Flow | Evidence | Confidence | Next read |
|---|---|---|---|
| Open workspace at `/` and land in workflows | root redirect to `/flows` | high | `src/app/flows/page.tsx` |
| Navigate between top areas | app shell nav items | high | area page files |
| Authenticate before workspace access | `AuthGuard` redirects to `/login` when required | high | `src/app/login/page.tsx` |
| Edit/validate/save/run a workflow | shared editor header actions | medium | flow editor page/components |
| Review workflow runs | `/flow-runs` nav/path | medium | `src/app/flow-runs/page.tsx` |
| Manage libraries/documents | library/document paths | low | library page files |
| Manage models | model paths | low | model page files |

## Routing Guidance For Future Tasks

- Workflow list/editor task: start with `/flows` pages, then bounded flow editor reads.
- Execution/run-history task: start with `/flow-runs`, then bounded execution UI/API reads if approved.
- Library/document/retrieval task: start with `/libraries` pages, then bounded library component reads.
- Model configuration task: start with `/models` pages.
- Auth/session task: start with `AuthGuard`, login page, and auth hook only after approval.
- Shell/navigation/theme task: start with `AppShell`, `Header`, and workspace chrome hook only after approval.

## Not Yet Mapped

- Detailed area ownership
- Detailed user journeys
- Data model and API behavior
- Permission model
- Flow editor state model
- Library/document/chunk semantics
- Model provider/configuration semantics
