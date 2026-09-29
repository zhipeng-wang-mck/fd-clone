---
name: knowledge-testing
description: >
  Use this skill when a task involves TESTING this application — writing or running tests,
  generating test cases or a test plan, choosing where and how to run tests, analysing
  coverage, or validating a change before an MR or release. It is the entry point to the
  team's testing knowledge: the test environment description (environments, URLs/hosts as
  placeholders, test data, access, refresh cadence), the test policies (e.g. performance
  testing parameters, coverage thresholds, mandatory test types per change), and the test
  patterns and tools in use (frameworks, harnesses, naming and layout conventions). Trigger
  it before coverage analysis, test-case generation or test-plan authoring, and before any
  "test the app" step. Do NOT use it for
  unit-test coding conventions embedded in the coding standards (knowledge-development) or
  for product acceptance intent (knowledge-product) — this skill covers the test
  environments, policies and tooling the team uses.
id: KN-03
phase: Knowledge
version: 1.0.0
tags: [knowledge, testing, test-environment, test-policy, test-tools, quality]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [the change or feature to be tested, artifacts under reference/]
outputs: [applicable test environment, policies and tooling for the task, with the reference file cited]
enterprise_tools: [GitLab]
---

# Knowledge — Testing (environments, policies, patterns and tools)

## When to use
Trigger this whenever a task requires the team's testing setup or rules: which environment
to use, what test data exists, which tests are mandatory for this kind of change, what
performance parameters apply, and which frameworks and patterns the team expects. Read it
before designing, generating or running tests.

Boundary: environments, policies, patterns and tools. Coding-level unit-test conventions
sit with the coding standards in **knowledge-development**; acceptance intent comes from
**knowledge-product**; compliance constraints on test data (e.g. no production PII) from
**knowledge-common**.

## Inputs
- The change, feature or MR to be tested, and its risk/impact if known.
- The artifacts under `reference/` (converted to Markdown from the team's source documents),
  indexed below. Artifacts marked with a star are critical for initial onboarding.

| Artifact | File under `reference/` | Critical | Update frequency | Responsible |
|---|---|---|---|---|
| Test environment description — environments (dev/SIT/UAT/perf), purpose of each, hosts as placeholders, access model, test data sets, refresh cadence, known limitations | `test-environment-description.md` | ★ | One-time upload, refresh on environment change | QA lead |
| Test policies — mandatory test types per change class, coverage thresholds, performance testing parameters (load profile, SLO targets), regression scope, exit criteria | `test-policies.md` | | One-time upload, refresh on policy change | QA lead |
| Test patterns and tools used — frameworks, runners, mocking/contract-testing tools, test layout and naming conventions, CI test stages, reporting | `test-patterns-and-tools.md` | | One-time upload, refresh when tooling changes | QA lead |

## Workflow
1. **Classify the testing need.** Determine which test types the task requires (unit,
   integration, contract, end-to-end, performance, security) and at which stage.
2. **Read the reference file(s).** Open the relevant files under `reference/`: environment
   description for where to run, policies for what is mandatory, patterns and tools for
   how to write and structure tests.
3. **Select the environment and data.** Pick the environment appropriate to the test type
   and note its access model, test data set and limitations. Never use production data or
   hosts unless the environment description explicitly permits it.
4. **Apply the policies.** Identify the mandatory tests, coverage thresholds, performance
   parameters and exit criteria that bind this change class.
5. **Follow the patterns and tools.** Use the team's frameworks, layout and naming
   conventions; reuse existing harnesses and fixtures before creating new ones.
6. **Apply and cite.** Carry the environment, policy and tooling choices into the test
   plan, test cases or test run, citing the reference file and section.
7. **Flag gaps and staleness.** If a file is missing, an environment described does not match
   reality, a policy conflicts with CI configuration, or tooling has moved on, report it to
   the QA lead — never assume an environment exists or a threshold applies. Do not edit
   `reference/` files directly; they are synced from the team's source documents by the
   onboarding agent, which is the only sanctioned writer.

## Standards & references
- `reference/test-environment-description.md` — where tests run and with what data.
- `reference/test-policies.md` — what is mandatory and the bar to pass.
- `reference/test-patterns-and-tools.md` — how tests are written and executed here.
- `../README.md` — which knowledge skill to load for a given task, and the conventions
  shared by all four knowledge skills.
- Compliance constraints on test data from **knowledge-common** take precedence.

## Output
The applicable test environment, mandatory tests and thresholds, and tooling/pattern
choices for the task, stated explicitly and cited, ready to feed test-case generation, a
test plan or a test run.

## Quality checklist
- [ ] Environment chosen matches the test type and its documented purpose.
- [ ] Mandatory test types and thresholds for this change class identified.
- [ ] Performance parameters applied where the policy requires a performance test.
- [ ] Team frameworks, layout and naming conventions followed.
- [ ] No production data or hosts used without explicit permission in the reference.
- [ ] Missing or stale artifacts reported, not invented.

## Anti-patterns
- Running tests against an environment because it "seems right" without checking its purpose.
- Introducing a new test framework when the team already standardises on one.
- Ignoring performance parameters for a change the policy classes as performance-relevant.
- Treating a missing policy file as "no thresholds apply".

## Handoff
→ **KN-04 knowledge-development** — for unit-test conventions inside the coding standards.
→ The testing skills for the task — coverage/hotspot analysis, test-case generation and
   test-plan authoring all consume the environment, policies and tools loaded here.
→ The release-readiness skill for the task — testing evidence for the go-live decision.
