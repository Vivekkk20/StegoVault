"""
StegoVault - Decoding Pipeline Orchestrator
Coordinates stego carrier bitstream extraction, envelope parsing,
AEAD verification, decryption, and decompression back to original data.
"""

from __future__ import annotations

import struct
import zlib
from PIL import Image

from core.exceptions import CorruptPayloadError
from core.payload import (
    HEADER_FORMAT,
    HEADER_SIZE,
    MAGIC_HEADER,
    TOTAL_PREFIX_SIZE,
    StegoEnvelope,
)
from crypto.encryption import decrypt_payload
from crypto.key_derivation import derive_key
from stego.lsb import extract_lsb


def decode_payload(
    stego_image: Image.Image,
    passphrase: str | bytes,
) -> tuple[bytes, int]:
    """
    Executes the complete StegoVault decoding pipeline:
    1. Extracts fixed header bytes via LSB to verify magic bytes and ciphertext length.
    2. Extracts the exact remaining envelope bytes from the carrier.
    3. Deserializes the binary StegoEnvelope structure.
    4. Derives the 256-bit symmetric key using Scrypt and the extracted salt.
    5. Verifies the AEAD authentication tag and decrypts ciphertext via AES-256-GCM.
    6. Decompresses the decrypted stream via zlib.
    7. Returns the original plaintext payload and payload type.

    :param stego_image: Stego image in RGB or RGBA mode.
    :param passphrase: User passphrase for decryption key derivation.
    :return: (recovered_bytes, payload_type)
    :raises AuthenticationError: If passphrase is wrong or payload is tampered.
    :raises CorruptPayloadError: If magic bytes mismatch or framing is corrupt.
    :raises InvalidPayloadError: If version or payload type is unsupported.
    """
    # 1. Extract fixed header to locate magic and read ciphertext length
    header_raw = extract_lsb(stego_image, HEADER_SIZE)
    magic, version, payload_type, reserved, ciphertext_len = struct.unpack_from(
        HEADER_FORMAT, header_raw, 0
    )

    if magic != MAGIC_HEADER:
        raise CorruptPayloadError("Carrier does not contain a valid StegoVault payload.")

    # 2. Extract total required envelope bytes
    total_wire_len = TOTAL_PREFIX_SIZE + ciphertext_len
    full_wire_bytes = extract_lsb(stego_image, total_wire_len)

    # 3. Deserialize binary envelope
    envelope = StegoEnvelope.deserialize(full_wire_bytes)

    # 4. Derive symmetric key using extracted salt
    derived_key = derive_key(passphrase, envelope.salt)

    # 5. Authenticated Decryption (AES-256-GCM + AAD Verification)
    aad_bytes = envelope.header.serialize_aad()
    compressed_plaintext = decrypt_payload(
        ciphertext=envelope.ciphertext,
        key=derived_key,
        nonce=envelope.nonce,
        auth_tag=envelope.auth_tag,
        associated_data=aad_bytes,
    )

    # 6. Decompress payload
    try:
        original_data = zlib.decompress(compressed_plaintext)
    except zlib.error as exc:
        raise CorruptPayloadError("Payload decompression failed: corrupt compressed data.") from exc

    return original_data, envelope.header.payload_type