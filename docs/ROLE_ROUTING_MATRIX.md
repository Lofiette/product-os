# ROLE_ROUTING_MATRIX.md

## By operation

### Screen creation/redesign / UI prototype
Required: product_designer.
Usually: design_system_guardian, design_engineer, ux_writer, qa_engineer.
Conditional: ux_researcher, accessibility_specialist, visual_design_director, information_architect, data_visualization_designer, frontend_architect.

### Existing repo UI implementation
Required: repo-recon skill, design-recon skill, design_engineer, frontend_architect.
Usually: design_system_guardian, qa_engineer.

### No design system UI prototype
Required: product_designer, design_engineer.
Usually: ux_writer, qa_engineer.
Optional: design_system_guardian to create lightweight local consistency rules.

### Governed design system
Required: design_system_guardian, design_engineer, design-recon, design-system-compliance.
Custom UI requires approval.

### AI tool-using agent
Required: ai_ml_systems_architect, model_evaluation_specialist, ai_safety_reviewer, security_reviewer, privacy_compliance_reviewer, qa_engineer.

### Research-only
Select the relevant researcher only. Do not implement.

### Backend/API change
Backend Architect, API Contract Guardian, QA Engineer; risk roles if data/auth/security.

### Service journey
Service Designer, CX Researcher, Product Strategist, Business Analyst.

### Dashboard/report
Data Visualization Designer, Analytics Engineer, Product Designer, QA Engineer.


## 2.0 beta 1 additions

### Quick UI prototype without a design system
Required:
- product_designer
- design_engineer

Usually include:
- design_system_guardian, to create a lightweight Prototype UI Kit Contract
- ux_writer, if user-facing copy/states matter

Required skills:
- design-recon
- prototype-ui-kit
- screen-redesign
- state-matrix
- ui-heuristic-audit

### Module design for later developer rebuild
Required:
- product_designer
- information_architect
- design_system_guardian
- ux_writer
- design_engineer as feasibility/handoff reviewer
- qa_engineer as design QA reviewer

Required skills:
- design-recon
- module-design
- design-system-manifest, if DS exists
- design-system-compliance
- design-handoff-qa
- handoff-docs

Do not implement code unless the user approves implementation.

### Production web service with design system in code
Use phased orchestration.
Phase 1: repo-recon and design-recon.
Phase 2: product/architecture/design plan.
Phase 3: risk/readiness gates.
Phase 4: implementation.
Phase 5: verification and review.

Required skills usually include:
- production-service-planning
- production-readiness-review
- design-system-compliance
- ds-code-contract-enforcement
- implementation-review
