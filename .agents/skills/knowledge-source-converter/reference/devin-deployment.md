# Deploying the converter in a Devin environment

A playbook cannot carry a script — Devin playbooks are text. The scripts reach a session
because this repository is cloned into Devin's environment snapshot, so the paths in
`SKILL.md` resolve inside the session's workspace.

Two things must be true for that to hold.

## 1. This repository is a configured repository in the blueprint

Devin's environment is built from a **blueprint** (Settings → Environment → Blueprints) into
a **snapshot**, and every session boots a fresh copy of that snapshot with the configured
repositories already cloned. If the repository is not configured there, the skill's paths do
not exist in the session.

## 2. The venv is built at build time, not at session time

Session changes never persist back to the snapshot, so a venv created during a session is
rebuilt and discarded every time. Put the bootstrap in the blueprint's `maintenance` section,
which runs during builds and is surfaced to the agent at session start as context it can
re-run when dependencies change.

```yaml
maintenance: |
  python3 skills/knowledge-source-converter/scripts/setup.py

knowledge:
  - name: knowledge-source-converter
    contents: |
      Convert a source document to markdown:
      skills/knowledge-source-converter/.venv/bin/python \
        skills/knowledge-source-converter/scripts/convert.py <source> --out <target>
```

`initialize` is for runtimes and system packages; `maintenance` is where `pip install` and
equivalents belong. `knowledge` entries are never executed — they are loaded into the agent's
context at session start, which is why the convert command is worth putting there.

## Why build time matters here

`requirements.txt` pins `pypandoc_binary`, which bundles the pandoc binary and is therefore a
large wheel. If egress to PyPI is restricted or proxied, installing it at build time fails
loudly and visibly during the build instead of halfway through a user's onboarding session.

## Handling an attached document

When a user attaches a source document to a Devin session, locate the attachment path in the
session workspace before converting. The converter takes a filesystem path; it has no
knowledge of session attachments.
