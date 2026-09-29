---
name: onboard-knowledge
description: >
  Use this skill to onboard an application's knowledge, or to re-check it later — auditing what
  the team has documented against what the knowledge skills declare, collecting the source
  documents the owner can supply, and delivering the result as a merge request. Trigger it when
  someone asks to onboard an application, to check knowledge coverage, to find out what
  documentation is missing before delivery work starts, or when the `!onboarding` playbook runs.
  It audits one role's domains per session: a product owner covers product and common, a QA lead
  covers testing, a tech lead covers development. Do NOT use it to write the knowledge itself, to
  author a document the owner has not supplied, or to decide what knowledge a domain should hold —
  that is declared by each knowledge skill's artifact table, which this skill only reads.
id: UT-02
phase: Utility
version: 1.0.0
tags: [utility, onboarding, knowledge, audit, coverage, gitlab]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [the user's role, organization name, source documents the owner supplies]
outputs: [updated onboarding-status.md per in-scope domain, one merge request, a closing coverage message]
enterprise_tools: [GitLab]
---

# Onboard Knowledge

## When to use
Run this when an application is being onboarded, or when its knowledge is being re-checked. It
answers one question: **which artifacts does this application have, and which are still missing.**

**One session, one role.** Onboarding takes several sessions run by different people. The role is
fixed once confirmed and never changes mid-session — a second role means a second session.

Each domain carries an `onboarding-status.md` beside its `SKILL.md`. Reading it first is what stops
a later session redoing finished work.

Boundary: this skill audits and collects. It never writes knowledge content, and it never decides
what a domain should hold — each knowledge skill's artifact table declares that.

## Inputs
- **The user's role** — the only answer you genuinely need, because it is a scoping decision rather
  than a fact. Take it from the macro argument (`!onboarding <organization> <role>`) when one was
  given; otherwise ask. It fixes the domains in scope:

| Role | Macro argument | Domains in scope |
| --- | --- | --- |
| Team lead / Product Owner | `product-owner` | `knowledge-common`, `knowledge-product` |
| Tech lead / Developer | `tech-lead` | `knowledge-development` |
| QA lead / Tester | `qa` | `knowledge-testing` |
| Cross-functional / Full audit | `full` | all four |

- **Organization name**, for labelling the output. Take it from the macro argument when one was
  given; otherwise ask alongside the role.
- **Source documents** the owner supplies, attached to the session.

## Workflow

### 1. Find the knowledge repository
Look through the repositories cloned into this session for one containing `.agents/skills/knowledge/`. That
folder is the fingerprint. Sessions boot with the organization's configured repositories already
cloned, so this is a precondition to check, not something you can arrange.

- One match — the normal case. Use it and name it in your first message.
- Several matches — list them and ask the user to pick one, and ask nothing else yet. Never choose
  by guessing which repository name looks like the organization.
- No match — stop. Report that an admin must connect the repository to the organization's git
  integration and add it to the environment blueprint (Settings → Environment → Blueprints), and
  that onboarding resumes once a session boots with it cloned.

- **Never:** ask the user for a repository name or URL before looking; clone it; continue past this
  step without it; audit a different repository instead.
- **Done when:** exactly one knowledge repository is identified — or you have stopped with the
  blocker, having asked the user nothing.

### 2. Confirm scope
Take the organization name and role from the macro arguments when given. Ask only for what is
still missing, in one grouped question. When the role is asked, say in that question that a session
audits one role only, and that someone who holds several roles should pick Cross-functional / Full
audit rather than run one session per role. A role argument that matches no row of the table is
missing: ask. State the confirmed role and its domains back to the user before grading anything.

- **Never:** widen the scope; audit a second role however the user asks; infer the role from a job
  title.
- **Done when:** one role is confirmed — by macro argument or by answer — and you have named its
  domains back to the user.
- **Revisit if:** never. A different role is a different session.

### 3. Refresh DeepWiki
DeepWiki is how the code itself gets documented, and it does not regenerate on its own when
`.devin/wiki.json` or the code changes. The code is the development domain's concern, so this step
runs only when `knowledge-development` is in scope (`tech-lead` or `full`); for any other role, skip
it and say nothing about DeepWiki.

Read the `## DeepWiki` section of `.agents/skills/knowledge/knowledge-development/onboarding-status.md`,
then compare it with the default branch:
`git rev-parse origin/<default>` for the commit, and `git rev-parse origin/<default>:.devin/wiki.json`
for the `wiki.json` blob (`absent` if there is no file).

- Both match the recorded row and its result is `generated` — skip regeneration, and say so.
- Otherwise — the section is absent, either value differs, or the last result was not `generated` —
  regenerate the wiki for this repository with Devin's wiki-generation tool (`devin_generate_wiki`).
  Running `!onboarding` is the request to regenerate it. Wait for the tool to finish.
- Not running in Devin, or the tool is unavailable — do not regenerate; the result is `skipped`.

Record the date, commit, blob, result (`generated`, `skipped` or `failed`) and wiki link for step 9.

- **Never:** block the audit on this step — a failed or skipped refresh is recorded and the session
  carries on; regenerate for a branch other than the default branch.
- **Done when:** `knowledge-development` is out of scope; or the wiki was regenerated, found
  current, skipped or failed — and the user has been told which.

### 4. Read prior status
Read `.agents/skills/knowledge/<skill>/onboarding-status.md` for each in-scope domain.

**Absent, empty, or unreadable all mean the same thing: every artifact in that domain starts as
`pending`.** A first onboarding hits this for every in-scope domain — that is the expected state, not
an error. Say so and carry on. Where the file does have rows, take their statuses as they stand.

- **Takes:** the in-scope domain list from step 2.
- **Never:** treat a missing or empty file as a problem; trust `done` as proof a file still exists;
  reset `done` or `n/a` to `pending` unless the file has gone missing.
- **Done when:** every in-scope artifact has a starting status — `done`, `n/a`, or `pending` — and
  you have said in your opening summary how many you are skipping. On a first run that is none.

### 5. Build the gap list
Gather three lists, in this order:

1. **Prior** — the statuses from step 4.
2. **Expected** — read each in-scope `SKILL.md` and take its artifact table: filename, `★` flag,
   cadence, owner. That table is the only checklist. Audit what it declares and nothing else.
3. **Present** — list each `reference/` folder, ignoring `README.md` and `onboarding-status.md`.

Then grade each expected artifact by lookup, not judgement:

| Prior status | File present | Grade | Read the file? |
| --- | --- | --- | --- |
| `done` | yes | `DOCUMENTED` | no |
| `done` | no | `MISSING`, and report it as drift | no |
| `n/a` | either | `NOT APPLICABLE` | no |
| `pending`, or no prior | yes | `DOCUMENTED` or `THIN` | yes, in full |
| `pending`, or no prior | no | `MISSING` | no |

Where the table says to read:

- `DOCUMENTED` — a reader could act on it today.
- `THIN` — present but unusable: a rule with no reject condition, a command with no directory, a
  target with no number, a role with no named person. An empty template — headings with no content —
  is `MISSING`, not `THIN`.

`NOT APPLICABLE` is only ever set by the owner confirming it in step 7, with a reason.

Then for every artifact graded:

- Cite the filename and section, except for `MISSING`.
- For every `THIN`, name the one missing specific — that sentence is the writing brief for whoever
  fixes it.
- Flag a `DOCUMENTED` artifact as stale only when its own content names a period or version that has
  passed.

- **Takes:** the three lists above.
- **Never:** invent an artifact no table declares; drop one a table does declare; grade from a
  filename, a heading, or a directory listing; read a file the lookup says not to; infer staleness
  from the cadence alone.
- **Done when:** every in-scope artifact has a grade, and every grade except `MISSING` has its
  evidence.

### 6. Tier the gaps
A `★` artifact that is not `DOCUMENTED` is always `BLOCKING`, without judgement. Tier the rest:

- `BLOCKING` — *can an agent begin the task at all?* Without it the work is guesswork.
- `DEGRADING` — *would a reviewer reject the output for missing a standard nobody wrote down?*
- `DEFERRABLE` — *does anything break this sprint if it stays missing?* Absence costs humans.

- **Never:** tier a `★` gap as anything but `BLOCKING`; leave a non-obvious tier unexplained.
- **Done when:** every gap sits in one tier, ordered within its tier by how much the work depends on
  it — the gap that blocks the most downstream work first.

### 7. Report and ask
Show coverage and the tiered gaps first, so the owner sees the shape of the ask. Then, in one
grouped blocking question, request: the source document for each `MISSING` and `THIN` artifact; a
newer document for anything flagged stale; and confirmation of each `NOT APPLICABLE` with its reason.

Say that they may attach everything at once or a few at a time, and ask them to tell you when they
have nothing further. That sentence is what lets step 8 know when to stop waiting.

- **Never:** ask about an out-of-scope domain, or about an artifact already `done` or `n/a`; ask one
  question at a time — an audit producing forty questions gets none answered.
- **Done when:** the owner has answered, or has said they cannot supply something. "I don't have
  that" is a complete answer: record the gap and move on without pressing.

### 8. Ingest the documents
Ask once, in step 7 — never file by file. But **process each document as it arrives**, whether the
owner attaches everything at once or a few at a time. Order does not matter, and one document's
failure never holds up another.

This step stays open until the owner says they have nothing further. If they stop responding without
saying so, proceed with what you have and list exactly what you processed.

For each document: resolve its target filename, convert it, then scrub it.

- **Filename** — if it maps to an artifact the table declares, use that artifact's
  `File under reference/` value verbatim. A derived name makes the next audit report the artifact as
  `MISSING`. Only if it maps to nothing expected, ask for a topic; if none is given, derive one from
  the content, state what you chose, and use kebab-case `.md`.
- **Out-of-scope document** — if it belongs to a domain this session is not auditing, say so
  explicitly, confirm with the owner what they want done, and do not upload it. Never file a
  document into a domain outside the confirmed scope.
- **Several documents for one artifact** — owners resend, revise and split documents in different
  ways. Resolve which case applies before converting, and never merge two documents into one file:
  - *Same artifact, later in this session* — the newer document replaces the earlier one unless the
    owner says otherwise. Discard the earlier draft whole, including any redaction confirmation
    still pending on it, and tell the owner which draft it replaced. Scrub and confirm the new one
    from scratch; nothing carries over.
  - *Identical to a document already processed* — say so and skip it.
  - *Clearly partial* — an addendum, a single section, "plus this" — ask whether it replaces the
    draft or is filed as its own topic under the unexpected-document rule above.
  - *Artifact already `done` from an earlier session* — ask whether it replaces the committed file
    before touching it.
  - *One document covering several artifacts* — ask which single artifact it is for, file it there,
    and grade the others on their own. Never split a document across files.
- **Convert** — invoke the `knowledge-source-converter` skill (UT-01) with the `skill` tool and
  follow its workflow. Locate the attachment's path on disk first; the converter takes a filesystem
  path. Never convert by hand or reimplement it inline. If the converter rejects the format, tell
  the owner that format is not supported, list the formats its error names, and ask for the document
  in one of them; if they cannot supply one, record the gap with the converter's error.
- **Scrub — blocking, no exceptions.** Drop conversion chrome the converter left: repeated PDF
  headers and footers, `CONFIDENTIAL` banners, `Page N`, PPTX `Slide N` labels, Excel metadata
  sheets. Replace every real secret, credential, token, connection string, internal hostname, IP
  address, and personal identifier with a placeholder — compliance documents, test environment
  descriptions, and dev configs are the likeliest carriers. Use `<UPPER_SNAKE_CASE>` placeholders
  that name what was removed. Record every redaction — file, line, category (`credential`,
  `connection string`, `hostname`, `IP address`, `personal identifier`) and placeholder — never the
  value. A credential that was real in the source is a **live secret**: tell the owner, recommend
  rotating it at source, and carry it into step 9 and the closing message. Show the owner every
  redaction and get explicit confirmation. If they ask for changes, apply exactly what they
  describe, show the full list again, and re-confirm. Change nothing else: no summarising,
  improving, or reorganising.

**Re-grade every artifact this step touched.** A converted document is not automatically
`DOCUMENTED` — apply the step 5 definitions again and it may still be `THIN`. Then apply the owner's
step 7 answers: each confirmed `NOT APPLICABLE`, with its reason. These revised grades are the final
ones, and they are what step 9 and step 10 use.

- **Takes:** the documents the owner attaches, in however many messages they arrive, and the artifact
  tables from step 5.
- **Never:** commit an unscrubbed file; transcribe a document whose conversion failed; edit or delete
  a `reference/` file the owner did not ask you to replace; let one failed conversion stop the others;
  move to step 9 while the owner is still sending files; assume a converted document is `DOCUMENTED`.
- **Done when:** the owner has said they have nothing further, every document they sent is either
  converted, scrubbed, and confirmed — or recorded as a gap with the converter's error — and every
  artifact has its final grade.
- **Revisit if:** another document arrives before step 9 opens the merge request — process it,
  re-grade, and include it. Anything arriving after that is a new session.

### 9. Write the changes
Three writes, then one merge request.

- **`SKILL.md`** — only in two cases: an unexpected document was added, so add a row to that skill's
  artifact table; or new reference content contradicts an instruction in the skill's `Workflow` or
  `Standards & references`, so correct it. Keep the section structure from
  `.agents/skills/AUTHORING_STANDARD.md`.
- **`onboarding-status.md`** — per in-scope domain, to the format in
  `.agents/skills/knowledge/README.md`. Map the **final** grade from step 8 directly: `DOCUMENTED` → `done`,
  `NOT APPLICABLE` → `n/a`, `THIN` and `MISSING` → `pending`. No judgement. Fill `Grade` with the
  final grade, `Note` with the `THIN` missing specific, the `MISSING` writing brief, the
  `NOT APPLICABLE` reason or the stale flag, and `Redactions` with every placeholder this session
  put into the artifact's file, marking live secrets. Never write a secret value. Rewrite the file
  whole, keeping rows this session did not work on with their cells unchanged. Create it if it does
  not exist.
  In `knowledge-development`'s file, also write the `## DeepWiki` section with the values step 3
  recorded, whenever step 3 regenerated, skipped or failed; keep it unchanged when the wiki was found
  current or step 3 did not run.
- **Merge request** — one, containing all of the above. Write the description with the
  `draft-merge-request-descriptions` skill.

Write the status files whenever this session changed any grade or the DeepWiki section — including
when the owner supplied no documents but confirmed an artifact as `NOT APPLICABLE`. That confirmation is a decision worth
keeping; dropping it means the next session asks again.

- **Never:** restructure a skill, change its `id`, or edit an out-of-scope skill; write an
  out-of-scope domain's status file; commit to the default branch; merge the MR yourself; map a
  step 5 grade that step 8 has since revised.
- **Done when:** one MR exists with every changed file — or nothing changed at all, in which case
  there is no MR and the report is the only deliverable.

### 10. Deliver
Post the closing message described under Output.

- **Done when:** the message states the role, scope, result, coverage before and after, every
  redaction and live secret, the remaining gaps by tier, and the MR link when there is one — and
  says plainly which gaps someone must still write up, and the DeepWiki result when step 3 ran.

## Standards & references
- Each in-scope `.agents/skills/knowledge/<skill>/SKILL.md` — the artifact table is the checklist.
- [`.agents/skills/knowledge/README.md`](../knowledge/README.md) — the `onboarding-status.md` format,
  including its DeepWiki section, shared with anything else that reads those files.
- `.devin/wiki.json` — steers which pages DeepWiki generates.
- `knowledge-source-converter` (UT-01) — document conversion.
- `draft-merge-request-descriptions` — the MR description.
- `.agents/skills/AUTHORING_STANDARD.md` — the structure any edited `SKILL.md` must keep.

## Output
**In the repository:** the updated `onboarding-status.md` for each in-scope domain, plus any
converted `reference/` files and `SKILL.md` edits, as one merge request.

**In the session,** a closing message in this order:

1. `Organization`, `Role`, `Audit scope`, `Result` — `PASS` when every applicable in-scope artifact
   is `DOCUMENTED` after this session, excluding `NOT APPLICABLE`; otherwise `NEEDS ATTENTION`.
2. Coverage per in-scope domain: `DOCUMENTED` over applicable artifacts, `NOT APPLICABLE` excluded
   from the denominator and stated separately. Before and after, where gaps were closed.
3. One row per in-scope artifact:
   `Skill | Artifact | Expected file | Critical | Status | Evidence | What's needed`.
   `What's needed` is empty for `DOCUMENTED`, the missing specific for `THIN`, a one-line writing
   brief for `MISSING`, and the reason for `NOT APPLICABLE`.
4. Files added or changed, each with the source document it came from.
5. Redactions per file: line, category and placeholder — never the value. Live secrets come first,
   under **Live secrets to rotate**, with the source document each appeared in.
6. Remaining gaps by tier, numbered by priority under each tier's test question.
7. DeepWiki, when step 3 ran: its result, the commit it was generated from and the wiki link.
8. The MR link, when there is one.

There is no report file. Out-of-scope domains appear nowhere in the output.

## Quality checklist
- [ ] One row per in-scope artifact, and no out-of-scope rows anywhere.
- [ ] Every row except `MISSING` names its file and section.
- [ ] Every `THIN` row names its missing specific.
- [ ] Every `NOT APPLICABLE` row carries its reason.
- [ ] Every `★` gap is tiered `BLOCKING`.
- [ ] Every committed file was scrubbed and the redactions confirmed.
- [ ] Every redaction is in the closing message and the status file, live secrets flagged, and no
      secret value written anywhere.
- [ ] Every document superseded this session left nothing behind — no draft, no pending confirmation.
- [ ] Every in-scope `onboarding-status.md` was rewritten, and none out of scope was touched.

## Anti-patterns
- Inventing, inferring, or transcribing content the owner did not supply. A gap with no document
  stays a gap.
- Filling a gap from a similar application, or presenting an inference as documented fact.
- Committing a secret, hostname, or personal identifier. Placeholders only, confirmed first.
- Auditing or editing a domain outside the confirmed role.
- Marking an artifact `DOCUMENTED` on the strength of a filename or an assurance it exists somewhere.
- Creating Devin Knowledge notes. Knowledge lives in the repository here.

## Handoff
→ The SDLC orchestrator reads every domain's `onboarding-status.md` to decide whether delivery work
   can begin. This skill covers one role; only the orchestrator sees the whole picture.
→ A second role's domains — a fresh session of this skill.
