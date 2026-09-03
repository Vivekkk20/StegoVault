"""
StegoVault - Cryptographic Unit Tests
Validates AES-256-GCM behavior, AAD integrity, wire envelope framing,
and error handling.
"""

import pytest

from core.exceptions import (
    AuthenticationError,
    CorruptPayloadError,
    InvalidPayloadError,
)
from core.payload import (
    HEADER_SIZE,
    MAGIC_HEADER,
    PAYLOAD_TYPE_BINARY,
    PAYLOAD_TYPE_TEXT,
    TOTAL_PREFIX_SIZE,
    EnvelopeHeader,
    StegoEnvelope,
)
from crypto.encryption import (
    AUTH_TAG_SIZE_BYTES,
    KEY_SIZE_BYTES,
    NONCE_SIZE_BYTES,
    decrypt_payload,
    encrypt_payload,
    generate_nonce,
)
from crypto.key_derivation import derive_key, generate_salt


@pytest.fixture
def sample_key() -> bytes:
    salt = generate_salt()
    return derive_key("StrongTestPassphrase123!", salt)


# --- 1. Basic Encryption/Decryption and Input Types ---

def test_encrypt_decrypt_round_trip(sample_key):
    """Verify basic plaintext round-trip."""
    data = b"Confidential Payload Message"
    ct, nonce, tag = encrypt_payload(data, sample_key)
    decrypted = decrypt_payload(ct, sample_key, nonce, tag)

    assert decrypted == data


def test_empty_plaintext(sample_key):
    """Verify encryption and decryption of zero-byte inputs."""
    data = b""
    ct, nonce, tag = encrypt_payload(data, sample_key)
    decrypted = decrypt_payload(ct, sample_key, nonce, tag)

    assert decrypted == b""
    assert len(ct) == 0
    assert len(tag) == AUTH_TAG_SIZE_BYTES


def test_unicode_utf8_payload(sample_key):
    """Verify multibyte UTF-8 Unicode characters are handled correctly."""
    text = "StegoVault 🔒 密碼學 • 🔐 • Проверка"
    data = text.encode("utf-8")
    ct, nonce, tag = encrypt_payload(data, sample_key)
    decrypted = decrypt_payload(ct, sample_key, nonce, tag)

    assert decrypted.decode("utf-8") == text


def test_arbitrary_binary_data(sample_key):
    """Verify non-text, high-entropy binary inputs decrypt bit-identically."""
    import os
    data = os.urandom(2048)
    ct, nonce, tag = encrypt_payload(data, sample_key)
    decrypted = decrypt_payload(ct, sample_key, nonce, tag)

    assert decrypted == data


# --- 2. Ciphertext and Nonce Randomness ---

def test_nonce_is_12_bytes():
    """Verify nonces are generated with the standard 96-bit length."""
    nonce = generate_nonce()
    assert len(nonce) == NONCE_SIZE_BYTES


def test_distinct_encryptions_same_plaintext(sample_key):
    """Verify identical plaintexts generate distinct ciphertexts due to fresh nonces."""
    data = b"Constant Plaintext"
    ct1, nonce1, tag1 = encrypt_payload(data, sample_key)
    ct2, nonce2, tag2 = encrypt_payload(data, sample_key)

    assert nonce1 != nonce2
    assert ct1 != ct2
    assert tag1 != tag2


# --- 3. Tampering and Authentication Failures ---

def test_wrong_password_fails_authentication():
    """Verify an incorrect passphrase derivation fails tag authentication."""
    salt = generate_salt()
    key_correct = derive_key("CorrectPassword", salt)
    key_wrong = derive_key("WrongPassword", salt)

    ct, nonce, tag = encrypt_payload(b"Top Secret", key_correct)

    with pytest.raises(AuthenticationError) as exc_info:
        decrypt_payload(ct, key_wrong, nonce, tag)

    assert "Cryptographic verification failed" in str(exc_info.value)
    # Ensure raw secret materials are never leaked
    assert "CorrectPassword" not in str(exc_info.value)
    assert "WrongPassword" not in str(exc_info.value)


def test_modified_ciphertext_fails(sample_key):
    """Verify single-bit modifications in ciphertext fail GCM validation."""
    data = b"Sensitive Data"
    ct, nonce, tag = encrypt_payload(data, sample_key)

    # Flip the first bit
    corrupted_ct = bytes([ct[0] ^ 0x01]) + ct[1:]

    with pytest.raises(AuthenticationError):
        decrypt_payload(corrupted_ct, sample_key, nonce, tag)


def test_modified_authentication_tag_fails(sample_key):
    """Verify modifications to the authentication tag trigger an immediate error."""
    data = b"Sensitive Data"
    ct, nonce, tag = encrypt_payload(data, sample_key)

    corrupted_tag = bytes([tag[0] ^ 0xFF]) + tag[1:]

    with pytest.raises(AuthenticationError):
        decrypt_payload(ct, sample_key, nonce, corrupted_tag)


def test_modified_nonce_fails(sample_key):
    """Verify decrypting with a modified nonce fails validation."""
    data = b"Sensitive Data"
    ct, nonce, tag = encrypt_payload(data, sample_key)

    corrupted_nonce = bytes([nonce[0] ^ 0x01]) + nonce[1:]

    with pytest.raises(AuthenticationError):
        decrypt_payload(ct, sample_key, corrupted_nonce, tag)


