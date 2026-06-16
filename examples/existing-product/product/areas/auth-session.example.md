# Auth And Session Area Map

freshness: current
confidence: medium
last_verified: 2026-06-12
scope: first compact map for Auth/session from approved Phase 3A and Phase 3B route evidence
evidence:
- Phase 3A: `src/components/auth/AuthGuard.tsx`, `src/components/layout/AppShell.tsx`
- Phase 3B batch: `src/app/login/page.tsx`
unknowns:
- `LoginForm` and auth hook internals are not read.
- Credential fields, auth failure states, session persistence, and auth-required source need verification.
review_trigger: changes to login route, auth guard, auth hook, provider setup, or profile/logout behavior

## Area Summary

Auth/session appears to gate product areas behind `AuthGuard` when auth is required, provide `/login`, and expose profile/logout controls in the app shell.

Claim status: confirmed for route wrapping and redirect behavior; detailed auth mechanics need verification. Confidence: medium.

## Confirmed Surfaces

| Surface | Purpose | Claim status | Confidence |
|---|---|---|---|
| `/login` | Login surface rendering `LoginForm` | confirmed | high |
| Product area routes | Wrapped by `AuthGuard` in approved reads | confirmed | high |
| App shell profile menu | Profile/logout controls when authenticated and auth is required | confirmed | high |

## Actors And Access

| Claim | Claim status | Confidence |
|---|---|---|
| Unauthenticated users are redirected to `/login` when auth is required. | confirmed | high |
| Auth can be optional/configurable via `authRequired`. | confirmed | high |
| Session user has a display/login value used in the profile menu. | confirmed | high |

## Candidate Flows For Future Flow Maps

| Future flow map | Current status | Next evidence needed |
|---|---|---|
| `auth/login` | placeholder | `src/components/auth/LoginForm.tsx` |
| `auth/guarded-route` | placeholder | `AuthGuard` plus provider/auth hook evidence |
| `auth/logout` | placeholder | `useAuth` logout behavior |
| `auth/session-restore` | placeholder | provider/auth hook evidence |

## Where To Look Next

- To understand login form behavior: `src/components/auth/LoginForm.tsx`
- To understand auth state and logout: `src/lib/hooks/useAuth.ts`
- To understand provider setup: `src/components/Providers.tsx`
