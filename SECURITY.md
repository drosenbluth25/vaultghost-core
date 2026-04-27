# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in `vaultghost-core` or any other VaultGhost repository, please report it privately. Do not open a public GitHub issue for security-sensitive reports.

To report a vulnerability:

- Open a private security advisory on this repository via GitHub's "Report a vulnerability" workflow under the **Security** tab, **or**
- Contact the repository owner directly through the contact information on their GitHub profile (`@drosenbluth25`).

Please include:

- A description of the issue and its impact.
- Steps to reproduce, or a proof-of-concept, where possible.
- The affected versions, commits, or files.
- Any relevant logs, traces, or sample inputs (with sensitive data redacted).

## Disclosure

The maintainer will acknowledge receipt of valid reports and coordinate a fix and disclosure timeline with the reporter. Please do not publicly disclose the vulnerability until a fix has been released or a disclosure timeline has been agreed upon.

## Scope

This policy covers code and documentation in this repository. Issues in upstream dependencies should be reported to those projects directly; reports here that concern dependencies will be triaged and forwarded as appropriate.

## Evidence Boundary

VaultGhost verifies records within a captured boundary. It can verify hashes, signatures, schemas, timestamps, declared metadata, and replayable artifacts. It does not claim visibility into hidden model weights, provider-side logs, undisclosed system prompts, or private infrastructure. Security reports should reflect this boundary.
