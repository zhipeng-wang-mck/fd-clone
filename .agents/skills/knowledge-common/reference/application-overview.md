# fd - Application Overview

## Purpose

`fd` is a command-line file search tool written in Rust, offered as a faster and more approachable alternative to the Unix `find` command. It is distributed as the `fd-find` crate and installs a single binary named `fd`.

## Users

Developers and platform engineers searching source trees interactively, and automation that needs fast filename lookup inside CI pipelines.

## Business capability

Developer productivity tooling. Not customer facing and holds no customer data.

## High-level components

| Component | Responsibility                                    |
|-----------|---------------------------------------------------|
| main.rs   | Entry point and orchestration                     |
| cli.rs    | Command-line parsing into an Opts struct          |
| walk.rs   | Parallel directory traversal, worker coordination |
| filter/   | Pattern, type, size, time and owner filters       |
| output.rs | Result formatting and colourisation               |
| exec/     | Command execution per result or batched           |

## Ownership

Maintained by the Developer Experience team. Technical owner: <TECHNICAL_OWNER_NAME>. Product owner: <PRODUCT_OWNER_NAME>. Escalation through the \#devex-tooling channel.

## Target service levels

Interactive search over a 250k-file tree completes in under 400 ms on a developer laptop. No availability target applies; the tool runs locally.
