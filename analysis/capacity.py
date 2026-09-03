"""
StegoVault - Carrier Capacity Engine
Computes maximum safe byte capacity, pixel headroom, and payload consumption
ratios for input images across different channel arrangements.
"""

from __future__ import annotations

from PIL import Image

SAFE_CAPACITY_RATIO: float = 0.15


def calculate_carrier_capacity(carrier_image: Image.Image) -> tuple[int, int]:
    """
    Calculates total usable byte capacity and recommended safe byte limit.
    Only RGB channels are considered for embedding.

    :param carrier_image: PIL Image object.
    :return: (max_bytes, safe_bytes)
    :raises ValueError: If the image mode is not RGB or RGBA.
    """
    if carrier_image.mode not in ("RGB", "RGBA"):
        raise ValueError(f"Unsupported image mode '{carrier_image.mode}'. Expected RGB or RGBA.")

    width, height = carrier_image.size
    total_bits = width * height * 3
    max_bytes = total_bits // 8
    safe_bytes = int(max_bytes * SAFE_CAPACITY_RATIO)

    return max_bytes, safe_bytes


def payload_fits(carrier_image: Image.Image, payload_size_bytes: int) -> bool:
    """
    Checks whether a payload of given size can fit into the carrier image.

    :param carrier_image: PIL Image object.
    :param payload_size_bytes: Total size of the payload in bytes.
    :return: True if the payload fits, False otherwise.
    """
    max_bytes, _ = calculate_carrier_capacity(carrier_image)
    return payload_size_bytes <= max_bytes