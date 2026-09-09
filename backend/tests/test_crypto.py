"""
Unit Tests: Cryptographic Engine (AES-256-GCM & PBKDF2-HMAC-SHA256)
"""
import pytest
from app.security.crypto import (
    derive_key,
    encrypt_payload,
    decrypt_payload,
    SALT_SIZE,
    NONCE_SIZE,
    TAG_SIZE,
    KEY_SIZE,
)
from app.core.exceptions import AuthenticationFailedError


def test_key_derivation_deterministic():
    salt = b"A" * SALT_SIZE
    key1 = derive_key("Password123", salt, iterations=1000)
    key2 = derive_key("Password123", salt, iterations=1000)
    assert key1 == key2
    assert len(key1) == KEY_SIZE


def test_key_derivation_diff_password():
    salt = b"A" * SALT_SIZE
    key1 = derive_key("Password1", salt, iterations=1000)
    key2 = derive_key("Password2", salt, iterations=1000)
    assert key1 != key2


def test_encrypt_decrypt_roundtrip():
    secret = b"Highly confidential forensic payload"
    password = "CorrectHorseBatteryStaple!"
    
    salt, nonce, ciphertext, auth_tag, flags, iterations = encrypt_payload(
        secret, password, compress=True, iterations=1000
    )
    assert len(salt) == SALT_SIZE
    assert len(nonce) == NONCE_SIZE
    assert len(auth_tag) == TAG_SIZE
    assert ciphertext != secret  # Plaintext never stored

    decrypted = decrypt_payload(
        ciphertext, auth_tag, password, salt, nonce, flags=flags, iterations=iterations
    )
    assert decrypted == secret


def test_wrong_password_fails_safely():
    secret = b"Test message"
    salt, nonce, ciphertext, auth_tag, flags, iterations = encrypt_payload(
        secret, "RightPassword", iterations=1000
    )

    with pytest.raises(AuthenticationFailedError):
        decrypt_payload(
            ciphertext, auth_tag, "WrongPassword", salt, nonce, flags=flags, iterations=iterations
        )


def test_tampered_ciphertext_fails():
    secret = b"Test message"
    salt, nonce, ciphertext, auth_tag, flags, iterations = encrypt_payload(
        secret, "Password123", iterations=1000
    )
    
    # Tamper with 1 byte of ciphertext
    tampered = bytearray(ciphertext)
    tampered[0] ^= 0x01

    with pytest.raises(AuthenticationFailedError):
        decrypt_payload(
            bytes(tampered), auth_tag, "Password123", salt, nonce, flags=flags, iterations=iterations
        )


def test_tampered_auth_tag_fails():
    secret = b"Test message"
    salt, nonce, ciphertext, auth_tag, flags, iterations = encrypt_payload(
        secret, "Password123", iterations=1000
    )

    tampered_tag = bytearray(auth_tag)
    tampered_tag[0] ^= 0x01

    with pytest.raises(AuthenticationFailedError):
        decrypt_payload(
            ciphertext, bytes(tampered_tag), "Password123", salt, nonce, flags=flags, iterations=iterations
        )
