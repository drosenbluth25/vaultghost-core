"""
VaultGhost™ Protocol — tests/test_signing.py
Signing sprint test suite — v1.0.0-signing

7 original tests + test_unsigned_record_fails (8th test per Code Review Report, April 24, 2026)
Patent Reference: Provisional — Feb 25, 2026

Rules:
  - Do not modify the 7 existing tests.
  - Do not touch sign.py.
  - Release cannot be tagged until 8/8 pass.
"""
from __future__ import annotations

import copy
import json
from uuid import uuid4

import pytest

from vaultghost_core.sign import (
    generate_keypair,
    pubkey_to_base64,
    signature_to_base64,
    sign_data,
    verify_signature,
)
from vaultghost_core.canonical import canonicalize_jcs
from vaultghost_core.verify import verify_event
from vaultghost_core.adapter import build_base_event, build_signed_record, GENESIS_HASH

import base64
import hashlib
from datetime import datetime, timezone


# ── Helpers ────────────────────────────────────────────────────────────────────

def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def to_base64url(data: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def from_base64url(s: str) -> bytes:
    pad = 4 - (len(s) % 4)
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def key_pair():
    return generate_keypair()


@pytest.fixture(scope="module")
def other_key_pair():
    return generate_keypair()


def make_signed_frozen(key_pair, turn_id=None, tool_id="test-adapter/v1"):
    """Helper: produce a complete signed frozen event record."""
    private_key, public_key = key_pair
    tid = turn_id or str(uuid4())
    return build_signed_record(
        turn_id=tid,
        tool_id=tool_id,
        event_type="tool_call",
        input_data={"prompt": "test input"},
        output_data={"result": "test output"},
        private_key=private_key,
        public_key=public_key,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 — Happy path: valid signed record verifies as PASS
# ══════════════════════════════════════════════════════════════════════════════

def test_happy_path_pass(key_pair):
    """A correctly signed, unmodified record must return status=PASS."""
    frozen = make_signed_frozen(key_pair)
    result = verify_event(frozen)
    assert result["status"] == "PASS", f"Expected PASS, got: {result['status']}\n{result}"
    assert result["check_hash_integrity"]["passed"] is True
    assert result["check_signature_validity"]["passed"] is True


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 — Content mutation: tampered payload must return FAIL_CONTENT_MISMATCH
# ══════════════════════════════════════════════════════════════════════════════

def test_content_mutation_fails(key_pair):
    """
    Mutating any field in the payload after signing must cause FAIL_CONTENT_MISMATCH.
    FAIL_CONTENT_MISMATCH in test output is correct behavior — not a bug.
    """
    frozen = make_signed_frozen(key_pair)
    tampered = copy.deepcopy(frozen)
    tampered["payload"]["output"]["result"] = "tampered output"
    result = verify_event(tampered)
    assert result["status"] == "FAIL_CONTENT_MISMATCH", (
        f"Expected FAIL_CONTENT_MISMATCH, got: {result['status']}"
    )
    assert result["check_hash_integrity"]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 — Wrong public key: phase1 passes, phase2 fails → FAIL_SIGNATURE
# ══════════════════════════════════════════════════════════════════════════════

def test_wrong_public_key_fails(key_pair, other_key_pair):
    """
    Verifying with the wrong public key must fail phase2 only.
    test_wrong_public_key_fails correctly verifies phase1_integrity: True
    while phase2_authenticity: False — proving the two phases are independent.
    """
    frozen = make_signed_frozen(key_pair)
    tampered = copy.deepcopy(frozen)

    _, wrong_pub = other_key_pair
    wrong_pub_b64 = to_base64url(wrong_pub.public_bytes_raw())
    tampered["signer"]["public_key"] = wrong_pub_b64

    result = verify_event(tampered)
    assert result["status"] == "FAIL_SIGNATURE", (
        f"Expected FAIL_SIGNATURE, got: {result['status']}"
    )
    assert result["check_hash_integrity"]["passed"] is True
    assert result["check_signature_validity"]["passed"] is False


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4 — Unsupported schema version → FAIL_UNSUPPORTED_VERSION
# ══════════════════════════════════════════════════════════════════════════════

def test_unsupported_schema_version_fails(key_pair):
    """schema_version other than vaultghost-event/v1 must return FAIL_UNSUPPORTED_VERSION."""
    frozen = make_signed_frozen(key_pair)
    bad = copy.deepcopy(frozen)
    bad["schema_version"] = "vaultghost-event/v2"
    result = verify_event(bad)
    assert result["status"] == "FAIL_UNSUPPORTED_VERSION", (
        f"Expected FAIL_UNSUPPORTED_VERSION, got: {result['status']}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5 — Unexpected top-level key → INDETERMINATE (Fix 1)
# ══════════════════════════════════════════════════════════════════════════════

def test_unexpected_top_level_key_indeterminate(key_pair):
    """
    A top-level key not in EXPECTED_TOP_KEYS must return INDETERMINATE.
    Validates Fix 1: the key guard enforces schema boundary.
    """
    frozen = make_signed_frozen(key_pair)
    bad = copy.deepcopy(frozen)
    bad["injected_by_middleware"] = "unexpected"
    result = verify_event(bad)
    assert result["status"] == "INDETERMINATE", (
        f"Expected INDETERMINATE on unexpected key, got: {result['status']}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 6 — Missing signer fields → FAIL_SIGNER_METADATA
# ══════════════════════════════════════════════════════════════════════════════

def test_missing_signer_field_fails(key_pair):
    """SignerMetadata missing a required field must return FAIL_SIGNER_METADATA."""
    frozen = make_signed_frozen(key_pair)
    bad = copy.deepcopy(frozen)
    del bad["signer"]["public_key"]
    result = verify_event(bad)
    assert result["status"] == "FAIL_SIGNER_METADATA", (
        f"Expected FAIL_SIGNER_METADATA, got: {result['status']}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 7 — Legacy compatibility: turn_verify CLI path over new signed data
# ══════════════════════════════════════════════════════════════════════════════

def test_legacy_compatibility(key_pair, tmp_path):
    """
    test_legacy_compatibility exercises the existing turn-verify CLI path
    over new signed data. Writes a signed record to a temp file and reads
    it back without mutating the loaded dict (Fix 3 validated here).
    """
    frozen = make_signed_frozen(key_pair)
    turn_file = tmp_path / "turn.json"
    turn_file.write_text(json.dumps(frozen, ensure_ascii=False, indent=2), encoding="utf-8")

    # Simulate the CLI's file-load-then-verify flow without mutation
    loaded = json.loads(turn_file.read_text(encoding="utf-8"))
    sig_obj = loaded.get("signature")
    turn_for_verify = {k: v for k, v in loaded.items() if k != "signature"}
    _ = canonicalize_jcs(turn_for_verify)  # must not raise

    result = verify_event(loaded)
    assert result["status"] == "PASS", (
        f"Legacy CLI path expected PASS, got: {result['status']}\n{result}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 8 — Unsigned record → FAIL_SIGNER_METADATA (Fix 2, new test)
# ══════════════════════════════════════════════════════════════════════════════

def test_unsigned_record_fails():
    """
    An unsigned frozen record (signature=None, signer=None) must return
    FAIL_SIGNER_METADATA — not INDETERMINATE from a swallowed AttributeError.

    8th test added per Code Review Report April 24, 2026 (Fix 2).
    Validates that unsigned records produce explicit, semantically correct status.
    """
    from vaultghost_core.sign import generate_keypair
    from vaultghost_core.adapter import to_frozen_schema_unsigned

    internal_unsigned = {
        "turn_id": str(uuid4()),
        "schema_version": "vaultghost-event/v1",
        "event_type": "tool_call",
        "timestamp": "2026-04-24T12:00:00Z",
        "tool_id": "test-adapter/v1",
        "input": {"prompt": "unsigned test"},
        "output": {"result": "unsigned result"},
        "prev_turn_hash": GENESIS_HASH,
    }

    frozen = to_frozen_schema_unsigned(internal_unsigned)
    assert frozen["signature"] is None, "Expected signature=None for unsigned record"
    assert frozen["signer"] is None, "Expected signer=None for unsigned record"

    result = verify_event(frozen)
    assert result["status"] == "FAIL_SIGNER_METADATA", (
        f"Expected FAIL_SIGNER_METADATA for unsigned record, got: {result['status']}\n{result}"
    )
