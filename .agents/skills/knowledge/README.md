# Knowledge Skills — application context loaded on demand

Four skills that carry the team's knowledge about **this application**. Each one is an
index: the `SKILL.md` says when the knowledge applies and which file to open, and the
actual knowledge lives in that skill's `reference/` folder.

| ID | Skill | Holds |
|---|---|---|
| KN-01 | [knowledge-common](./knowledge-common) | Application overview; the compliance and security standards that bind it. |
| KN-02 | [knowledge-product](./knowledge-product) | Product roadmap; existing user journey maps. |
| KN-03 | [knowledge-testing](./knowledge-testing) | Test environments, test policies, test patterns and tools. |
| KN-04 | [knowledge-development](./knowledge-development) | Architecture constraints, coding standards, dev environment. Rules only — how the code is *currently* built is read from the codebase. |

## Which knowledge to load

Load only what the task needs. Loading all four on every task wastes context and buries the
constraints that actually bind the work.

| Task | Load | Also load when relevant |
|---|---|---|
| Backend service, endpoint, integration or data-flow change | **KN-04** development | KN-01 common |
| Frontend screen or component change | **KN-04** development | KN-01 common; KN-02 product if the user-facing flow changes |
| Interpreting or refining a feature request / user story | **KN-02** product | KN-01 common |
| Prioritisation, sequencing, "is this planned?" | **KN-02** product | — |
| Writing, generating or running tests; test plan | **KN-03** testing | KN-04 for unit-test conventions; KN-01 for test-data rules |
| Code review / MR review | **KN-04** development | KN-01 common |
| Security, compliance or data-handling question | **KN-01** common | — |
| Local dev environment setup or breakage | **KN-04** development | — |
| Wireframes or UX design | **KN-02** product | KN-04 for the API contract |
| Release readiness, change request | **KN-01** common | KN-03 testing |
| First-time onboarding to the application | **KN-01** common | then all three domain skills |

Two standing rules:

- **KN-01 common comes first** whenever the task touches code, data or an environment — it
  decides the compliance scope everything else works inside.
- **Precedence:** KN-01 compliance and security standards, plus org-mandatory security rules,
  override any convention documented in KN-02, KN-03 or KN-04.

## Conventions shared by all four

- **`reference/` holds the knowledge; `SKILL.md` holds the routing.** Read the whole
  reference file, not just its headings.
- **Never edit `reference/` files.** They are synced from the team's source documents or
  regenerated from the codebase. Report an error to the responsible owner instead.
- **Cite what you applied.** Name the reference file and section whenever it changes a
  design, implementation or test decision.
- **A missing artifact is a gap, not an absence of constraints.** State the gap and ask the
  named owner. Do not infer the content.
- **★ marks artifacts critical for initial onboarding.** They must exist before Devin starts
  delivery work on the application.

## Critical artifacts

Each skill's `SKILL.md` declares its own artifacts, with the `★` flag, refresh cadence and owner.
Those tables are the only place that list lives — read them rather than a copy.

**KN-04 development has no `★` artifacts.** Architecture, dependencies and API contracts are read
from the codebase rather than uploaded, so delivery work can start without a tech lead providing
anything. Its artifacts hold only what the team *requires*, and not every team has constraints to
state. For how that codebase documentation is generated, see
[`.devin/README.md`](../../../.devin/README.md).

## Onboarding status

Each domain also carries an `onboarding-status.md` beside its `SKILL.md`, written by the
onboarding agent (`!onboarding`) and read by anything that needs to know whether a domain is
ready.

```markdown
# Onboarding status — knowledge-product

> Maintained by the onboarding agent (`!onboarding`). Do not edit by hand.

| Artifact | Status |
|---|---|
| product-roadmap.md | done |
| user-journey-maps.md | n/a |
```

- Exactly three values: `done`, `pending`, `n/a`.
- One row per artifact the skill's table declares, in the same order.
- The template ships **no** status files. The first `!onboarding` session creates them, so an absent
  file means that domain has never been audited. Do not add empty stubs.
- Absent, empty, or unreadable are equivalent: every artifact in that domain is `pending`.
- The file is not an artifact. Never count it in coverage.
