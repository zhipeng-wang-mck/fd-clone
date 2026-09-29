---
name: knowledge-development
description: >
  Use this skill for ANY development task on this application — adding or changing a
  service, endpoint, integration or data flow; writing, refactoring or reviewing backend or
  frontend code; setting up or fixing the local dev environment; or answering "what am I
  allowed to build / what conventions apply here". It is the entry point to what the team
  REQUIRES of development work: the architecture constraints (forbidden and allowed
  dependencies, intentional boundaries, deprecations, approved versions, target state), the
  coding standards (conventions, unit-test standards, review rules), and the dev environment
  setup (access, configs, local services). Trigger it before repo navigation, code review,
  backend or frontend design work, and before any code you write. Do NOT use it to learn how
  the application is currently structured — read the codebase for that — and do NOT use it
  for test environments and policies (knowledge-testing), roadmap or user journeys
  (knowledge-product), or application-wide compliance rules (knowledge-common).
id: KN-04
phase: Knowledge
version: 1.0.0
tags: [knowledge, development, architecture-constraints, coding-standards, dev-environment]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [the development task or code under review, artifacts under reference/, the codebase]
outputs: [the constraints, conventions and environment rules that bind the task, with the reference file cited]
enterprise_tools: [GitLab]
---

# Knowledge — Development (constraints, coding standards, environment)

## When to use
Trigger this at the start of every development task, backend or frontend. Read what the team
requires from `reference/`, and only then start designing or coding.

This skill holds **rules, not descriptions**. It does not tell you how the application is
currently structured — its components, flows and dependencies are in the codebase, and you
read them there. What it tells you is what the team allows you to do with them.

That distinction carries one rule worth stating plainly: **what the code currently does is
not what the team permits.** A forbidden dependency that already exists is still forbidden. A
deprecated library still in use is still deprecated. Only
`reference/architecture-constraints.md` can tell you which is which, so never treat the
presence of something in the codebase as approval for adding more of it.

Boundary: what the team allows and how code is written. Test environments and policies live
in **knowledge-testing**; product intent in **knowledge-product**; application-wide
compliance and security standards in **knowledge-common** and take precedence over anything
here.

## Inputs
- The development task, MR or code under review.
- The artifacts under `reference/`, indexed below — what the team requires.
- The codebase itself — what currently exists.

| Artifact | File under `reference/` | Critical | Update frequency | Responsible |
|---|---|---|---|---|
| Architecture constraints — forbidden and allowed dependencies, intentional boundaries and the reason for each, deprecated components and libraries, approved versions, target-state changes already agreed | `architecture-constraints.md` | | Refresh when a boundary, deprecation or target-state decision changes | Tech lead |
| Coding standards — naming and structure conventions, language/framework versions, lint/format config, unit-test standards, error handling, logging, MR review rules | `coding-standards.md` | | Refresh when conventions change | Tech lead |
| Dev environment setup — prerequisites and access (VPN, roles, licensed tooling), configs and secrets handling (placeholders only), local services/mocks, common issues | `dev-environment-setup.md` | | Refresh when tooling, access or configs change | Tech lead |

No artifact in this domain is critical for initial onboarding, and not every team has
constraints to state. When one is missing, say so and fall back to what the codebase shows,
stating that you did — but never infer a constraint the team has not written down, in either
direction.

## Workflow
1. **Scope the task against the codebase.** Identify the components, flows, dependencies and
   contracts the task touches. Treat what you find as description, not permission.
2. **Check what the team allows.** Open `reference/architecture-constraints.md`. Confirm the
   change does not cross a forbidden boundary, add a deprecated or unapproved dependency, or
   build deeper into something the target state removes. Do not introduce a new dependency
   without noting it is new.
3. **Load the coding standards.** Open `reference/coding-standards.md` and apply naming,
   structure, framework versions, lint/format, unit-test and review rules as you write or
   review. Prefer the team's stated patterns over generic idiom.
4. **Keep integration contracts compatible.** For any API or event change, keep the contract
   backward compatible or flag the breaking change explicitly, and update its specification
   in the codebase alongside the code.
5. **Set up or verify the environment when needed.** For local runs or tests, follow
   `reference/dev-environment-setup.md`; never hardcode secrets — use the documented
   placeholders and CI variables.
6. **Apply and cite.** Carry the constraints into the design, code or review, citing the
   reference file and section when they drive a decision.
7. **Report drift.** Where the codebase contradicts a stated constraint — a forbidden
   dependency that already exists, a deprecated library still in use — report it to the tech
   lead rather than treating the code as permission. Do not edit `reference/` files directly;
   the onboarding agent is the only sanctioned writer.

## Standards & references
- `reference/architecture-constraints.md` — what must not be built, and why.
- `reference/coding-standards.md` — conventions, unit-test standards, MR rules.
- `reference/dev-environment-setup.md` — access, configs, local run.
- `../README.md` — which knowledge skill to load for a given task, and the conventions
  shared by all four knowledge skills.
- **knowledge-common** compliance and security standards, and org-mandatory security rules,
  take precedence over any team convention here.

## Output
The constraints, conventions and environment rules that bind the task, stated explicitly and
cited to the reference file, so that the resulting design, code or review is traceable to a
named source rather than to inference.

## Quality checklist
- [ ] Change checked against the stated constraints — boundaries, deprecations, approved versions, target state.
- [ ] New or changed dependencies called out explicitly.
- [ ] Coding standards applied (naming, structure, versions, unit tests, review rules).
- [ ] Integration contracts kept compatible, or breaking changes flagged and the specification updated.
- [ ] No secrets or hostnames hardcoded; environment setup followed.
- [ ] Drift between the codebase and the stated constraints reported, not silently accepted.

## Anti-patterns
- Treating something the codebase already does as something the team permits.
- Expecting this skill to describe the architecture; it holds rules, not descriptions.
- Inferring a constraint the team never wrote down, in either direction.
- Coding from generic framework idiom when the team's standard says otherwise.
- Changing an API without updating its specification in the codebase.
- Building further into a component the target state says is being removed.
- Editing `reference/` files by hand instead of re-running onboarding with a corrected source.

## Handoff
→ **KN-03 knowledge-testing** — how to test the change.
→ The repo-navigation skill for the task — locate the code areas the change touches.
→ The code-review skills for the task — apply and review against the coding standards loaded here.
→ The design skills for the task — backend, database and frontend design all work within the
   constraints loaded here.