def test_modified_aad_fails(sample_key):
    """Verify tampering with Additional Authenticated Data invalidates the tag."""
    data = b"Sensitive Data"
    aad = b"Version:01;Type:Text"
    ct, nonce, tag = encrypt_payload(data, sample_key, associated_data=aad)

    # Decrypting with altered AAD must fail
    tampered_aad = b"Version:02;Type:Text"
    with pytest.raises(AuthenticationError):
        decrypt_payload(ct, sample_key, nonce, tag, associated_data=tampered_aad)

    # Decrypting with missing AAD must fail
    with pytest.raises(AuthenticationError):
        decrypt_payload(ct, sample_key, nonce, tag, associated_data=None)


# --- 4. Envelope Framing and Protocol Serialization ---

def test_envelope_round_trip_text(sample_key):
    """Verify serialization and deserialization of complete text envelopes."""
    salt = generate_salt()
    plaintext = "Secret text message inside carrier".encode("utf-8")

    header = EnvelopeHeader(
        version=1,
        payload_type=PAYLOAD_TYPE_TEXT,
        reserved=b"\x00\x00",
        ciphertext_len=len(plaintext),
    )
    aad = header.serialize_aad()
    ct, nonce, tag = encrypt_payload(plaintext, sample_key, associated_data=aad)

    envelope = StegoEnvelope(
        header=header,
        salt=salt,
        nonce=nonce,
        auth_tag=tag,
        ciphertext=ct,
    )

    wire_bytes = envelope.serialize()
    deserialized = StegoEnvelope.deserialize(wire_bytes)

    assert deserialized.header.version == 1
    assert deserialized.header.payload_type == PAYLOAD_TYPE_TEXT
    assert deserialized.header.ciphertext_len == len(plaintext)
    assert deserialized.salt == salt
    assert deserialized.nonce == nonce
    assert deserialized.auth_tag == tag
    assert deserialized.ciphertext == ct

    # Complete decryption via deserialized components
    decrypted = decrypt_payload(
        deserialized.ciphertext,
        sample_key,
        deserialized.nonce,
        deserialized.auth_tag,
        associated_data=deserialized.header.serialize_aad(),
    )
    assert decrypted == plaintext


def test_envelope_modified_salt_detection():
    """Verify modifying the salt in the wire frame causes key derivation mismatch."""
    passphrase = "ConsistentPassword"
    salt = generate_salt()
    key = derive_key(passphrase, salt)
    plaintext = b"Payload with salt verification"

    header = EnvelopeHeader(1, PAYLOAD_TYPE_BINARY, b"\x00\x00", len(plaintext))
    ct, nonce, tag = encrypt_payload(plaintext, key, associated_data=header.serialize_aad())

    envelope = StegoEnvelope(header, salt, nonce, tag, ct)
    wire_bytes = bytearray(envelope.serialize())

    # Flip bit in salt field
    salt_offset = HEADER_SIZE
    wire_bytes[salt_offset] ^= 0xFF

    corrupted_env = StegoEnvelope.deserialize(bytes(wire_bytes))
    rederived_key = derive_key(passphrase, corrupted_env.salt)

    with pytest.raises(AuthenticationError):
        decrypt_payload(
            corrupted_env.ciphertext,
            rederived_key,
            corrupted_env.nonce,
            corrupted_env.auth_tag,
            associated_data=corrupted_env.header.serialize_aad(),
        )


def test_envelope_malformed_magic():
    """Verify envelopes with non-matching magic headers are rejected."""
    raw_bad_magic = b"NOPE" + b"\x00" * (TOTAL_PREFIX_SIZE)
    with pytest.raises(CorruptPayloadError, match="magic bytes mismatch"):
        StegoEnvelope.deserialize(raw_bad_magic)


def test_envelope_unsupported_version():
    """Verify envelopes with invalid version bytes are rejected."""
    import struct
    bad_header = struct.pack(">4sBB2sI", MAGIC_HEADER, 99, PAYLOAD_TYPE_TEXT, b"\x00\x00", 0)
    raw_data = bad_header + b"\x00" * (SALT_SIZE + NONCE_SIZE + AUTH_TAG_SIZE_BYTES)

    with pytest.raises(InvalidPayloadError, match="Unsupported payload version"):
        StegoEnvelope.deserialize(raw_data)


def test_envelope_truncated_prefix():
    """Verify payloads shorter than minimum prefix width are rejected."""
    short_data = b"SVLT\x01\x01"
    with pytest.raises(CorruptPayloadError, match="Payload truncated"):
        StegoEnvelope.deserialize(short_data)


def test_envelope_truncated_ciphertext(sample_key):
    """Verify envelopes specifying longer ciphertext lengths than provided fail."""
    header = EnvelopeHeader(1, PAYLOAD_TYPE_TEXT, b"\x00\x00", ciphertext_len=100)
    wire = header.serialize_aad() + (b"\x00" * (SALT_SIZE + NONCE_SIZE + AUTH_TAG_SIZE_BYTES)) + b"short"

    with pytest.raises(CorruptPayloadError, match="Ciphertext length mismatch"):
        StegoEnvelope.deserialize(wire)