# Coding Standards - Developer Tooling

Applies to all Rust crates owned by the Developer Experience team, including `fd-find`. Version 3.1, reviewed August 2026.

## Naming

- Modules, functions and variables: `snake_case`.
- Types, traits and enum variants: `PascalCase`.
- Constants and statics: `SCREAMING_SNAKE_CASE`.
- No abbreviations except `cfg`, `ctx` and `id`. A reviewer rejects `fltr`, `wlk` and similar.
- Boolean names read as a predicate: `is_hidden`, not `hidden_flag`.

## Module structure

- One concern per module. A module over 400 lines is split.
- Public surface is declared in the module header with `pub use`; nothing else is `pub`.
- Filters live under `filter/`, one file per filter dimension.

## Language version and edition

Rust edition 2024, minimum toolchain 1.90.0. Nightly features are prohibited in shipped code.

## Error handling

- `anyhow::Result` at the binary boundary, concrete error types inside library modules.
- `unwrap()` and `expect()` are permitted only in tests, or where a comment proves the invariant.
- Every error surfaced to the user names the path or pattern that caused it.
- Exit codes go through `ExitCode`; never call `process::exit` directly.

## Formatting and lint

- `cargo fmt` with the checked-in `rustfmt.toml`. No local overrides.
- `cargo clippy -- -D warnings` must pass. Suppressions require an inline reason.
- Both run in CI and block the merge. Do not hand-check what the linter enforces.

## Unit test standards

- Every public function has at least one test covering the happy path and one boundary.
- Tests live in a `mod tests` block beside the code under test.
- Test names read `given_<condition>_<expected>`.
- No test touches the real filesystem outside a `tempfile` directory.
- Line coverage on `filter/` and `walk.rs` must not fall below 80 percent.

## Logging

No logging framework in the binary. Diagnostics go to stderr behind `--verbose`. Never print a matched path to stderr; stdout is the only result channel.

## Merge request rules

- Under 400 changed lines. Larger changes are split, or the author justifies the size in the description.
- Two approvals, one of which is from a code owner.
- Green pipeline before review is requested, not during.
- The description states what changed, why, and how it was tested.
- No drive-by refactors mixed into a behavioural change.
