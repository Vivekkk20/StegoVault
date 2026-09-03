"""
StegoVault - Perceptual Fidelity and Error Metrics
Implements spatial difference algorithms including Mean Squared Error (MSE)
and Peak Signal-to-Noise Ratio (PSNR) to measure steganographic distortion.
"""

from __future__ import annotations

import math
from PIL import Image


def calculate_mse(image_a: Image.Image, image_b: Image.Image) -> float:
    """
    Computes Mean Squared Error (MSE) between two images across RGB channels.

    :param image_a: First PIL Image (RGB or RGBA).
    :param image_b: Second PIL Image (RGB or RGBA).
    :return: MSE float value (0.0 represents identical images).
    :raises ValueError: If image dimensions or modes do not match or are unsupported.
    """
    if image_a.size != image_b.size:
        raise ValueError("Images must have identical dimensions to calculate MSE.")

    if image_a.mode not in ("RGB", "RGBA") or image_b.mode not in ("RGB", "RGBA"):
        raise ValueError("Both images must be in RGB or RGBA mode.")

    pixels_a = list(image_a.convert("RGB").getdata())
    pixels_b = list(image_b.convert("RGB").getdata())

    total_squared_diff = 0
    total_components = len(pixels_a) * 3

    for (r1, g1, b1), (r2, g2, b2) in zip(pixels_a, pixels_b):
        total_squared_diff += (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

    return total_squared_diff / total_components


def calculate_psnr(image_a: Image.Image, image_b: Image.Image) -> float:
    """
    Computes Peak Signal-to-Noise Ratio (PSNR) in decibels (dB).

    :param image_a: First PIL Image.
    :param image_b: Second PIL Image.
    :return: PSNR float value in dB (returns float('inf') if MSE is zero).
    :raises ValueError: If image dimensions or modes do not match or are unsupported.
    """
    mse = calculate_mse(image_a, image_b)
    if mse == 0.0:
        return float("inf")

    max_pixel_val = 255.0
    return 10.0 * math.log10((max_pixel_val ** 2) / mse)