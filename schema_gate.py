"""
VaultGhost Agent Firewall v0.1-FREEZE / PATCH-3
Module: Schema Gate
Status: BASELINE SKELETON - SELF-VALIDATION ADDED, NOT PRODUCTION.
"""
import json
import jsonschema
import os

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "schemas")

def load_schema(schema_name):
    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_envelope_schema(envelope):
    """
    Validates the envelope against the agent_run_envelope schema.
    """
    schema = load_schema("agent_run_envelope.schema.json")
    try:
        jsonschema.validate(instance=envelope, schema=schema)
        return {"is_valid": True, "messages": []}
    except jsonschema.ValidationError as e:
        return {
            "is_valid": False, 
            "messages": [{"type": "error", "text": f"Schema validation error: {e.message}", "path": str(e.path)}]
        }

def validate_sanitized_payload_schema(payload):
    """
    Validates the sanitized payload against the sanitized_review_payload schema.
    """
    schema = load_schema("sanitized_review_payload.schema.json")
    # Note: In a real implementation, we would handle local references in the schema.
    # For this skeleton, we assume the schema is self-contained or handled by the validator.
    try:
        jsonschema.validate(instance=payload, schema=schema)
        return {"is_valid": True, "messages": []}
    except jsonschema.ValidationError as e:
        return {
            "is_valid": False, 
            "messages": [{"type": "error", "text": f"Schema validation error: {e.message}", "path": str(e.path)}]
        }
