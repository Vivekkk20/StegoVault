"""
StegoVault - Core Package
Provides pipeline orchestration, binary wire framing, and security exceptions.

Modules:
    encoder: Pipeline orchestrator for compression, encryption, and LSB embedding.
    decoder: Pipeline orchestrator for extraction, verification, decryption, and decompression.
    payload: Binary wire framing specifications and envelope serialization.
    exceptions: Security-safe domain exceptions preventing timing and data leaks.
"""

from core.decoder import decode_payload
from core.encoder import encode_payload
from core.exceptions import (
    AuthenticationError,
    CorruptPayloadError,
    InsufficientCapacityError,
    InvalidPayloadError,
    StegoVaultError,
)
from core.payload import (
    MAGIC_HEADER,
    PAYLOAD_TYPE_BINARY,
    PAYLOAD_TYPE_TEXT,
    EnvelopeHeader,
    StegoEnvelope,
)

__all__ = [
    "encode_payload",
    "decode_payload",
    "StegoEnvelope",
    "EnvelopeHeader",
    "StegoVaultError",
    "AuthenticationError",
    "CorruptPayloadError",
    "InvalidPayloadError",
    "InsufficientCapacityError",
    "MAGIC_HEADER",
    "PAYLOAD_TYPE_TEXT",
    "PAYLOAD_TYPE_BINARY",
]
