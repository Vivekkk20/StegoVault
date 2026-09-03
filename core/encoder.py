"""
StegoVault - Encoding Pipeline Orchestrator
Coordinates payload compression, key derivation, authenticated encryption,
capacity checking, and LSB spatial embedding into carrier images.
"""

from __future__ import annotations

import zlib
from PIL import Image

from analysis.capacity import payload_fits
from core.exceptions import InsufficientCapacityError
from core.payload import (
    CURRENT_VERSION,
    PAYLOAD_TYPE_BINARY,
    PAYLOAD_TYPE_TEXT,
    EnvelopeHeader,
    StegoEnvelope,
)
from crypto.encryption import encrypt_payload
from crypto.key_derivation import derive_key, generate_salt
from stego.lsb import embed_lsb


def encode_payload(
    carrier_image: Image.Image,
    payload: bytes,
    passphrase: str | bytes,
    payload_type: int = PAYLOAD_TYPE_TEXT,
) -> Image.Image:
    """
    Executes the complete StegoVault encoding pipeline:
    1. Compresses raw payload via zlib.
    2. Generates a fresh 16-byte random salt.
    3. Derives a 256-bit symmetric key using Scrypt.
    4. Serializes the AAD framing header.
    5. Encrypts compressed payload via AES-256-GCM with a random 12-byte nonce.
    6. Assembles the StegoEnvelope binary stream.
    7. Validates carrier capacity headroom.
    8. Embeds the bitstream into the carrier image using spatial LSB.

    :param carrier_image: Cover image in RGB or RGBA mode.
    :param payload: Raw bytes to hide (text UTF-8 or binary file data).
    :param passphrase: User passphrase for key derivation.
    :param payload_type: PAYLOAD_TYPE_TEXT (1) or PAYLOAD_TYPE_BINARY (2).
    :return: Stego PIL Image containing embedded, encrypted payload.
    :raises InsufficientCapacityError: If envelope exceeds carrier pixel capacity.
    :raises ValueError: If image mode is unsupported or payload parameters invalid.
    """
    if payload_type not in (PAYLOAD_TYPE_TEXT, PAYLOAD_TYPE_BINARY):
        raise ValueError(f"Invalid payload type: {payload_type}")

    # 1. Compress raw payload
    compressed_data = zlib.compress(payload, level=9)

    # 2. Key Derivation (Fresh Salt)
    salt = generate_salt()
    derived_key = derive_key(passphrase, salt)

    # 3. Create Envelope Header & Serialize AAD
    header = EnvelopeHeader(
        version=CURRENT_VERSION,
        payload_type=payload_type,
        reserved=b"\x00\x00",
        ciphertext_len=len(compressed_data),
    )
    aad_bytes = header.serialize_aad()

    # 4. Authenticated Encryption (AES-256-GCM)
    ciphertext, nonce, auth_tag = encrypt_payload(
        plaintext=compressed_data,
        key=derived_key,
        associated_data=aad_bytes,
    )

    # 5. Assemble Binary StegoEnvelope
    envelope = StegoEnvelope(
        header=header,
        salt=salt,
        nonce=nonce,
        auth_tag=auth_tag,
        ciphertext=ciphertext,
    )
    wire_bytes = envelope.serialize()

    # 6. Check Carrier Capacity
    if not payload_fits(carrier_image, len(wire_bytes)):
        raise InsufficientCapacityError(
            f"Serialized envelope ({len(wire_bytes)} bytes) exceeds carrier capacity."
        )

    # 7. Spatial LSB Embedding
    stego_image = embed_lsb(carrier_image, wire_bytes)
    return stego_image