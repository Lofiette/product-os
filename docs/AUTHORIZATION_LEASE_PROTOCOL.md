# Scoped Authorization Lease Protocol

## Purpose

Record one bounded user approval package instead of asking for approval before every routine command.

## Scope

A lease may include:

- read path globs;
- write path globs;
- exact verification commands;
- bounded worker delegation;
- explicit forbidden operations;
- expiration conditions.

## Important boundary

A CPT lease is runtime memory, not a security boundary. Native Codex sandbox, permission, approval, organizational, and operating-system controls remain authoritative.

## Lifecycle

```text
proposed → active → consumed
                 ↘ expired
                 ↘ revoked
```

Renew or replace the lease when:

- scope expands;
- a dependency, migration, public API, network, or destructive operation appears;
- a new worker type is needed;
- the task changes materially;
- an expiration condition is reached.

## Minimum request

Before requesting approval, present:

- objective;
- read scope;
- write scope;
- verification commands;
- delegation budget;
- forbidden operations;
- expiration.
