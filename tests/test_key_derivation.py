"""
StegoVault - Key Derivation Tests
Verifies Scrypt key derivation mechanics, output dimensions, and determinism.
"""

import pytest
from crypto.key_derivation import (
    DERIVED_KEY_SIZE,
    SALT_SIZE,
    derive_key,
    generate_salt,
)


def test_salt_length_and_randomness():
    """Verify generated salts are 16 bytes and distinct across calls."""
    salt1 = generate_salt()
    salt2 = generate_salt()

    assert len(salt1) == SALT_SIZE
    assert len(salt2) == SALT_SIZE
    assert salt1 != salt2


def test_derived_key_is_32_bytes():
    """Verify derived key satisfies AES-256 length requirements."""
    salt = generate_salt()
    key = derive_key("master_password", salt)

    assert isinstance(key, bytes)
    assert len(key) == DERIVED_KEY_SIZE


def test_deterministic_derivation():
    """Verify identical credentials yield identical keys with identical salts."""
    salt = generate_salt()
    passphrase = "consistent_secure_passphrase"

    key1 = derive_key(passphrase, salt)
    key2 = derive_key(passphrase, salt)

    assert key1 == key2


def test_different_salt_different_key():
    """Verify varying salts yield distinct keys under an identical passphrase."""
    passphrase = "identical_passphrase"
    salt1 = generate_salt()
    salt2 = generate_salt()

    key1 = derive_key(passphrase, salt1)
    key2 = derive_key(passphrase, salt2)

    assert key1 != key2


def test_different_password_different_key():
    """Verify varying passphrases yield distinct keys with an identical salt."""
    salt = generate_salt()
    key1 = derive_key("passphrase_one", salt)
    key2 = derive_key("passphrase_two", salt)

    assert key1 != key2


def test_invalid_salt_length_rejection():
    """Verify derivation rejects salts that are not 16 bytes."""
    with pytest.raises(ValueError, match="Salt must be exactly 16 bytes"):
        derive_key("passphrase", b"too_short")

    with pytest.raises(ValueError, match="Salt must be exactly 16 bytes"):
        derive_key("passphrase", b"a" * 32)


def test_passphrase_type_acceptance():
    """Verify both str and bytes passphrases are accepted and yield equivalent keys."""
    salt = generate_salt()
    key_str = derive_key("passphrase", salt)
    key_bytes = derive_key(b"passphrase", salt)

    assert key_str == key_bytes