# ACME CORP - ENGINEERING TOOLING STANDARD

1. Scope
This standard applies to all tooling distributed to engineering
workstations, including the fd search utility.
Tools that read source code must not transmit file contents or
file paths off the workstation.

2. Data handling
No telemetry may be collected without explicit opt-in.
Crash reports are routed to <CRASH_INTAKE_HOST> and must
be scrubbed of absolute paths before submission.
The intake endpoint authenticates with a shared key:
INTAKE_KEY=<CRASH_INTAKE_API_KEY>
Contact <KEY_ROTATION_CONTACT_EMAIL> to rotate it.

3. Dependency review
Third-party crates must be reviewed before adoption. Crates with
known critical advisories are prohibited.
The approved mirror is <APPROVED_CRATE_MIRROR_IP> and must be used for all builds.
Licence allow-list: MIT, Apache-2.0, BSD-3-Clause.