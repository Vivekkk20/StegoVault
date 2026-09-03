"""
StegoVault - Authenticated Symmetric Encryption
Provides AES-256-GCM encryption and decryption routines with AAD support.
"""

from __future__ import annotations

import os
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from core.exceptions import AuthenticationError

KEY_SIZE_BYTES: int = 32
NONCE_SIZE_BYTES: int = 12
AUTH_TAG_SIZE_BYTES: int = 16


def generate_nonce() -> bytes:
    """Generates a 12-byte cryptographically secure random nonce for AES-GCM."""
    return os.urandom(NONCE_SIZE_BYTES)


def encrypt_payload(
    plaintext: bytes,
    key: bytes,
    nonce: bytes | None = None,
    associated_data: bytes | None = None,
) -> tuple[bytes, bytes, bytes]:
    """
    Encrypts plaintext using AES-256-GCM.

    :param plaintext: Data to encrypt.
    :param key: 32-byte symmetric key.
    :param nonce: Optional 12-byte nonce (generated randomly if omitted).
    :param associated_data: Additional Authenticated Data (AAD) bound to the ciphertext.
    :return: (ciphertext, nonce, auth_tag)
    """
    if len(key) != KEY_SIZE_BYTES:
        raise ValueError(f"AES-256 key must be exactly {KEY_SIZE_BYTES} bytes.")

    if nonce is None:
        nonce = generate_nonce()
    elif len(nonce) != NONCE_SIZE_BYTES:
        raise ValueError(f"Nonce must be exactly {NONCE_SIZE_BYTES} bytes.")

    aesgcm = AESGCM(key)
    # The cryptography library appends the 16-byte tag to the ciphertext
    ct_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data)
    ciphertext = ct_with_tag[:-AUTH_TAG_SIZE_BYTES]
    auth_tag = ct_with_tag[-AUTH_TAG_SIZE_BYTES:]

    return ciphertext, nonce, auth_tag


def decrypt_payload(
    ciphertext: bytes,
    key: bytes,
    nonce: bytes,
    auth_tag: bytes,
    associated_data: bytes | None = None,
) -> bytes:
    """
    Decrypts and verifies ciphertext using AES-256-GCM and its authentication tag.

    :param ciphertext: Encrypted bytes.
    :param key: 32-byte symmetric key.
    :param nonce: 12-byte nonce used during encryption.
    :param auth_tag: 16-byte authentication tag.
    :param associated_data: Additional Authenticated Data (AAD) to verify.
    :return: Decrypted plaintext.
    :raises AuthenticationError: If decryption/tag validation fails.
    """
    if len(key) != KEY_SIZE_BYTES:
        raise ValueError(f"AES-256 key must be exactly {KEY_SIZE_BYTES} bytes.")

    if len(nonce) != NONCE_SIZE_BYTES:
        raise ValueError(f"Nonce must be exactly {NONCE_SIZE_BYTES} bytes.")

    if len(auth_tag) != AUTH_TAG_SIZE_BYTES:
        raise ValueError(f"Authentication tag must be exactly {AUTH_TAG_SIZE_BYTES} bytes.")

    aesgcm = AESGCM(key)
    combined_ct = ciphertext + auth_tag

    try:
        plaintext = aesgcm.decrypt(nonce, combined_ct, associated_data)
        return plaintext
    except InvalidTag as exc:
        # Standardize and prevent leakage of secret/timing details
        raise AuthenticationError(
            "Cryptographic verification failed: invalid credentials or corrupted payload."
        ) from exc