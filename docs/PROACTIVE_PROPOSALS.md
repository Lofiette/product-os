# PROACTIVE_PROPOSALS.md

## Purpose

Define how Codex should propose improvements the user did not explicitly request.

## Proposal classes

| Class | Use when | Approval |
|---|---|---|
| Quality fix | Required to meet current acceptance criteria or gates | Can be included if no scope/risk change |
| Craft improvement | Improves clarity/consistency without scope change | Ask if non-trivial |
| Product opportunity | Changes user value, flow, feature, or acceptance criteria | Must ask |
| Risk mitigation | Reduces security/privacy/data/AI/release risk | Must ask if it changes implementation or scope |
| Exploration idea | Interesting but not needed now | Backlog unless user asks |

## Proposal discipline

Every proactive proposal must include:
- trigger;
- expected benefit;
- cost/complexity;
- impact on scope;
- affected roles/skills;
- whether it is now/next/later;
- exact approval question.

## Good proactive proposal

> “I found that the dashboard has a strong primary CTA but no recovery path for empty metrics. I recommend adding an empty-state guidance block. This does not change scope, uses existing EmptyState component, and improves first-run clarity. Approve adding it?”

## Bad proactive proposal

> “I improved the dashboard by adding onboarding, filters, export, and a new recommendations widget.”

Why bad:
- silent scope expansion;
- no evidence;
- no approval;
- multiple features disguised as polish.
