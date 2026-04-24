import argparse
import sys
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def keygen(args):
    from .sign import generate_keypair, save_private_key, save_public_key
    priv, pub = generate_keypair()
    save_private_key(priv, args.private_out)
    save_public_key(pub, args.public_out)
    print(f"Keys saved to {args.private_out} and {args.public_out}")

def turn_sign(args):
    from .sign import load_private_key
    from .turn import sign_turn_record
    priv = load_private_key(args.key)
    with open(args.in_file) as f:
        turn = json.load(f)
    signed = sign_turn_record(priv, turn)
    output = json.dumps(signed, indent=2)
    if args.out:
        args.out.write_text(output)
    else:
        print(output)

def turn_verify(args):
    from .sign import load_public_key, verify_signature
    from .canonical import canonicalize_jcs
    with open(args.in_file) as f:
        turn = json.load(f)
    # Fix 3 (Code Review Report, April 24, 2026): do not pop signature in-place.
    # Use a copy-based approach so the loaded dict is never mutated.
    sig_obj = turn.get("signature")
    turn_for_verify = {k: v for k, v in turn.items() if k != "signature"}
    canonical_bytes = canonicalize_jcs(turn_for_verify)
    sig_bytes = base64.b64decode(sig_obj["sig"])
    if args.pubkey:
        pub = load_public_key(args.pubkey)
    else:
        pubkey_bytes = base64.b64decode(sig_obj["pubkey"])
        pub = Ed25519PublicKey.from_public_bytes(pubkey_bytes)
    valid = verify_signature(pub, sig_bytes, canonical_bytes)
    if valid:
        print("Signature OK")
    else:
        print("Signature INVALID", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="VaultGhost Core CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    keygen_parser = sub.add_parser("keygen", help="Generate Ed25519 key pair")
    keygen_parser.add_argument("--private-out", type=Path, default="ed25519_sk.bin")
    keygen_parser.add_argument("--public-out", type=Path, default="ed25519_pk.bin")

    sign_parser = sub.add_parser("turn-sign", help="Sign a turn record")
    sign_parser.add_argument("--key", required=True, type=Path, help="Private key file")
    sign_parser.add_argument("--in-file", required=True, type=Path, help="Input turn JSON")
    sign_parser.add_argument("--out", type=Path, help="Output signed JSON (default: stdout)")

    verify_parser = sub.add_parser("turn-verify", help="Verify a signed turn record")
    verify_parser.add_argument("--in-file", required=True, type=Path, help="Input signed turn JSON")
    verify_parser.add_argument("--pubkey", type=Path, help="Optional public key file (overrides embedded)")

    args = parser.parse_args()

    if args.cmd == "keygen":
        keygen(args)
    elif args.cmd == "turn-sign":
        turn_sign(args)
    elif args.cmd == "turn-verify":
        turn_verify(args)

if __name__ == "__main__":
    main()
