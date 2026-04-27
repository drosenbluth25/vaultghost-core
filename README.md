# vaultghost-core

## Purpose

`vaultghost-core` is the reference Python implementation of VaultGhost's turn-record canonicalization, signing, and verification primitives. It defines the on-disk turn-record format, provides JCS (RFC 8785) canonicalization, and exposes Ed25519 key generation, signing, and verification utilities used by other VaultGhost components to produce and check tamper-evident records of model interactions.

## Status

Implemented

This status reflects that the repository contains a working Python package (`vaultghost_core/`), a JSON Schema for turn records, a CLI with `keygen`, `turn-sign`, and `turn-verify` subcommands, and a pytest test suite covering the signing and verification flow.

## What This Repository Contains

- `vaultghost_core/` — Python package with the implementation:
  - `canonical.py` — JCS (RFC 8785) canonicalization
  - `sign.py` — Ed25519 key generation, signing, and signature verification
  - `turn.py` — turn-record signing helpers
  - `verify.py` — record verification logic
  - `adapter.py` — event/record construction helpers (genesis hash, base event, signed record)
  - `cli.py` — command-line entry point (`keygen`, `turn-sign`, `turn-verify`)
- `schemas/VaultGhost.TurnRecord.v1.schema.json` — JSON Schema for the v1 turn record format
- `tests/test_signing.py` — pytest suite for the signing and verification flow
- `requirements.txt` — runtime and test dependencies (`rfc8785`, `jsonschema`, `pytest`, `cryptography`)

## Verification / Usage

Install dependencies and run the test suite:

```
pip install -r requirements.txt
pytest
```

Run the CLI directly:

```
python -m vaultghost_core.cli keygen --private-out sk.bin --public-out pk.bin
python -m vaultghost_core.cli turn-sign --key sk.bin --in-file turn.json --out signed.json
python -m vaultghost_core.cli turn-verify --in-file signed.json
```

## Relationship to VaultGhost

VaultGhost is composed of several coordinated repositories:

- **vaultghost-protocol** — protocol specification and normative definitions for turn records, canonicalization, and signing.
- **vaultghost-core** (this repository) — reference implementation of the protocol's record, signing, and verification primitives in Python.
- **vaultghost-verify** — verifier tooling that consumes records produced by `vaultghost-core` and checks them against the protocol's rules.
- **vaultghost-chain-ledger** — ledger component that links signed records into a chained, append-only history.

This repository provides the building blocks (canonicalization, key handling, signing, schema) that the verify and chain-ledger components depend on.

## Evidence Boundary

VaultGhost verifies records within a captured boundary. It can verify hashes, signatures, schemas, timestamps, declared metadata, and replayable artifacts. It does not claim visibility into hidden model weights, provider-side logs, undisclosed system prompts, or private infrastructure.

## License

License decision pending. No open-source license should be assumed until a LICENSE file is added.
