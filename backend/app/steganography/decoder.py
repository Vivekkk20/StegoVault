"""
LSB Steganography Decoder Module
Extracts and decrypts authenticated binary payloads from lossless RGB/RGBA images.
"""
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Any

from app.core.exceptions import (
    InvalidPayloadError,
    CorruptedPayloadError,
)
from app.steganography.payload import (
    HEADER_SIZE,
    TRAILER_SIZE,
    inspect_payload_header,
    unpack_payload,
)


def extract_raw_lsb_bits(image: Image.Image) -> np.ndarray:
    """
    Extracts LSB bits from RGB channels in order.
    Returns 1D numpy array of uint8 bits (0 or 1).
    """
    img_array = np.array(image)
    mode = image.mode

    if mode == "RGB":
        flattened = img_array.reshape(-1)
        return (flattened & 1).astype(np.uint8)
    elif mode == "RGBA":
        rgb_view = img_array[:, :, :3].reshape(-1)
        return (rgb_view & 1).astype(np.uint8)
    else:
        rgb_img = image.convert("RGB")
        img_array = np.array(rgb_img)
        flattened = img_array.reshape(-1)
        return (flattened & 1).astype(np.uint8)


def detect_stegovault_payload(image: Image.Image) -> Dict[str, Any]:
    """
    Probes image for StegoVault header without needing the password.
    Returns payload detection status and metadata.
    """
    bits = extract_raw_lsb_bits(image)
    header_bits_count = HEADER_SIZE * 8

    if len(bits) < header_bits_count:
        return {
            "detected": False,
            "reason": "Image has fewer pixels than required for a StegoVault header.",
        }

    header_bytes = np.packbits(bits[:header_bits_count]).tobytes()
    try:
        version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc = inspect_payload_header(header_bytes)
        total_payload_bytes = HEADER_SIZE + ciphertext_len + TRAILER_SIZE
        
        return {
            "detected": True,
            "version": version,
            "flags": flags,
            "iterations": iterations,
            "compressed": bool(flags & 0x02),
            "ciphertext_length": ciphertext_len,
            "total_payload_bytes": total_payload_bytes,
            "header_crc_valid": True,
        }
    except InvalidPayloadError as e:
        return {
            "detected": False,
            "reason": str(e),
        }
    except CorruptedPayloadError as e:
        return {
            "detected": True,
            "header_crc_valid": False,
            "error": str(e),
        }


def extract_payload_from_image(image: Image.Image, password: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts, validates, and decrypts hidden message from image.
    """
    bits = extract_raw_lsb_bits(image)
    header_bits_count = HEADER_SIZE * 8

    if len(bits) < header_bits_count:
        raise InvalidPayloadError("Image is too small to contain a StegoVault header.")

    header_bytes = np.packbits(bits[:header_bits_count]).tobytes()
    version, flags, iterations, salt, nonce, ciphertext_len, auth_tag, header_crc = inspect_payload_header(header_bytes)

    total_bytes = HEADER_SIZE + ciphertext_len + TRAILER_SIZE
    total_bits = total_bytes * 8

    if len(bits) < total_bits:
        raise CorruptedPayloadError(
            f"Image dimensions insufficient for full payload: need {total_bits} bits, "
            f"but image only yields {len(bits)} bits."
        )

    # Extract full payload bytes
    payload_bytes = np.packbits(bits[:total_bits]).tobytes()

    # Decrypt and verify
    plaintext = unpack_payload(payload_bytes, password)

    metadata = {
        "version": version,
        "payload_bytes": total_bytes,
        "ciphertext_bytes": ciphertext_len,
        "iterations": iterations,
        "compressed": bool(flags & 0x02),
        "integrity_verified": True,
    }

    return plaintext, metadata
