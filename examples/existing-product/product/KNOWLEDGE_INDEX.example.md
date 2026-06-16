# KNOWLEDGE_INDEX

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: index of runtime product knowledge artifacts and evidence collected through TKT-002 Phase 3A
evidence:
- Phase 2 path-only scan
- Phase 3A targeted app shell/top-navigation reads
unknowns:
- Area maps and flow maps do not exist yet.
- Detailed page behavior is not verified.
review_trigger: any new onboarding phase, product artifact update, or route/navigation/auth change

| Artifact / Evidence | Type | Scope | Freshness | Confidence | Last verified | Review trigger |
|---|---|---|---|---|---|---|
| `.codex-runtime/product/PRODUCT_MAP.md` | product map | MVP navigation map | current | medium | 2026-06-12 | top nav, route tree, auth, or product metadata changes |
| Phase 2 path-only scan | evidence | approved route/component/lib/style paths | current | medium | 2026-06-12 | route tree changes or new approved shape scan |
| `src/app/layout.tsx` | evidence | product metadata and root providers wrapper | current | high | 2026-06-12 | metadata/layout changes |
| `src/app/page.tsx` | evidence | root redirect to `/flows` | current | high | 2026-06-12 | root route changes |
| `src/components/layout/AppShell.tsx` | evidence | top navigation, profile, theme, workspace logo route | current | high | 2026-06-12 | navigation/shell changes |
| `src/components/layout/Header.tsx` | evidence | editor header actions and flow status labels | current | medium | 2026-06-12 | editor header changes |
| `src/components/auth/AuthGuard.tsx` | evidence | auth-required redirect behavior | current | high | 2026-06-12 | auth guard changes |
| Area maps | planned artifact | product area details | stale | low | 2026-06-12 | Phase 3B or later approval |
| Flow maps | planned artifact | user/system flows | stale | low | 2026-06-12 | Phase 3B or later approval |
| Decision records | planned artifact | durable product decisions | stale | low | 2026-06-12 | user decision or explicit evidence approval |
| Context packets | planned artifact | task-specific bounded context | stale | low | 2026-06-12 | future task approval |
