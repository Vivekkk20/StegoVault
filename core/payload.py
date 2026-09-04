"""
StegoVault - Binary Wire Envelope Framing and Protocol Specification
Handles binary serialization and deserialization of the cryptographic payload.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from core.exceptions import CorruptPayloadError, InvalidPayloadError

# Protocol Constants
MAGIC_HEADER: bytes = b"SVLT"
CURRENT_VERSION: int = 0x01
SUPPORTED_VERSIONS: set[int] = {0x01}

# Payload Type Flags
PAYLOAD_TYPE_TEXT: int = 0x01
PAYLOAD_TYPE_BINARY: int = 0x02
VALID_PAYLOAD_TYPES: set[int] = {PAYLOAD_TYPE_TEXT, PAYLOAD_TYPE_BINARY}

# Cryptographic Field Widths (in bytes)
SALT_SIZE: int = 16
NONCE_SIZE: int = 12
AUTH_TAG_SIZE: int = 16

# Fixed Header Format:
# Magic (4B) + Version (1B) + Type (1B) + Reserved (2B) + Ciphertext Length (4B)
# = 12 bytes
HEADER_FORMAT: str = ">4sBB2sI"
HEADER_SIZE: int = struct.calcsize(HEADER_FORMAT)
TOTAL_PREFIX_SIZE: int = HEADER_SIZE + SALT_SIZE + NONCE_SIZE + AUTH_TAG_SIZE


@dataclass(frozen=True)
class EnvelopeHeader:
    version: int
    payload_type: int
    reserved: bytes
    ciphertext_len: int

    def serialize_aad(self) -> bytes:
        """
        Serializes protocol metadata passed as Additional Authenticated Data (AAD)
        to the AEAD cipher. Any alteration to this header invalidates the GCM tag.
        """
        return struct.pack(
            HEADER_FORMAT,
            MAGIC_HEADER,
            self.version,
            self.payload_type,
            self.reserved,
            self.ciphertext_len,
        )


@dataclass(frozen=True)
class StegoEnvelope:
    header: EnvelopeHeader
    salt: bytes
    nonce: bytes
    auth_tag: bytes
    ciphertext: bytes

    def serialize(self) -> bytes:
        """
        Encodes the envelope components into an immutable binary wire frame.
        No plaintext, passwords, or derived cryptographic keys are stored.
        """
        aad_bytes = self.header.serialize_aad()
        return (
            aad_bytes
            + self.salt
            + self.nonce
            + self.auth_tag
            + self.ciphertext
        )

    @classmethod
    def deserialize(cls, data: bytes) -> StegoEnvelope:
        """
        Unpacks and validates a serialized byte stream into a StegoEnvelope.
        Enforces strict boundary, size, and magic byte validations.
        """
        if len(data) < TOTAL_PREFIX_SIZE:
            raise CorruptPayloadError(
                f"Payload truncated: received {len(data)} bytes, "
                f"expected at least {TOTAL_PREFIX_SIZE} bytes."
            )

        # 1. Parse Fixed Header
        magic, version, payload_type, reserved, ciphertext_len = struct.unpack_from(
            HEADER_FORMAT, data, 0
        )

        if magic != MAGIC_HEADER:
            raise CorruptPayloadError("Invalid payload identifier: magic bytes mismatch.")

        if version not in SUPPORTED_VERSIONS:
            raise InvalidPayloadError(f"Unsupported payload version: {version}.")

        if payload_type not in VALID_PAYLOAD_TYPES:
            raise InvalidPayloadError(f"Unsupported payload type: {payload_type}.")
        if reserved != b"\x00\x00":
            raise InvalidPayloadError("Unsupported or invalid reserved header flags.")
        header = EnvelopeHeader(
            version=version,
            payload_type=payload_type,
            reserved=reserved,
            ciphertext_len=ciphertext_len,
        )

        # 2. Extract Cryptographic Wire Components
        offset = HEADER_SIZE
        salt = data[offset : offset + SALT_SIZE]
        offset += SALT_SIZE

        nonce = data[offset : offset + NONCE_SIZE]
        offset += NONCE_SIZE

        auth_tag = data[offset : offset + AUTH_TAG_SIZE]
        offset += AUTH_TAG_SIZE

        ciphertext = data[offset:]

        if len(ciphertext) != ciphertext_len:
            raise CorruptPayloadError(
                f"Ciphertext length mismatch: header specifies {ciphertext_len} bytes, "
                f"but found {len(ciphertext)} bytes."
            )

        return cls(
            header=header,
            salt=salt,
            nonce=nonce,
            auth_tag=auth_tag,
            ciphertext=ciphertext,
        )