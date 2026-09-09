"""
StegoVault - Image Compatibility Utilities
Provides unified pixel extraction across Pillow versions without deprecation warnings.
"""

from __future__ import annotations

from typing import Any, Sequence
from PIL import Image


def get_pixel_data(image: Image.Image) -> Sequence[Any]:
    """
    Returns pixel data for a PIL Image in a way that is compatible across Pillow versions.
    Uses Image.get_flattened_data() if available (Pillow 11.1+ / 12+) to avoid
    DeprecationWarning, falling back to Image.getdata() on older releases.
    """
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()
