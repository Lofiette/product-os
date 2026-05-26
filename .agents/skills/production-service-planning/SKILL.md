---
name: production-service-planning
description: Plan production web/service work through phased orchestration: product, architecture, UI/DS, data/API, risk, release, and verification.
---


# production-service-planning

## Purpose

Create a phased plan for production-grade web services or modules.

## Procedure

1. Run or require repo-recon.
2. Classify service surface: UI-heavy, full-stack, API/service, data product, AI-enabled.
3. Define phases and gates.
4. Select roles only per phase.
5. Define acceptance criteria and verification strategy.
6. Identify risk roles and approval gates.

## Output schema

```markdown
## Production Service Plan

### Service/module purpose
### Surface classification
### Phases
| Phase | Goal | Roles | Skills | Artifact | Gate |
### Architecture boundaries
### UI/DS plan
### Data/API plan
### Risk gates
### Verification plan
### Release/rollback notes
### Open questions
```

## Stop conditions

- Required evidence is missing and the next step would require guessing.
- The skill would change approved scope.
- A risk gate requires user approval.
- Another role owns the decision and has not been consulted.

