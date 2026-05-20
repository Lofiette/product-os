# RISK_POLICY.md

Use this file to trigger additional roles and approval gates.

## Security triggers

Activate Security Reviewer when work touches:
- authentication or authorization;
- roles/permissions;
- secrets/tokens/API keys;
- user-generated content;
- file upload/download;
- redirects;
- payments/billing;
- injection surfaces;
- multi-tenant isolation;
- admin features.

## Privacy and compliance triggers

Activate Privacy & Compliance Reviewer when work touches:
- personal data;
- sensitive data;
- analytics/tracking;
- consent;
- data export/import;
- deletion/retention;
- audit logs;
- regulated contexts.

## Performance triggers

Activate Performance Engineer when work touches:
- large lists/tables;
- heavy rendering;
- expensive queries;
- search;
- caching;
- media;
- realtime;
- slow routes;
- bundle size.

## Dependency triggers

Activate Dependency Curator before adding or replacing production dependencies.

## Migration triggers

Activate Migration Planner before:
- database schema changes;
- data migrations;
- backfills;
- destructive data changes;
- changing identifiers or references.

## Release/operations triggers

Activate DevOps & Release Engineer and Observability Engineer when work touches:
- CI/CD;
- infrastructure;
- deployment;
- environments;
- feature flags;
- production rollout;
- monitoring/logging/alerts.

## Incident triggers

Activate Incident Investigator when there is an outage, production bug, user-visible degradation, security event, or data integrity issue.
