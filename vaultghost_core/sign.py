"""Ed25519 signature utilities using the cryptography library."""
from __future__ import annotations
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key(private_key: Ed25519PrivateKey, path: Path) -> None:
    path.write_bytes(private_key.private_bytes_raw())

def save_public_key(public_key: Ed25519PublicKey, path: Path) -> None:
    path.write_bytes(public_key.public_bytes_raw())

def load_private_key(path: Path) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(path.read_bytes())

def load_public_key(path: Path) -> Ed25519PublicKey:
    return Ed25519PublicKey.from_public_bytes(path.read_bytes())

def sign_data(private_key: Ed25519PrivateKey, data: bytes) -> bytes:
    return private_key.sign(data)

def verify_signature(public_key: Ed25519PublicKey, signature: bytes, data: bytes) -> bool:
    try:
        public_key.verify(signature, data)
        return True
    except InvalidSignature:
        return False

def pubkey_to_base64(public_key: Ed25519PublicKey) -> str:
    return base64.b64encode(public_key.public_bytes_raw()).decode('ascii')

def signature_to_base64(signature: bytes) -> str:
    return base64.b64encode(signature).decode('ascii')
