"""
VaultGhost Agent Firewall v0.1-FREEZE / PATCH-3
Validator: Temporal Reference
Status: BASELINE SKELETON - SELF-VALIDATION ADDED, NOT PRODUCTION.
"""
from datetime import datetime

def validate_temporal_reference(envelope):
    """
    Validates the temporal reference (timestamp) of the agent run.
    """
    messages = []
    is_valid = True

    timestamp_str = envelope.get("timestamp")
    if not timestamp_str:
        is_valid = False
        messages.append({"type": "error", "text": "Missing timestamp in envelope.", "code": "MISSING_TIMESTAMP"})
        return {"is_valid": is_valid, "messages": messages}

    try:
        # Check if it's a valid ISO 8601 format
        # Ensure we handle Z and other offsets correctly for comparison
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
        
        # Example: timestamp should not be in the future
        if dt > datetime.now().astimezone():
             messages.append({"type": "warning", "text": "Timestamp is in the future.", "code": "FUTURE_TIMESTAMP"})
             # We might still consider it valid for now, or mark as invalid
             # is_valid = False 
    except ValueError:
        is_valid = False
        messages.append({"type": "error", "text": "Invalid timestamp format. Expected ISO 8601.", "code": "INVALID_TIMESTAMP"})

    return {"is_valid": is_valid, "messages": messages}
