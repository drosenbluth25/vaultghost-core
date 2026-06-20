# Contributing

Thank you for your interest in `vaultghost-core`. This repository is part of the VaultGhost project and is maintained under a deliberate review process.

## Before You Contribute

- The project does not yet have an open-source license. Until a `LICENSE` file is added, no open-source license should be assumed. By opening an issue or a pull request, you acknowledge that licensing terms are pending and may affect how contributions can be incorporated.
- Substantive changes (new features, protocol changes, schema changes, cryptographic changes) should be discussed in an issue before a pull request is opened.

## How to Contribute

1. Open an issue describing the bug, feature, or change you would like to make. Include enough context for a maintainer to understand the motivation and scope.
2. For small, well-scoped fixes (typos, documentation, obvious bugs), a pull request without a prior issue is acceptable.
3. Fork the repository and create a topic branch from `main`.
4. Make your changes in focused commits with clear commit messages.
5. Ensure the test suite passes locally:
   ```
   pip install -r requirements.txt
   pytest
   ```
6. Open a pull request against `main`. Describe what changed and why, and reference any related issue.

## Pull Request Expectations

- Keep pull requests focused. Unrelated changes should be split into separate PRs.
- Do not modify the protocol-level signing, canonicalization, or schema behavior without an accompanying issue and explicit maintainer agreement.
- Do not add a `LICENSE` file or modify license-related text in a pull request — licensing decisions are made by the repository owner.
- All pull requests are reviewed by the code owner (see `.github/CODEOWNERS`).

## Code of Conduct

Be respectful and constructive. Reports of unacceptable behavior may be sent to the repository owner via their GitHub profile.

## Security Issues

Do not file security-sensitive issues as public pull requests or issues. See `SECURITY.md` for the reporting process.
