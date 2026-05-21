"""
VaultGhost Agent Firewall v0.1-FREEZE / PATCH-3
Validator: Cross Reference Integrity
Status: BASELINE SKELETON - SELF-VALIDATION ADDED, NOT PRODUCTION.
"""

def validate_cross_ref_integrity(envelope):
    """
    Validates cross-reference integrity in the agent run envelope.
    Checks for:
    - Missing source references
    - Source-type/ref-kind mismatch
    - Artifact hash presence
    """
    messages = []
    is_valid = True

    source_ref = envelope.get("source_ref")
    source_type = envelope.get("source_type")
    artifact_hash = envelope.get("artifact_hash")

    if not source_ref:
        is_valid = False
        messages.append({"type": "error", "text": "Missing source_ref in envelope.", "code": "MISSING_SOURCE_REF"})

    if not source_type:
        is_valid = False
        messages.append({"type": "error", "text": "Missing source_type in envelope.", "code": "MISSING_SOURCE_TYPE"})

    if source_type == "github_commit" and source_ref and len(source_ref) != 40:
        is_valid = False
        messages.append({"type": "error", "text": "Invalid GitHub commit SHA format.", "code": "INVALID_COMMIT_SHA"})

    if not artifact_hash:
        is_valid = False
        messages.append({"type": "error", "text": "Missing artifact_hash in envelope.", "code": "MISSING_ARTIFACT_HASH"})

    return {"is_valid": is_valid, "messages": messages}
