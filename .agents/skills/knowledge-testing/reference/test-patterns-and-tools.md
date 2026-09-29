# Test Patterns and Tools

## Frameworks
- Unit tests: the built-in Rust test harness, `cargo test`
- Integration tests: `tests/` directory driving the compiled binary
- Snapshot assertions: `insta`
- Temporary trees: `tempfile`

## Layout and naming
- Unit tests live in a `mod tests` block beside the code under test
- Integration tests are one file per surface, named `test_<surface>.rs`
- Test names read `given_<condition>_<expected>`

## Fixtures
Directory trees are built by a helper in `tests/testenv/mod.rs`. Never rely on a
pre-existing tree on disk, and never write outside the temporary directory.

## CI stages
`cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`, then the perf job on
release branches only.

## Reporting
Coverage is produced by `cargo llvm-cov` and published as a CI artifact.
