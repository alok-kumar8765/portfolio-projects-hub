
import os
import hmac
import hashlib
import secrets

ITERATIONS = 600_000

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )
    return f"{salt.hex()}${derived.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, expected_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            ITERATIONS
        )

        return hmac.compare_digest(
            actual.hex(), expected_hex
        )
    except (ValueError, TypeError):
        return False
