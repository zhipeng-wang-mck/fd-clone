---
name: knowledge-source-converter
description: >
  Use this skill whenever a source document must become Markdown before an agent can read,
  grade, or commit it — a team's architecture Word file, a compliance PDF, a test-policy
  spreadsheet, a roadmap deck. Trigger it on any `.docx`, `.pdf`, `.xlsx`, `.pptx`
  or other supported file the user provides, and whenever a workflow needs a Markdown draft
  of something that is not Markdown yet. It runs a bundled, offline converter — pandoc for
  most formats, PyMuPDF for PDF, openpyxl for Excel — and returns a Markdown draft with
  obvious conversion chrome stripped. Do NOT use it to interpret, summarise, restructure or redact
  the content, and do NOT use it to decide where the output belongs; it converts only, and
  the calling skill or playbook owns naming, scrubbing and committing the result.
id: UT-01
phase: Utility
version: 1.0.0
tags: [utility, conversion, markdown, docx, pdf, xlsx, onboarding]
harnesses: [claude, devin, gitlab-duo, codex, cursor]
inputs: [a source document in a supported format, the desired output path]
outputs: [a Markdown draft at the requested path, plus converter notes on what was dropped]
enterprise_tools: []
---

# Knowledge Source Converter

## When to use
Trigger this whenever a workflow has a document in a non-Markdown format and needs its text
as Markdown. The common case is knowledge onboarding: a team hands over a Word architecture
document or a PDF compliance standard, and it has to land under a knowledge skill's
`reference/` folder as Markdown before anything can read or grade it.

Boundary: this skill converts, nothing more. It does not choose the output filename, decide
which artifact the document satisfies, redact secrets, or commit anything — the calling
playbook owns all of that. It also does not improve the content: the output is the author's
words with conversion artifacts removed, not a summary or a rewrite.

Run the scripts in this skill. Do not rewrite them, do not reimplement the conversion
inline, and do not use `.devin/knowledge_toolkit`.

## Inputs
- The **source document**, in one of the supported formats below.
- The **output path** the caller wants. If none is given, write `<source-stem>.md` beside the
  source.

| Format | Handled by |
|---|---|
| `.md`, `.markdown` | passthrough, no conversion |
| `.docx`, `.pptx`, `.odt`, `.rtf`, `.epub` | pandoc |
| `.rst`, `.org`, `.tex` | pandoc |
| `.adoc`, `.asciidoc`, `.ipynb`, `.csv`, `.tsv` | pandoc |
| `.jira`, `.textile`, `.mediawiki`, `.typ`, `.txt` | pandoc |
| `.pdf` | PyMuPDF (`scripts/pdf.py`) |
| `.xlsx`, `.xlsm` | openpyxl (`scripts/xlsx.py`) |

Nothing needs to be installed system-wide: `requirements.txt` pins `pypandoc_binary`, which
bundles the pandoc binary, alongside `pymupdf` and `openpyxl`.

## Workflow
1. **Confirm the format is supported.** Check the source's extension against the table above.
   If it is not listed, stop and tell the caller which formats are supported rather than
   transcribing the document by hand.
2. **Ensure the environment is ready.** The venv belongs in the environment build, not in
   every session — see `reference/devin-deployment.md`. Check whether
   `.agents/skills/knowledge-source-converter/.venv` exists and only bootstrap it if it is missing:
   `python .agents/skills/knowledge-source-converter/scripts/setup.py`
3. **Convert to the requested path.** Run from the repo root:
   - Linux/macOS: `.agents/skills/knowledge-source-converter/.venv/bin/python .agents/skills/knowledge-source-converter/scripts/convert.py <source> --out <target>`
   - Windows: `.agents\skills\knowledge-source-converter\.venv\Scripts\python.exe .agents\skills\knowledge-source-converter\scripts\convert.py <source> --out <target>`

   Use `--stdout` instead of `--out` when the caller wants the text without writing a file.
4. **Report what the converter dropped, and assume chrome remains.** The script prints the
   output path on stdout and its notes on stderr. Pass those notes back to the caller — they
   say what is no longer in the output. Excel conversion skips Metadata Field/Value sheets.
   PDF chrome removal is best-effort and narrower than it looks: a line is dropped only when
   it is byte-identical on **every** page, or is exactly `CONFIDENTIAL` or `Page N` on its own
   line. Single-page PDFs get no repetition detection at all, and a real-world footer such as
   `Acme Corp | Confidential | Page 1 of 3` survives because the page number makes each
   occurrence unique. Always expect the caller to still have chrome to strip. A PDF's title
   survives as a `# ` heading only when the source carries one — a running header that opens
   page 1, otherwise the PDF metadata title; with neither, no title is written.
5. **Hand the draft back without editing it.** Return the path and let the calling workflow
   decide on naming, remaining chrome, redaction and committing.
6. **On failure, report and stop.** Show the converter's error and the supported-format list.
   A failed conversion is a gap for the caller to handle, not something to work around by
   retyping the document.

## Standards & references
- `scripts/convert.py` — entry point; `--out` writes a file, `--stdout` prints.
- `scripts/setup.py` — builds the venv from `requirements.txt`; resolves paths relative to
  itself, so the skill folder works from any location.
- `scripts/pdf.py`, `scripts/xlsx.py` — the custom extractors pandoc cannot cover.
- `reference/devin-deployment.md` — how the converter is provisioned in a Devin environment.
- The caller's own rules on secrets and placeholders always apply to the output; this skill
  does not enforce them.

## Output
A Markdown draft at the requested path, holding the source document's text with obvious
conversion chrome removed, plus the converter's notes on what was dropped. The content is
unedited otherwise, and residual chrome is expected — removing it is the caller's job.

## Quality checklist
- [ ] Source format confirmed supported before running anything.
- [ ] Converter executed; content not transcribed, summarised, or retyped by hand.
- [ ] Output written to the path the caller asked for.
- [ ] Converter notes reported, so the caller knows what was dropped.
- [ ] Failures surfaced with the supported-format list, not worked around.
- [ ] Content returned unedited — no summarising, reordering, or "improving".

## Anti-patterns
- Reading the document and writing your own Markdown version of it instead of converting.
- Editing, summarising or reorganising the converted text inside this skill.
- Choosing the output filename or destination folder on the caller's behalf.
- Treating the output as safe to commit — it may still carry secrets, hostnames or PII that
  the caller must scrub.
- Rewriting or patching the scripts instead of reporting a conversion failure.
- Bootstrapping the venv every run when the environment already provides it.

## Handoff
→ **`!onboarding` playbook** — names the target artifact, scrubs the draft, and delivers the
   merge request.
→ **KN-01 / KN-02 / KN-03 / KN-04 knowledge skills** — own the `reference/` folders the
   converted artifacts land in.
