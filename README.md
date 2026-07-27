# VaultGhost Core

## Status

**Candidate core implementation; not independently validated and not production-ready.**

This repository contains implementation work associated with VaultGhost canonicalization, schema validation, Ed25519 signing/verification, deterministic fixtures, and evidence-control artifacts. It is a candidate implementation component of the wider VaultGhost repository ecosystem. The repository does not by itself establish legal ownership, factual truth, external adoption, patentability, or end-to-end interoperability with every related repository.

## Scope

VaultGhost Core is intended to support bounded technical operations such as:

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
- `drosenbluth25/vaultghost-verify`: minimal deterministic run-manifest verification utility.
- `drosenbluth25/vaultghost-chain-ledger`: artifact and hash-index consistency component.

No cross-repository release should be treated as authoritative until exact commit SHAs are pinned in a reviewed release manifest.

## Requirements

Observed dependency requirements include:

```text
rfc8785==0.1.4
jsonschema>=4.20
pytest>=8.0
cryptography>=42.0.0
```

## Installation

From a fresh clone, create an isolated Python environment and install the pinned or declared dependencies used by the checked-out commit. The exact package installation command still requires maintainer confirmation because this repository does not yet expose a single reviewed installation contract.

Example development setup:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Verification and Tests

Commit history records targeted signing tests and broader evidence-capture workflows. One historically recorded command is:

```bash
pytest -v tests/test_signing.py
```

Do not interpret this README as proof that the command currently passes on every supported environment. Before release designation, a reviewer must record:

- checked-out commit SHA;
- operating system and Python version;
- dependency resolution output;
- exact commands;
- stdout, stderr, and exit codes;
- test and fixture hashes.

## Security Boundary

The implementation may validate structural, cryptographic, and deterministic conditions defined by its schemas and code. It does not independently establish:

- truth of signed statements;
- authority of a signer beyond configured trust material;
- originality of an artifact;
- legal sufficiency;
- independent timestamp custody;
- absence of malicious maintainers.

## Current Gate 0 Blockers

1. Confirm the authoritative installation and full-suite test commands.
2. Inventory normative schemas, fixtures, and CLI entry points.
3. Map implementation behavior to the canonical specification candidate.
4. Pin this repository commit in a cross-repository release manifest.
5. Complete a fresh-clone reproduction by an independent human reviewer.
6. Resolve critical findings before a production-readiness claim.

## Reporting Findings

Report reproducible defects with the commit SHA, environment, command log, actual output, expected invariant, and a minimal fixture. Model-generated findings remain proposals until reproduced by a human or deterministic test.
