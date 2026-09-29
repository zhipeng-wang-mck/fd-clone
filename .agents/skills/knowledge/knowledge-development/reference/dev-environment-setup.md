# Development Environment Setup

## Prerequisites

- Rust 1.90.0 or later, installed through rustup
- A C toolchain for jemalloc on Linux: `build-essential` on Debian and Ubuntu, `gcc` and `make` on RHEL
- Git 2.40 or later
- VPN connection to the corporate network before fetching crates

## Access required

Request the **DEVEX-BUILD** role in the access portal at Requests, then New request, then Engineering roles. Your line manager approves it; approval normally lands within one business day. Without the role the crate mirror returns 401 on every fetch.

## Obtaining your crate mirror token

Each developer uses their own token. The shared token is being withdrawn.

1.  Sign in to the mirror at `https://<CRATE_MIRROR_HOST>` with your corporate account.
2.  Open Account, then API tokens, then Generate token. Scope it to `read`.
3.  Copy the token immediately; it is shown once. Tokens expire after 90 days and are regenerated the same way.
4.  If Generate token is greyed out, the DEVEX-BUILD role has not propagated yet. Wait an hour, then raise a ticket to the Developer Experience queue.

## Configuring the token

Write it to `~/.cargo/credentials.toml`, which must be mode 600:

    [registries.corp-mirror]
    token = "<your token>"

On Windows the file is at `%USERPROFILE%\.cargo\credentials.toml`.

For CI, or if you would rather not write it to disk, set the environment variable instead. It takes precedence over the file:

    export CARGO_REGISTRIES_CORP_MIRROR_TOKEN="<your token>"

Never commit either the file or the variable. `.cargo/credentials.toml` is in the global gitignore; confirm with `git check-ignore -v ~/.cargo/credentials.toml`.

A shared fallback token still exists for the build agents and is scheduled for removal in FY27 Q2: `<CRATE_MIRROR_SHARED_TOKEN>`. Do not use it for local development.

## Pointing cargo at the mirror

Add to `.cargo/config.toml` in the repository root:

    [source.crates-io]
    replace-with = "corp-mirror"

    [source.corp-mirror]
    registry = "https://<CRATE_MIRROR_HOST>/index"

    [registries.corp-mirror]
    index = "https://<CRATE_MIRROR_HOST>/index"

## Build and run

    rustup toolchain install 1.90.0
    rustup override set 1.90.0
    cargo build --release
    ./target/release/fd pattern

## Verifying the setup

`cargo fetch` completes without prompting. If it succeeds, both the role and the token are correct. `cargo build --release` then finishes in roughly four minutes cold, under 30 seconds warm.

## Common issues

- **401 on fetch** — the token is missing, expired, or scoped wrong. Regenerate it.
- **TLS handshake failure** — the VPN has dropped. Reconnect and retry.
- `jemalloc` **build failure on macOS** — build with `--no-default-features`.
- `credentials.toml` **ignored** — file permissions are wider than 600, so cargo refuses to read it. Run `chmod 600 ~/.cargo/credentials.toml`.
- **Slow first build** — expected. The mirror caches after the first fetch.
