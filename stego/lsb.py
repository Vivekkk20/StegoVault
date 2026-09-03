"""
StegoVault - Spatial Domain LSB Manipulation
Provides bitwise operations to embed and extract binary bitstreams within
the Least Significant Bits of 8-bit image color channels (RGB/RGBA).
"""

from __future__ import annotations

from PIL import Image

from core.exceptions import InsufficientCapacityError


def embed_lsb(carrier_image: Image.Image, payload: bytes) -> Image.Image:
    """
    Embeds raw payload bytes into the Least Significant Bits of carrier image pixels.
    Supports RGB and RGBA formats (alpha channel is preserved unmodified).

    :param carrier_image: PIL Image in RGB or RGBA mode.
    :param payload: Serialized bytes to embed.
    :return: New PIL Image with payload embedded in LSBs.
    :raises ValueError: If image mode is not supported.
    :raises InsufficientCapacityError: If payload exceeds carrier pixel capacity.
    """
    if carrier_image.mode not in ("RGB", "RGBA"):
        raise ValueError(f"Unsupported image mode '{carrier_image.mode}'. Expected RGB or RGBA.")

    total_bits = len(payload) * 8
    width, height = carrier_image.size
    available_bits = width * height * 3

    if total_bits > available_bits:
        raise InsufficientCapacityError(
            f"Payload requires {total_bits} bits, but carrier capacity is {available_bits} bits."
        )

    # Convert payload bytes to big-endian bitstream
    bitstream = [
        (byte >> shift) & 1
        for byte in payload
        for shift in range(7, -1, -1)
    ]

    has_alpha = carrier_image.mode == "RGBA"
    pixels = list(carrier_image.getdata())
    modified_pixels = []
    bit_idx = 0

    for pixel in pixels:
        if has_alpha:
            r, g, b, a = pixel
        else:
            r, g, b = pixel

        # Embed into Red
        if bit_idx < total_bits:
            r = (r & ~1) | bitstream[bit_idx]
            bit_idx += 1

        # Embed into Green
        if bit_idx < total_bits:
            g = (g & ~1) | bitstream[bit_idx]
            bit_idx += 1

        # Embed into Blue
        if bit_idx < total_bits:
            b = (b & ~1) | bitstream[bit_idx]
            bit_idx += 1

        if has_alpha:
            modified_pixels.append((r, g, b, a))
        else:
            modified_pixels.append((r, g, b))

    stego_image = Image.new(carrier_image.mode, carrier_image.size)
    stego_image.putdata(modified_pixels)
    return stego_image


def extract_lsb(stego_image: Image.Image, num_bytes: int) -> bytes:
    """
    Extracts a fixed number of bytes from the LSBs of target image pixels.

    :param stego_image: PIL Image containing embedded bitstream.
    :param num_bytes: Exact number of bytes to retrieve.
    :return: Extracted byte sequence.
    :raises ValueError: If image mode is not supported.
    :raises InsufficientCapacityError: If requested bytes exceed carrier capacity.
    """
    if stego_image.mode not in ("RGB", "RGBA"):
        raise ValueError(f"Unsupported image mode '{stego_image.mode}'. Expected RGB or RGBA.")

    target_bits = num_bytes * 8
    width, height = stego_image.size
    available_bits = width * height * 3

    if target_bits > available_bits:
        raise InsufficientCapacityError(
            f"Cannot extract {target_bits} bits from carrier with {available_bits} bits available."
        )

    has_alpha = stego_image.mode == "RGBA"
    extracted_bits = []

    for pixel in stego_image.getdata():
        if has_alpha:
            r, g, b, _ = pixel
        else:
            r, g, b = pixel

        extracted_bits.append(r & 1)
        if len(extracted_bits) == target_bits:
            break

        extracted_bits.append(g & 1)
        if len(extracted_bits) == target_bits:
            break

        extracted_bits.append(b & 1)
        if len(extracted_bits) == target_bits:
            break

    # Reassemble bits into bytes (big-endian)
    extracted_bytes = bytearray()
    for i in range(0, target_bits, 8):
        byte_val = 0
        for bit in extracted_bits[i : i + 8]:
            byte_val = (byte_val << 1) | bit
        extracted_bytes.append(byte_val)

    return bytes(extracted_bytes)