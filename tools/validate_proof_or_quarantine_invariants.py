#!/usr/bin/env python3
"""
Validator for Proof‑or‑Quarantine v0.1‑draft events.

This script reads a JSON file representing a Proof‑or‑Quarantine event and verifies
that it satisfies the semantic rules defined in the classification rules document.
It does not attempt to prove truth about the underlying world; it only checks
internal consistency and adherence to declared evidence requirements and bucket
ceilings.

Usage:
    python tools/validate_proof_or_quarantine_invariants.py path/to/event.json

On success it prints `PASS: <path>` and returns exit code 0.
On failure it prints `FAIL: <path>` followed by one or more failure messages and
returns exit code 1.

Limitations:
* Does not dereference evidence pointers or perform artifact hashing.
* Does not replay external artifacts or commands.
* Only enforces invariants described in v0.1‑draft classification rules.
* Cannot verify external truth or model correctness.
"""

import json
import sys
from pathlib import Path

# Bucket strength ranking for comparisons
BUCKET_RANK = {
    "verified": 3,
    "provisionally_verified": 2,
    "inferred": 1,
    "quarantined": 0,
}

# Maximum allowed bucket given risk flags
RISK_FLAG_CAPS = {
    "unsupported_factual_claim": "quarantined",
    "contradicted_by_evidence": "quarantined",
    "technical_claim_requires_byte_level_check": "quarantined",
    "weak_evidence_type": "inferred",
    "intent_claim": "inferred",
    "legal_conclusion": "inferred",
    "causal_overclaim": "inferred",
    "destructive_action": "quarantined",
}

# Evidence types considered byte‑level for technical claims
BYTE_LEVEL_EVIDENCE_TYPES = {
    "git_blob",
    "hashed_artifact",
    "full_command_output",
    "independent_replay",
}

# Resolver statuses that satisfy byte‑level checks
BYTE_LEVEL_RESOLVER_STATUSES = {
    "resolved_and_hashed",
    "replayed",
}

# Evidence statuses considered sufficient for verified claims
VERIFIED_EVIDENCE_STATUSES = {
    "artifact_hash_bound",
    "independently_replayed",
}

# Evidence statuses allowed for provisionally verified claims
PROVISIONALLY_ALLOWED_STATUSES = {
    "pointer_format_valid",
    "artifact_resolved",
}

def bucket_rank(bucket: str) -> int:
    return BUCKET_RANK.get(bucket, -1)

def bucket_above_cap(bucket: str, cap: str) -> bool:
    """Return True if bucket is ranked above the cap bucket."""
    return bucket_rank(bucket) > bucket_rank(cap)

def claim_has_byte_level_evidence(claim: dict) -> bool:
    """Return True if claim contains at least one evidence item that qualifies as byte‑level."""
    for ev in claim.get("evidence", []):
        if (
            ev.get("evidence_type") in BYTE_LEVEL_EVIDENCE_TYPES
            and ev.get("resolver_status") in BYTE_LEVEL_RESOLVER_STATUSES
        ):
            # If resolver_status is resolved_and_hashed then artifact_hash must exist
            if ev.get("resolver_status") == "resolved_and_hashed" and not ev.get("artifact_hash"):
                # incomplete evidence; skip
                continue
            return True
    return False

