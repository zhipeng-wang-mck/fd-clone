---
name: knowledge-product
description: >
  Use this skill when a task needs PRODUCT context for this application — interpreting or
  refining a feature request or user story, prioritising or sequencing work, checking
  whether a change fits the roadmap, or understanding how users move through the product.
  It is the entry point to the team's product knowledge: the product roadmap (themes,
  planned features, PI/quarter sequencing, dependencies) and the existing user journey
  maps (personas, steps, touchpoints, pain points). Trigger it during requirements and
  design work — feature intake, requirements Q&A, capability gap analysis, feature
  definition, wireframing, frontend design — and whenever someone asks "is this planned /
  what comes next / how does the user do X today". Do NOT use it for technical
  architecture or coding conventions (knowledge-development) or for test policies
  (knowledge-testing) — this skill holds what the product is meant to become and how users
  experience it, not how it is built.
id: KN-02
phase: Knowledge
version: 1.0.0
tags: [knowledge, product, roadmap, user-journeys, requirements, prioritisation]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [feature request / story / question, artifacts under reference/]
outputs: [roadmap and user-journey context applied to the task, with the reference file cited]
enterprise_tools: [Rally, GitLab]
---

# Knowledge — Product (roadmap and user journeys)

## When to use
Trigger this when the right answer depends on product intent: what is planned, in which
order, for which users, and how those users currently experience the product. Typical
moments: shaping a Rally feature, judging overlap with planned work, designing a screen or
flow, or explaining the "why" behind a change.

Boundary: product direction and user experience only. How the system is built lives in
**knowledge-development**; how it is tested in **knowledge-testing**; application-wide
compliance constraints in **knowledge-common**.

## Inputs
- The feature request, story, design question or prioritisation question at hand.
- The artifacts under `reference/` (converted to Markdown from the team's source documents),
  indexed below. Artifacts marked with a star are critical for initial onboarding.

| Artifact | File under `reference/` | Critical | Update frequency | Responsible |
|---|---|---|---|---|
| Product roadmap — themes, planned features/epics, PI or quarter sequencing, key dependencies and milestones | `product-roadmap.md` | ★ | Quarterly (after PI planning) and ad-hoc on re-prioritisation | Team lead / PO |
| Existing user journey maps — personas, journey steps, touchpoints, systems involved, known pain points | `user-journey-maps.md` | | Ad-hoc when journeys change | Team lead / PO |

## Workflow
1. **Identify the product question.** Is it about roadmap fit (is this planned, when, with
   what dependencies) or about user experience (how does the user do this today, where are
   the pain points), or both?
2. **Read the reference file(s).** Open `reference/product-roadmap.md` and/or
   `reference/user-journey-maps.md`. The roadmap is time-bound: check its stated period or
   version and whether that period is still current before relying on it.
3. **Locate the task in the product picture.** Map the request to a roadmap theme, epic or
   milestone, and to the user journey step(s) it affects. Note related or overlapping
   planned items.
4. **Derive the implications.** State what the product context means for the task: scope
   that is already planned elsewhere, sequencing constraints, personas affected, pain
   points the change should address or must not worsen.
5. **Apply and cite.** Carry these implications into the feature brief, design or
   decision, citing the reference file and section.
6. **Flag gaps and staleness.** If a file is missing, the roadmap period has passed, the
   journey map does not cover the affected flow, or the codebase contradicts the documented
   journey, ask the PO for the current version rather than inventing one. Do not edit
   `reference/` files directly; they are synced from the team's source documents by the
   onboarding agent, which is the only sanctioned writer.

## Standards & references
- `reference/product-roadmap.md` — the current roadmap; treat items as intent, not
  commitment, unless marked committed.
- `reference/user-journey-maps.md` — the as-is user journeys.
- `../knowledge/README.md` — which knowledge skill to load for a given task, and the conventions
  shared by all four knowledge skills.
- Application-wide compliance constraints from **knowledge-common** still apply to any
  product change.

## Output
The roadmap and user-journey context relevant to the task — theme/epic fit, sequencing
constraints, affected personas and journey steps — stated explicitly and cited, ready to
feed a feature brief, design spec or prioritisation decision.

## Quality checklist
- [ ] Roadmap period/version checked and still current.
- [ ] Task mapped to a roadmap item (or explicitly identified as unplanned).
- [ ] Affected personas and journey steps named.
- [ ] Overlap with other planned items surfaced.
- [ ] Missing or stale artifacts reported, not invented.

## Anti-patterns
- Using an expired roadmap as if it were current.
- Inventing personas or journey steps that are not in the journey map.
- Treating roadmap intent as a hard commitment (or the reverse) without checking its status.
- Skipping the journey map for "backend-only" changes that still alter user outcomes.

## Handoff
→ **KN-04 knowledge-development** — for how the affected capability is built today.
→ The requirements skills for the task — feature intake, capability gap analysis and feature
   definition all consume this product context.
→ The design skills for the task — wireframing and frontend design work from the journey maps.
