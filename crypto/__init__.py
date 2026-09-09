"""
StegoVault - Cryptography Package
Provides authenticated symmetric encryption (AES-256-GCM) and password-based key derivation (Scrypt).

Modules:
    encryption: AES-256-GCM authenticated encryption and decryption with AAD binding.
    key_derivation: Memory-hard Scrypt key derivation function and salt generation.
"""

from crypto.encryption import (
    AUTH_TAG_SIZE_BYTES,
    KEY_SIZE_BYTES,
    NONCE_SIZE_BYTES,
    decrypt_payload,
    encrypt_payload,
    generate_nonce,
)
from crypto.key_derivation import (
    DERIVED_KEY_SIZE,
    SALT_SIZE,
    SCRYPT_N,
    SCRYPT_P,
    SCRYPT_R,
    derive_key,
    generate_salt,
)

__all__ = [
    "encrypt_payload",
    "decrypt_payload",
    "generate_nonce",
    "derive_key",
    "generate_salt",
    "KEY_SIZE_BYTES",
    "NONCE_SIZE_BYTES",
    "AUTH_TAG_SIZE_BYTES",
    "SALT_SIZE",
    "DERIVED_KEY_SIZE",
    "SCRYPT_N",
    "SCRYPT_R",
    "SCRYPT_P",
]