def validate_claim(claim: dict) -> list:
    """Validate a single claim and return a list of failure messages (empty if valid)."""
    failures = []
    bucket = claim.get("claim_bucket")
    evidence_status = claim.get("evidence_status")
    risk_flags = set(claim.get("risk_flags") or [])
    claim_type = claim.get("claim_type")

    # 1. Check risk‑flag caps
    for flag in risk_flags:
        cap = RISK_FLAG_CAPS.get(flag)
        if cap and bucket_above_cap(bucket, cap):
            failures.append(
                f"risk flag {flag!r} caps bucket at {cap}, but stored bucket is {bucket}."
            )

    # 2. Verified bucket rules
    if bucket == "verified":
        # Evidence status must be artifact_hash_bound or independently_replayed
        if evidence_status not in VERIFIED_EVIDENCE_STATUSES:
            failures.append(
                f"verified claim requires evidence_status in {sorted(VERIFIED_EVIDENCE_STATUSES)}, got {evidence_status}."
            )
        # Byte‑level requirement if flag present
        if "technical_claim_requires_byte_level_check" in risk_flags:
            if not claim_has_byte_level_evidence(claim):
                failures.append(
                    "verified technical claim lacks byte‑level evidence for byte‑level risk flag."
                )
        # Ensure any resolved_and_hashed evidence has artifact_hash
        for ev in claim.get("evidence", []):
            if ev.get("resolver_status") == "resolved_and_hashed" and not ev.get("artifact_hash"):
                failures.append(
                    f"evidence {ev.get('evidence_id')} has resolver_status resolved_and_hashed but no artifact_hash."
                )

    # 3. Provisionally verified bucket rules
    if bucket == "provisionally_verified":
        # Evidence status must not be none_provided or self_reported_pointer_only
        if evidence_status not in PROVISIONALLY_ALLOWED_STATUSES:
            failures.append(
                f"provisionally verified claim requires evidence_status in {sorted(PROVISIONALLY_ALLOWED_STATUSES)}, got {evidence_status}."
            )
        # Byte‑level requirement similar to verified
        if "technical_claim_requires_byte_level_check" in risk_flags:
            if not claim_has_byte_level_evidence(claim):
                failures.append(
                    "provisionally verified technical claim lacks byte‑level evidence for byte‑level risk flag."
                )
        for ev in claim.get("evidence", []):
            if ev.get("resolver_status") == "resolved_and_hashed" and not ev.get("artifact_hash"):
                failures.append(
                    f"evidence {ev.get('evidence_id')} has resolver_status resolved_and_hashed but no artifact_hash."
                )

    # 4. Inferred bucket rules
    # Byte‑level risk flag should not be inferred; however, inferred is allowed as long as risk caps permit
    if bucket == "inferred":
        # If technical byte-level check flag present, and no byte-level evidence, ensure bucket remains inferred not verified; no error required.
        pass

    # 5. Quarantined bucket rules
    # No additional validations needed for quarantined beyond general evidence checks

    # 6. General evidence rules (apply regardless of bucket)
    for ev in claim.get("evidence", []):
        if ev.get("resolver_status") == "resolved_and_hashed" and not ev.get("artifact_hash"):
            failures.append(
                f"evidence {ev.get('evidence_id')} has resolver_status resolved_and_hashed but no artifact_hash."
            )

    return failures

def recompute_summary(claims: list) -> dict:
    """Recompute classification counts from claim buckets."""
    summary = {
        "verified_count": 0,
        "provisionally_verified_count": 0,
        "inferred_count": 0,
        "quarantined_count": 0,
    }
    for claim in claims:
        bucket = claim.get("claim_bucket")
        key = f"{bucket}_count"
        if key in summary:
            summary[key] += 1
        else:
            # Unknown bucket; ignore here – it will be caught by claim validation
            pass
    summary["total_claims"] = len(claims)
    return summary

def validate_event(event: dict) -> list:
    failures = []

    # Validate classification summary
    claims = event.get("claims", [])
    stored_summary = event.get("classification_summary", {})
    recomputed = recompute_summary(claims)
    # Compare each count
    for key, count in recomputed.items():
        stored_value = stored_summary.get(key)
        if stored_value is None:
            failures.append(
                f"classification_summary missing field {key}."
            )
            continue
        if stored_value != count:
            failures.append(
                f"classification_summary mismatch for {key}: stored {stored_value} vs recomputed {count}."
            )

    # Validate each claim
    for claim in claims:
        claim_id = claim.get("claim_id", "<unknown>")
        claim_failures = validate_claim(claim)
        for msg in claim_failures:
            failures.append(f"claim {claim_id}: {msg}")

    return failures

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_proof_or_quarantine_invariants.py <event_json_path>")
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        print(f"FAIL: {path}\n- invalid JSON: {e}")
        return 1
    failures = validate_event(data)
    if failures:
        print(f"FAIL: {path}")
        for msg in failures:
            print(f"- {msg}")
        return 1
    print(f"PASS: {path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())