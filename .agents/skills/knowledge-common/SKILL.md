---
name: knowledge-common
description: >
  Use this skill whenever a task touches THIS application as a whole — before starting any
  feature, bug fix, review, or test work, or when someone asks "what is this application /
  what does it do / what rules apply to it". It is the entry point to the team's common
  knowledge: the application overview (purpose, users, high-level components, ownership)
  and the specific compliance and security standards the application must meet (e.g. PCI
  DSS for payments, data-residency, audit requirements). Read it first so that every other
  domain skill (product, testing, development) is applied in the right context. Do NOT use
  it for architecture or coding conventions (knowledge-development), roadmap or user
  journeys (knowledge-product), or test environments and policies (knowledge-testing) —
  this skill holds only the application-wide context and constraints.
id: KN-01
phase: Knowledge
version: 1.0.0
tags: [knowledge, common, application-overview, compliance, security-standards]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [the task at hand, artifacts under reference/]
outputs: [application context and compliance constraints applied to the task, with the reference file cited]
enterprise_tools: [GitLab]
---

# Knowledge — Common (application overview and compliance)

## When to use
Trigger this at the start of any work on the application, and whenever a decision depends
on what the application is for, who owns it, or which compliance and security standards
bind it. It is short by design: read it, load the relevant reference, then continue with
the task or hand off to the specific domain skill.

Boundary: application-wide context and constraints only. Architecture, dependencies and
coding standards live in **knowledge-development**; roadmap and user journeys in
**knowledge-product**; test environments, policies and tools in **knowledge-testing**.

## Inputs
- The task, feature, MR or question being worked on.
- The artifacts under `reference/` (converted to Markdown from the team's source documents),
  indexed below. Artifacts marked with a star are critical for initial onboarding and must
  exist before Devin starts delivery work on this application.

| Artifact | File under `reference/` | Critical | Update frequency | Responsible |
|---|---|---|---|---|
| Application overview — purpose, users, business capability, high-level components, ownership | `application-overview.md` | | One-time upload, refresh on major change | Team lead / PO |
| Compliance requirements and security standards specific to this application (e.g. PCI DSS for payments, PII handling, data residency, audit logging) | `compliance-and-security-standards.md` | ★ | One-time upload, refresh when regulation or scope changes | Team lead / PO |

## Workflow
1. **Identify what the task needs.** Decide whether it needs the application overview, the
   compliance/security standards, or both.
2. **Read the reference file(s).** Open the relevant file(s) under `reference/`. Read the
   whole file, not just the headings — compliance constraints are often in the detail.
3. **Extract the constraints that bind this task.** Note which compliance or security
   standards apply to the code, data or environment the task touches (e.g. card data must
   never be logged; PII fields must be encrypted at rest).
4. **Apply and cite.** Carry the constraints into the task. When they change a design or
   implementation choice, say so and cite the reference file and section.
5. **Flag gaps and staleness.** If a needed artifact is missing from `reference/`, outdated,
   or contradicts what you observe in the codebase, report it to the responsible team member
   rather than guessing — never infer compliance rules from the industry. Do not edit
   `reference/` files directly; they are synced from the team's source documents by the
   onboarding agent, which is the only sanctioned writer.
6. **Hand off.** Continue with the relevant domain skill (development, testing, product)
   or the SDLC skill for the task.

## Standards & references
- `reference/application-overview.md` — what the application is and who owns it.
- `reference/compliance-and-security-standards.md` — the binding compliance and security
  standards; these take precedence over team conventions and generic idiom.
- `../knowledge/README.md` — which knowledge skill to load for a given task, and the conventions
  shared by all four knowledge skills.
- Org-mandatory security rules always apply in addition to what is documented here,
  whichever skill enforces them.

## Output
The application context and compliance constraints relevant to the task, stated explicitly
and cited to the reference file, so downstream skills and reviewers can trace why a choice
was made.

## Quality checklist
- [ ] Relevant reference file(s) actually read, not assumed.
- [ ] Every compliance/security constraint affecting the task is listed and cited.
- [ ] Missing or stale artifacts reported, not invented.

## Anti-patterns
- Assuming compliance requirements from the industry instead of reading the team's document.
- Skipping this skill because the task "looks small" — compliance scope is decided here.
- Treating a missing artifact as "no constraints".
- Editing `reference/` files to fix a perceived error instead of reporting it.

## Handoff
→ **KN-04 knowledge-development** — architecture, dependencies, coding standards, environment setup.
→ **KN-02 knowledge-product** — roadmap and user journeys for feature context.
→ **KN-03 knowledge-testing** — test environments, policies and tools.
→ The delivery skill for the task — it must enforce the compliance and security constraints
   loaded here.
