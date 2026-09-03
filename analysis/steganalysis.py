"""
StegoVault - Steganalysis and Anomaly Detection
Implements bit-plane decomposition (LSB plane extraction) and statistical
evaluation (Chi-Square attack) to assess steganographic detectability.
"""

from __future__ import annotations

import math
from PIL import Image


def extract_lsb_plane(image: Image.Image, channel_index: int = 0) -> Image.Image:
    """
    Extracts the least significant bit (bit 0) of the designated color channel
    and scales it to full binary contrast (0 -> 0, 1 -> 255) for visual inspection.

    :param image: PIL Image (RGB or RGBA).
    :param channel_index: Channel to inspect (0: Red, 1: Green, 2: Blue).
    :return: Grayscale PIL Image representing the LSB plane.
    :raises ValueError: If channel_index is invalid or image mode is unsupported.
    """
    if image.mode not in ("RGB", "RGBA"):
        raise ValueError(f"Unsupported image mode '{image.mode}'. Expected RGB or RGBA.")

    if channel_index not in (0, 1, 2):
        raise ValueError("Channel index must be 0 (Red), 1 (Green), or 2 (Blue).")

    rgb_image = image.convert("RGB")
    pixels = list(rgb_image.getdata())

    # Map LSB 0 -> 0 (Black), LSB 1 -> 255 (White)
    plane_data = [255 if (pixel[channel_index] & 1) else 0 for pixel in pixels]

    plane_image = Image.new("L", image.size)
    plane_image.putdata(plane_data)
    return plane_image


def chi_square_attack(image: Image.Image) -> tuple[float, float]:
    """
    Performs a standard Chi-Square (χ²) statistical attack on the spatial domain
    Pairs of Values (PoVs) across color channels.

    Sequential LSB embedding equalizes adjacent frequencies (2k and 2k+1).
    A p-value < 0.05 indicates a statistically significant anomaly
    consistent with artificial LSB replacement.

    :param image: PIL Image (RGB or RGBA).
    :return: (p_value, chi_square_statistic)
    :raises ValueError: If image mode is unsupported.
    """
    if image.mode not in ("RGB", "RGBA"):
        raise ValueError(f"Unsupported image mode '{image.mode}'. Expected RGB or RGBA.")

    rgb_image = image.convert("RGB")
    pixels = list(rgb_image.getdata())

    # Build histogram across all RGB pixel components (0 to 255)
    histogram = [0] * 256
    for r, g, b in pixels:
        histogram[r] += 1
        histogram[g] += 1
        histogram[b] += 1

    chi_stat = 0.0
    degrees_of_freedom = 0

    # Evaluate Pairs of Values: (0, 1), (2, 3), ..., (254, 255)
    for k in range(0, 256, 2):
        count_even = histogram[k]
        count_odd = histogram[k + 1]
        pair_sum = count_even + count_odd

        # Only evaluate bins with sufficient observations
        if pair_sum > 0:
            expected = pair_sum / 2.0
            chi_stat += ((count_even - expected) ** 2) / expected
            chi_stat += ((count_odd - expected) ** 2) / expected
            degrees_of_freedom += 1

    degrees_of_freedom = max(degrees_of_freedom - 1, 1)

    # Upper incomplete gamma / chi-square survival approximation
    p_value = _chi_square_survival(chi_stat, degrees_of_freedom)

    return p_value, chi_stat


def _chi_square_survival(x: float, df: int) -> float:
    """
    Approximates the survival function P(X >= x) for a chi-square distribution
    with degrees of freedom `df` using the Wilson-Hilferty transformation.
    """
    if x <= 0.0:
        return 1.0

    s = 2.0 / (9.0 * df)
    z = (((x / df) ** (1.0 / 3.0)) - (1.0 - s)) / math.sqrt(s)

    # Standard normal complementary CDF approximation: 0.5 * erfc(z / sqrt(2))
    return 0.5 * math.erfc(z / math.sqrt(2.0))