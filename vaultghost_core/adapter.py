"""
VaultGhost™ Protocol — adapter.py
Translation layer: internal turn records → frozen signed event schema.

Approved as correct per Code Review Report dated April 24, 2026.
to_frozen_schema() re-derives computed_hash from canonical bytes at translation
time — never trusts the internal signed_digest field.
Patent Reference: Provisional — Feb 25, 2026
"""
from __future__ import annotations

import base64
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .canonical import canonicalize_jcs
from .sign import (
    generate_keypair,
    sign_data,
    pubkey_to_base64,
    signature_to_base64,
)

GENESIS_HASH = "sha256:" + "0" * 64


def _sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _to_base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def build_base_event(
    turn_id: str,
    tool_id: str,
    event_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    prev_turn_hash: str = GENESIS_HASH,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Construct a fully canonicalized BaseEventEnvelope.
    Computes computed_hash over all fields except itself.
    """
    ts = timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    partial = {
        "schema_version": "vaultghost-event/v1",
        "turn_id": turn_id,
        "event_type": event_type,
        "timestamp": ts,
        "tool_id": tool_id,
        "input": input_data,
        "output": output_data,
        "prev_turn_hash": prev_turn_hash,
    }
    canonical_bytes = canonicalize_jcs(partial)
    partial["computed_hash"] = _sha256_hex(canonical_bytes)
    return partial


def build_signed_record(
    turn_id: str,
    tool_id: str,
    event_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    private_key,
    public_key,
    signer_id: str = "vaultghost-adapter/v1",
    key_version: str = "v1",
    prev_turn_hash: str = GENESIS_HASH,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full adapter flow:
      1. Build BaseEventEnvelope
      2. Canonicalize and sign
      3. Attach SignatureBlock + SignerMetadata
      4. Return frozen schema record
    """
    envelope = build_base_event(
        turn_id=turn_id,
        tool_id=tool_id,
        event_type=event_type,
        input_data=input_data,
        output_data=output_data,
        prev_turn_hash=prev_turn_hash,
        timestamp=timestamp,
    )

    canonical_bytes = canonicalize_jcs(envelope)
    sig_bytes = sign_data(private_key, canonical_bytes)
    signed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pub_bytes = public_key.public_bytes_raw()

    signature_block: Dict[str, Any] = {
        "algorithm": "ed25519",
        "signature": _to_base64url(sig_bytes),
        "signed_hash": envelope["computed_hash"],
        "signed_at": signed_at,
        "signer_version": "vaultghost-signing/v1",
    }

    signer_metadata: Dict[str, Any] = {
        "signer_id": signer_id,
        "public_key": _to_base64url(pub_bytes),
        "public_key_encoding": "base64url",
        "key_version": key_version,
        "key_created_at": signed_at,
        "key_expires_at": None,
        "hsm_backed": False,
    }

    return {
        "schema_version": envelope["schema_version"],
        "event_id": envelope["turn_id"],
        "payload": envelope,
        "computed_hash": envelope["computed_hash"],
        "signature": signature_block,
        "signer": signer_metadata,
        "_verification": None,
    }


def to_frozen_schema_unsigned(internal_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate an unsigned internal record to frozen schema.
    Sets signature=None and signer=None.
    Used by test_unsigned_record_fails to validate Fix 2.
    Re-derives computed_hash from canonical bytes — never trusts signed_digest.
    """
    payload = {
        "schema_version": internal_record.get("schema_version", "vaultghost-event/v1"),
        "turn_id": internal_record["turn_id"],
        "event_type": internal_record.get("event_type", "tool_call"),
        "timestamp": internal_record["timestamp"],
        "tool_id": internal_record.get("tool_id", "vaultghost-adapter/v1"),
        "input": internal_record.get("input", {}),
        "output": internal_record.get("output", {}),
        "prev_turn_hash": internal_record.get("prev_turn_hash", GENESIS_HASH),
    }
    canonical_bytes = canonicalize_jcs(payload)
    computed_hash = _sha256_hex(canonical_bytes)
    payload["computed_hash"] = computed_hash

    return {
        "schema_version": payload["schema_version"],
        "event_id": internal_record["turn_id"],
        "payload": payload,
        "computed_hash": computed_hash,
        "signature": None,
        "signer": None,
        "_verification": None,
    }
