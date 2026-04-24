"""
VaultGhost™ Protocol — verify.py
Two-phase event verifier: hash integrity (Phase 1) + signature authenticity (Phase 2).

Fixed per Code Review Report dated April 24, 2026:
  Fix 1 — Top-level key guard (INDETERMINATE on schema drift)
  Fix 2 — Explicit null check for signature/signer (FAIL_SIGNER_METADATA on unsigned records)
Patent Reference: Provisional — Feb 25, 2026
"""
from __future__ import annotations

import base64
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict

from .canonical import canonicalize_jcs
from .sign import verify_signature, Ed25519PublicKey

SCHEMA_VERSION = "vaultghost-event/v1"

EXPECTED_TOP_KEYS = {
    "schema_version",
    "event_id",
    "payload",
    "computed_hash",
    "signature",
    "signer",
    "_verification",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _from_base64url(s: str) -> bytes:
    pad = 4 - (len(s) % 4)
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


def verify_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify a frozen VaultGhost event record.

    Returns a VerificationResult dict with keys:
        status, verified_at, turn_id, signed_hash,
        check_hash_integrity, check_signature_validity, failure_reason
    """
    result: Dict[str, Any] = {
        "status": "INDETERMINATE",
        "verified_at": _utc_now(),
        "turn_id": None,
        "signed_hash": None,
        "check_hash_integrity": {
            "passed": False,
            "recomputed_hash": None,
            "stored_hash": None,
            "failure_detail": None,
        },
        "check_signature_validity": {
            "passed": False,
            "signer_id": None,
            "key_version": None,
            "failure_detail": None,
        },
        "failure_reason": None,
        "verifier_version": "vaultghost-verifier/v1",
    }

    try:
        # ── Schema version gate ────────────────────────────────────────────────
        schema_ver = event.get("schema_version")
        if schema_ver != SCHEMA_VERSION:
            result["status"] = "FAIL_UNSUPPORTED_VERSION"
            result["failure_reason"] = f"Unsupported schema_version: {schema_ver!r}"
            return result

        # ── FIX 1: Top-level key guard ─────────────────────────────────────────
        # Any unexpected top-level key signals schema drift → INDETERMINATE.
        unexpected = set(event.keys()) - EXPECTED_TOP_KEYS
        if unexpected:
            result["status"] = "INDETERMINATE"
            result["failure_reason"] = f"Unexpected top-level keys: {sorted(unexpected)}"
            return result

        # ── FIX 2: Explicit null check for signature / signer ──────────────────
        # Unsigned records emit "signature": None and "signer": None.
        # Return FAIL_SIGNER_METADATA explicitly — not INDETERMINATE from AttributeError.
        if event.get("signature") is None or event.get("signer") is None:
            result["status"] = "FAIL_SIGNER_METADATA"
            result["failure_reason"] = "signature or signer is null — unsigned record"
            return result

        # ── Phase 1: Hash integrity ────────────────────────────────────────────
        payload = event.get("payload", {})
        stored_hash = event.get("computed_hash")
        result["signed_hash"] = stored_hash
        result["turn_id"] = payload.get("turn_id") or event.get("event_id")

        payload_for_hash = {k: v for k, v in payload.items() if k != "computed_hash"}
        recomputed = _sha256_hex(canonicalize_jcs(payload_for_hash))

        result["check_hash_integrity"]["recomputed_hash"] = recomputed
        result["check_hash_integrity"]["stored_hash"] = stored_hash

        if recomputed != stored_hash:
            result["status"] = "FAIL_CONTENT_MISMATCH"
            result["check_hash_integrity"]["passed"] = False
            result["check_hash_integrity"]["failure_detail"] = (
                f"recomputed={recomputed} stored={stored_hash}"
            )
            result["failure_reason"] = "Hash mismatch — content was tampered"
            return result

        result["check_hash_integrity"]["passed"] = True

        # ── Phase 2: Signature authenticity ────────────────────────────────────
        sig_block = event["signature"]
        signer_meta = event["signer"]

        signer_id = signer_meta.get("signer_id")
        key_version = signer_meta.get("key_version")
        result["check_signature_validity"]["signer_id"] = signer_id
        result["check_signature_validity"]["key_version"] = key_version

        required_signer_fields = {
            "signer_id", "public_key", "public_key_encoding", "key_version", "key_created_at"
        }
        missing = required_signer_fields - set(signer_meta.keys())
        if missing:
            result["status"] = "FAIL_SIGNER_METADATA"
            result["check_signature_validity"]["failure_detail"] = (
                f"Missing signer fields: {sorted(missing)}"
            )
            result["failure_reason"] = "Incomplete signer metadata"
            return result

        if signer_meta.get("public_key_encoding") != "base64url":
            result["status"] = "FAIL_SIGNER_METADATA"
            result["check_signature_validity"]["failure_detail"] = (
                f"Unsupported key encoding: {signer_meta.get('public_key_encoding')!r}"
            )
            result["failure_reason"] = "Unsupported public_key_encoding"
            return result

        # Verify Ed25519 signature against canonical payload bytes
        canonical_bytes = canonicalize_jcs(payload)
        pub_bytes = _from_base64url(signer_meta["public_key"])
        sig_bytes = _from_base64url(sig_block.get("signature", ""))
        pub_key = Ed25519PublicKey.from_public_bytes(pub_bytes)
        sig_valid = verify_signature(pub_key, sig_bytes, canonical_bytes)

        if not sig_valid:
            result["status"] = "FAIL_SIGNATURE"
            result["check_signature_validity"]["passed"] = False
            result["check_signature_validity"]["failure_detail"] = (
                "Ed25519 signature verification failed"
            )
            result["failure_reason"] = "Signature invalid"
            return result

        result["check_signature_validity"]["passed"] = True
        result["status"] = "PASS"
        result["failure_reason"] = None
        return result

    except Exception as exc:
        result["status"] = "INDETERMINATE"
        result["failure_reason"] = f"Verifier exception: {exc}"
        return result
