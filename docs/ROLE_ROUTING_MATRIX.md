# ROLE_ROUTING_MATRIX.md

Use this matrix to select the smallest sufficient team.

| Task signal | Required / likely roles | Optional triggers |
|---|---|---|
| Unknown or new task | Task Intake Orchestrator, Team Architect, Chronicle Keeper | Consistency Auditor for complex tasks |
| Market/category uncertainty | Market Researcher, Product Strategist | Business Analyst, Domain Expert |
| User behavior/usability uncertainty | UX Researcher, UX Interaction Reviewer | UX Writer, Accessibility Specialist |
| Customer journey/service issue | CX Researcher, Product Strategist | Business Analyst, UX Researcher |
| New product feature | Product Strategist, UX Interaction Reviewer, relevant architects, QA Engineer | UX Writer, Design System Guardian, Security, Privacy, Performance |
| UI-heavy work | UX Interaction Reviewer, UX Writer, Design System Guardian, Frontend Architect, QA Engineer | Visual Design Director, Accessibility Specialist |
| Visual identity/UI polish | Visual Design Director, Design System Guardian, UX Interaction Reviewer | UX Writer |
| Copy/content/error states | UX Writer, UX Interaction Reviewer | Product Strategist, Accessibility Specialist |
| Web frontend | Frontend Architect, QA Engineer | Design System Guardian, Performance Engineer |
| Backend/API | Backend Architect, API Contract Guardian, QA Engineer | Security Reviewer, Data Architect |
| Mobile app | Mobile Architect, UX Interaction Reviewer, QA Engineer | Accessibility, Release Engineer |
| Data model/storage | Data Architect, Backend Architect | Migration Planner, Privacy Reviewer |
| Analytics/tracking | Analytics Engineer, Product Strategist, Data Architect | Privacy Reviewer |
| Auth/permissions/secrets/user-generated content | Security Reviewer | Privacy Reviewer, Backend Architect |
| Personal/sensitive data | Privacy & Compliance Reviewer | Security Reviewer, Data Architect |
| Performance complaints or heavy rendering/queries | Performance Engineer | Frontend/Backend/Data architects |
| New dependency | Dependency Curator | Security Reviewer, Performance Engineer |
| Database migration/data deletion | Migration Planner, Data Architect, Backend Architect | Release Engineer, Privacy Reviewer |
| Deployment/CI/CD/release | DevOps & Release Engineer | Observability Engineer, Security Reviewer |
| Monitoring/incident readiness | Observability Engineer | DevOps & Release Engineer, Incident Investigator |
| Production incident | Incident Investigator, Observability Engineer, relevant architects | Security Reviewer, Release Engineer |
| Existing diff/PR | Code Reviewer, QA Engineer | Security, Performance, UX/A11y depending on affected area |
| Documentation/handoff | Technical Writer, Chronicle Keeper | Product Strategist, relevant architects |

## Rule of thumb

- Use research roles before building when the problem, users, market, or journey is uncertain.
- Use design roles before building when the task affects user-facing flows, UI, copy, accessibility, or visual identity.
- Use risk roles when production, data, auth, infrastructure, dependencies, or compliance are touched.
- Use review roles after a diff exists.
