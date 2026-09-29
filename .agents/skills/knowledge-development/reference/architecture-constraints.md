# Architecture Constraints

## Forbidden dependencies
- `filter/` must not depend on `output/`. Filters decide inclusion only; they never format.
- `cli.rs` must not call into `walk.rs`. Parsing produces a `Config` and nothing else.
- No module may read environment variables outside `cli.rs` and `main.rs`.

## Intentional boundaries
The traversal layer owns all concurrency. Worker threads communicate only through the
`crossbeam-channel` bounded channel into `ReceiverBuffer`. Nothing else may spawn threads,
because output ordering depends on that single funnel.

## Deprecated
- The pre-2024 ignore syntax is deprecated. Do not extend it.
- `lscolors` direct calls outside `output.rs` are deprecated; route through the formatter.

## Approved versions
- Rust edition 2024, minimum toolchain 1.90.0
- `regex` 1.12.x, `ignore` 0.4.x, `clap` 4.6.x
- New crates require Developer Experience sign-off

## Target state
The exec layer will move behind a trait so alternative runners can be added in FY27 Q3.
Do not add new direct callers of `exec/mod.rs` in the meantime.
