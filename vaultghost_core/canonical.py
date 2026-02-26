import rfc8785

def canonicalize_jcs(data: dict) -> bytes:
    """Canonicalize a dictionary using JCS (RFC 8785)."""
    return rfc8785.dumps(data)
