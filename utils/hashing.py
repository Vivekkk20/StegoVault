"""
StegoVault - Cryptographic Hashing Utilities
Provides standard digest calculations (e.g., SHA-256) for payload tracking,
integrity verification, and diagnostic logging.
"""

from __future__ import annotations

import hashlib


def compute_sha256(data: bytes) -> str:
    """
    Computes the SHA-256 hexadecimal digest for arbitrary byte sequences.

    :param data: Byte sequence to hash.
    :return: 64-character hexadecimal SHA-256 digest string.
    """
    digest = hashlib.sha256(data).hexdigest()
    return digest


def verify_sha256(data: bytes, expected_hash: str) -> bool:
    """
    Verifies data integrity against an expected SHA-256 digest
    using a constant-time comparison.

    :param data: Byte sequence to evaluate.
    :param expected_hash: Expected 64-character hex string.
    :return: True if the digest matches, False otherwise.
    """
    actual_hash = compute_sha256(data)
    # Using compare_digest to prevent timing side channels
    return hashlib.compare_digest(actual_hash.lower(), expected_hash.lower())