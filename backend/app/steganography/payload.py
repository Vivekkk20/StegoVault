"""
StegoVault Structured Payload Specification & Binary Serialization
Header:
- MAGIC (6 bytes): b"SVAULT"
- VERSION (1 byte): 0x01
- FLAGS (1 byte): bit 0=AES-256-GCM, bit 1=zlib
- ITERATIONS (4 bytes): PBKDF2 iteration count (uint32 big-endian)
- SALT (16 bytes): PBKDF2 random salt
- NONCE (12 bytes): AES-GCM 96-bit IV
- CIPHERTEXT_LENGTH (4 bytes): uint32 big-endian
- AUTH_TAG (16 bytes): AES-GCM 128-bit authentication tag
- HEADER_CRC32 (4 bytes): uint32 CRC32 of preceding 60 bytes
Body:
- CIPHERTEXT (N bytes)
Trailer:
- PAYLOAD_SHA256 (32 bytes): SHA-256 checksum of header + ciphertext
"""
import struct
import zlib
import hashlib
from typing import Tuple

from app.core.exceptions import (
    InvalidPayloadError,
    CorruptedPayloadError,
    AuthenticationFailedError,
)
from app.security.crypto import (
    encrypt_payload,
    decrypt_payload,
    SALT_SIZE,
    NONCE_SIZE,
    TAG_SIZE,
)

MAGIC = b"SVAULT"
VERSION = 0x01
HEADER_FORMAT = ">6sBBI16s12sI16sI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 64 bytes
TRAILER_SIZE = 32  # SHA-256 hash
MIN_PAYLOAD_SIZE = HEADER_SIZE + TRAILER_SIZE  # 96 bytes


def pack_payload(message: str, password: str, compress: bool = True) -> bytes:
    """
    Encrypts secret message and packs into the StegoVault structured binary payload.
    """
    if not message:
        raise ValueError("Secret message cannot be empty")
    if not password:
        raise ValueError("Password cannot be empty")

    plaintext_bytes = message.encode("utf-8")
    
    # Encrypt
    salt, nonce, ciphertext, auth_tag, flags, iterations = encrypt_payload(
        plaintext=plaintext_bytes,
        password=password,
        associated_data=MAGIC + bytes([VERSION]),
        compress=compress,
    )

    ciphertext_len = len(ciphertext)

    # Partial header without CRC32 (60 bytes)
    pre_header = struct.pack(
        ">6sBBI16s12sI16s",
        MAGIC,
        VERSION,
        flags,
        iterations,
        salt,
        nonce,
        ciphertext_len,
        auth_tag,
    )
    # Calculate CRC32 of pre-header
    header_crc = zlib.crc32(pre_header) & 0xFFFFFFFF
    
    # Complete 64-byte header
    header = pre_header + struct.pack(">I", header_crc)

    # Body: ciphertext
    body = ciphertext

    # Trailer: SHA-256 of header + body
    checksum = hashlib.sha256(header + body).digest()

    return header + body + checksum


def inspect_payload_header(data: bytes) -> Tuple[int, int, int, bytes, bytes, int, bytes, int]:
    """
    Inspects and validates the 64-byte header from extracted binary stream.
    Returns:
        (version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc)
    """
    if len(data) < HEADER_SIZE:
        raise InvalidPayloadError(
            f"Data too short ({len(data)} bytes) to contain a StegoVault header (requires {HEADER_SIZE} bytes)."
        )

    magic, version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc = struct.unpack(
        HEADER_FORMAT, data[:HEADER_SIZE]
    )

    if magic != MAGIC:
        raise InvalidPayloadError(
            f"Invalid magic signature: expected '{MAGIC.decode()}', found '{magic[:6]!r}'. "
            "No StegoVault payload detected in this image."
        )

    if version != VERSION:
        raise InvalidPayloadError(
            f"Unsupported payload version: {version}. Expected version {VERSION}."
        )

    # Verify header CRC32 of preceding 60 bytes
    expected_crc = zlib.crc32(data[:60]) & 0xFFFFFFFF
    if header_crc != expected_crc:
        raise CorruptedPayloadError(
            f"Header CRC32 mismatch (expected {expected_crc:#010x}, got {header_crc:#010x}). "
            "The image data has been altered or corrupted."
        )

    return version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc


def unpack_payload(payload_bytes: bytes, password: str) -> str:
    """
    Parses, validates, and decrypts structured StegoVault payload.
    Raises:
        InvalidPayloadError: If magic bytes or format mismatch
        CorruptedPayloadError: If CRC32 or SHA-256 verification fails
        AuthenticationFailedError: If password is incorrect
    """
    if len(payload_bytes) < MIN_PAYLOAD_SIZE:
        raise InvalidPayloadError("Insufficient data for a valid StegoVault payload.")

    # Inspect & validate header
    version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc = inspect_payload_header(payload_bytes)

    total_expected = HEADER_SIZE + ciphertext_len + TRAILER_SIZE
    if len(payload_bytes) < total_expected:
        raise CorruptedPayloadError(
            f"Payload truncated: expected at least {total_expected} bytes, available {len(payload_bytes)} bytes."
        )

    header = payload_bytes[:HEADER_SIZE]
    ciphertext = payload_bytes[HEADER_SIZE:HEADER_SIZE + ciphertext_len]
    trailer = payload_bytes[HEADER_SIZE + ciphertext_len:total_expected]

    # Verify trailer SHA-256 checksum
    computed_sha256 = hashlib.sha256(header + ciphertext).digest()
    if trailer != computed_sha256:
        raise CorruptedPayloadError(
            "Payload integrity check failed: SHA-256 checksum mismatch. "
            "The hidden data appears to have been tampered with."
        )

    # Authenticate and decrypt with AES-256-GCM
    decrypted_bytes = decrypt_payload(
        ciphertext=ciphertext,
        auth_tag=auth_tag,
        password=password,
        salt=salt,
        nonce=nonce,
        associated_data=MAGIC + bytes([version]),
        flags=flags,
        iterations=iterations,
    )

    try:
        return decrypted_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise AuthenticationFailedError("Decrypted payload is not valid UTF-8 text.")
