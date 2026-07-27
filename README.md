# VaultGhost Core

## Status

**Candidate core implementation with a passing GitHub-hosted CI baseline; not independently human-validated and not production-ready.**

This repository contains implementation work associated with VaultGhost canonicalization, schema validation, Ed25519 signing/verification, deterministic fixtures, and evidence-control artifacts. It is a candidate implementation component of the wider VaultGhost repository ecosystem. The repository does not by itself establish legal ownership, factual truth, external adoption, patentability, or end-to-end interoperability with every related repository.

## Scope

VaultGhost Core supports bounded technical operations such as:

- canonical serialization of defined payloads;
- schema validation;
- creation and verification of Ed25519 signatures over defined signable content;
- deterministic fixture verification;
- explicit failure codes and evidence-state records.

## Non-goals

This repository does **not** claim to:

- prove that a claim is factually true;
- prove legal authorship or ownership;
- infer hidden influence between proprietary LLM internals;
- provide a novel cryptographic primitive;
- establish production readiness or third-party validation.

A valid signature proves only that the signed bytes verify under the supplied key and algorithm. A successful replay proves only that the defined computation reproduced under the tested conditions.

## Relationship to Other Repositories

- `drosenbluth25/vaultghost-protocol`: claimed canonical specification candidate; specification-to-code correspondence remains under Gate 0 review.
- `drosenbluth25/vaultghost-verify`: minimal deterministic run-manifest verification utility; its corrected baseline has passed GitHub-hosted CI.
- `drosenbluth25/vaultghost-chain-ledger`: artifact and hash-index consistency component.

No cross-repository release should be treated as authoritative until exact commit SHAs are pinned in a reviewed release manifest and interface correspondence is demonstrated.

## Requirements

```text
rfc8785==0.1.4
jsonschema>=4.20
pytest>=8.0
cryptography>=42.0.0
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Verification and Tests

Run the complete included suite:

```bash
python -m pytest -q
```

Exercise the CLI:

```bash
python -m vaultghost_core.cli --help
python -m vaultghost_core.cli keygen --private-out sk.bin --public-out pk.bin
```

A GitHub-hosted Ubuntu baseline completed successfully on July 27, 2026:

- dependency installation: PASS;
- full suite: `8 passed in 0.14s`;
- CLI help: PASS;
- Ed25519 key generation smoke test: PASS;
- workflow run: `30283272571`;
- evidence artifact: `8659705260`;
- artifact digest: `sha256:11891fc5452d368e72019dda69474dd45d3b9d0f983e45fc0ce680ae1df36877`.

See `gate-0/CORE_BASELINE_RESULT_CI.json` for the bounded evidence record.

## Security Boundary

The implementation may validate structural, cryptographic, and deterministic conditions defined by its schemas and code. It does not independently establish:

- truth of signed statements;
- authority of a signer beyond configured trust material;
- originality of an artifact;
- legal sufficiency;
- independent timestamp custody;
- absence of malicious maintainers.

## Current Gate 0 Blockers

1. Map implementation behavior to the canonical specification candidate.
2. Demonstrate interface and fixture correspondence with `vaultghost-verify` and `vaultghost-chain-ledger`.
3. Pin a tested cross-repository commit set in a release manifest.
4. Complete an independent human reproduction for Gate 3.
5. Resolve critical findings before a production-readiness claim.

## Reporting Findings

Report reproducible defects with the commit SHA, environment, command log, actual output, expected invariant, and a minimal fixture. Model-generated findings remain proposals until reproduced by a human or deterministic test.
