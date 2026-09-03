"""
StegoVault - Key Derivation Function (KDF)
Derives 256-bit symmetric keys from user passphrases using Scrypt.
"""

from __future__ import annotations

import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Cryptographic Sizing Constants
SALT_SIZE: int = 16
DERIVED_KEY_SIZE: int = 32

# Scrypt Configuration Parameters
# Selected for memory-hardness against GPU/ASIC parallel password search.
# n = 2^14 (16,384 iterations), r = 8 (block size), p = 1 (parallelization)
# Requires ~16 MiB of RAM per derivation.
SCRYPT_N: int = 16384
SCRYPT_R: int = 8
SCRYPT_P: int = 1


def generate_salt() -> bytes:
    """Generates a 16-byte cryptographically secure pseudorandom salt."""
    return os.urandom(SALT_SIZE)


def derive_key(
    passphrase: str | bytes,
    salt: bytes,
    n: int = SCRYPT_N,
    r: int = SCRYPT_R,
    p: int = SCRYPT_P,
    key_length: int = DERIVED_KEY_SIZE,
) -> bytes:
    """
    Derives a 256-bit symmetric cryptographic key using Scrypt.

    :param passphrase: User-supplied passphrase (str or raw bytes).
    :param salt: 16-byte random salt.
    :param n: CPU/Memory cost parameter (must be a power of 2).
    :param r: Block size parameter.
    :param p: Parallelization parameter.
    :param key_length: Length of derived key in bytes (default 32).
    :return: 32-byte derived symmetric key.
    """
    if not isinstance(salt, (bytes, bytearray)) or len(salt) != SALT_SIZE:
        raise ValueError(f"Salt must be exactly {SALT_SIZE} bytes.")

    if isinstance(passphrase, str):
        password_bytes = passphrase.encode("utf-8")
    elif isinstance(passphrase, (bytes, bytearray)):
        password_bytes = bytes(passphrase)
    else:
        raise TypeError("Passphrase must be a string or bytes.")

    kdf = Scrypt(
        salt=salt,
        length=key_length,
        n=n,
        r=r,
        p=p,
    )
    return kdf.derive(password_bytes)