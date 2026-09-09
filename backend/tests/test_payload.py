"""
Unit Tests: Structured Binary Payload Packing & Unpacking
"""
import pytest
from app.steganography.payload import (
    pack_payload,
    unpack_payload,
    inspect_payload_header,
    MAGIC,
    VERSION,
    HEADER_SIZE,
)
from app.core.exceptions import (
    InvalidPayloadError,
    CorruptedPayloadError,
    AuthenticationFailedError,
)


def test_pack_unpack_payload():
    message = "StegoVault test secret message"
    password = "MySecurePassword2026"

    packed = pack_payload(message, password, compress=True)
    assert packed.startswith(MAGIC)
    assert len(packed) > HEADER_SIZE

    version, flags, iterations, salt, nonce, ct_len, tag, crc = inspect_payload_header(packed)
    assert version == VERSION
    assert iterations > 0

    unpacked = unpack_payload(packed, password)
    assert unpacked == message


def test_corrupted_header_crc_detected():
    message = "Secret"
    password = "Pass"
    packed = bytearray(pack_payload(message, password))

    # Flip byte in pre-header (byte 10 is inside salt)
    packed[10] ^= 0xFF

    with pytest.raises(CorruptedPayloadError) as exc_info:
        unpack_payload(bytes(packed), password)
    assert "Header CRC32 mismatch" in str(exc_info.value)


def test_non_stegovault_payload_rejected():
    garbage = b"RANDOM_NON_STEGOVAULT_DATA_OF_SUFFICIENT_LENGTH_FOR_HEADER_SIZE_TESTING_123456"
    with pytest.raises(InvalidPayloadError):
        unpack_payload(garbage, "Password")


def test_truncated_payload_rejected():
    message = "A longer secret message to ensure substantial payload size"
    password = "Password123"
    packed = pack_payload(message, password)

    # Truncate halfway
    truncated = packed[:len(packed) - 20]
    with pytest.raises(CorruptedPayloadError):
        unpack_payload(truncated, password)
