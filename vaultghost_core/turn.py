from . import sign
import hashlib

def sign_turn_record(private_key: sign.Ed25519PrivateKey, turn_record: dict) -> dict:
    # Copy to avoid mutating original
    record_copy = turn_record.copy()
    # Remove signature if present
    record_copy.pop("signature", None)
    # Canonicalize and get bytes
    from .canonical import canonicalize_jcs
    canonical_bytes = canonicalize_jcs(record_copy)
    # Compute signature
    sig_bytes = sign.sign_data(private_key, canonical_bytes)
    # Base64 encode
    sig_b64 = sign.signature_to_base64(sig_bytes)
    # Public key base64
    pubkey_b64 = sign.pubkey_to_base64(private_key.public_key())
    # Replace signature with structured object
    turn_record["signature"] = {
        "alg": "Ed25519",
        "pubkey": pubkey_b64,
        "sig": sig_b64,
        "signed_digest": hashlib.sha256(canonical_bytes).hexdigest()
    }
    return turn_record

def build_turn_record(private_key=None, **kwargs):
    # Placeholder for build_turn_record implementation
    turn_record = {
        "type": "TurnRecord",
        "version": "1.0",
        "data": kwargs,
        "signature": "placeholder"
    }
    if private_key:
        return sign_turn_record(private_key, turn_record)
    return turn_record
