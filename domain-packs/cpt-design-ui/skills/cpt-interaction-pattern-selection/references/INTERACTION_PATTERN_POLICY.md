# Interaction Pattern Knowledge Policy

Policy ID: `cpt-interaction-pattern-policy-v1`
Source basis: Jenifer Tidwell, Charles Brewer, and Aynne Valencia, *Designing Interfaces*, third edition.
Status: transformed operational summary; the source book is not bundled.

## Purpose

Use the source as a vocabulary for recurring interaction problems, not as a template gallery. A pattern is a reusable response to a problem under recognizable forces. It is never a substitute for product evidence, domain modeling, accessibility, platform conventions, or an authoritative design system.

## Source authority

1. Verified user and product evidence.
2. Approved domain, workflow, risk, and technical constraints.
3. Authoritative product and design-system patterns.
4. Current platform and accessibility requirements supplied by the project.
5. This transformed catalog.
6. Historical examples from the source.

## Interpretation rules

- Select patterns by problem, context, forces, and consequences, not by visual resemblance.
- Treat the page as a composition: page type + navigation + command model + state/recovery model.
- Separate domain/data structure from representation before choosing UI.
- Preserve recognizable conventions when they reduce learning cost; break them only for a demonstrated user need.
- Account for novice and expert use separately. Guidance, density, shortcuts, and customization are not mutually exclusive.
- Support safe exploration, interruption, re-entry, incremental work, spatial memory, repetition, and keyboard operation where the context demands them.
- Pattern examples from 2019 and earlier are historical evidence of an idea, not present-day visual direction.
- Social proof, infinite feeds, carousels, animation, and proactive behavior are contextual options with manipulation, attention, accessibility, and control risks.
- Any current ARIA, browser, device, or platform behavior requires current project evidence or separate verification.

## Pattern composition test

Before accepting a composition, answer:

1. What user goal and decision does it support?
2. What page/workflow type dominates?
3. What objects and relationships must remain legible?
4. What behavior lenses are active?
5. How does the user enter, orient, act, recover, leave, and return?
6. How does the model change for novice, expert, keyboard, touch, and narrow contexts?
7. Which alternative composition was rejected and why?
8. What evidence would falsify the choice?
