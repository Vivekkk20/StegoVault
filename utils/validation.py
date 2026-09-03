"""
StegoVault - Input and Carrier Validation
Validates input types, enforces lossless image formats (PNG, BMP), rejects
lossy carriers (JPEG), and guards against invalid buffer dimensions.
"""

from __future__ import annotations

from PIL import Image

ALLOWED_IMAGE_MODES: set[str] = {"RGB", "RGBA"}
ALLOWED_IMAGE_FORMATS: set[str] = {"PNG", "BMP", "TIFF"}
FORBIDDEN_LOSSY_FORMATS: set[str] = {"JPEG", "JPG", "WEBP"}


def validate_carrier_image(image: Image.Image) -> None:
    """
    Validates carrier image suitability for LSB steganography.
    Enforces lossless formats and RGB/RGBA color modes.

    :param image: PIL Image instance to inspect.
    :raises ValueError: If the format is lossy, mode is unsupported, or dimensions are zero.
    """
    if image.format and image.format.upper() in FORBIDDEN_LOSSY_FORMATS:
        raise ValueError(
            f"Lossy image format '{image.format}' is strictly forbidden. "
            "Lossy compression destroys spatial LSB payload integrity. Use PNG or BMP."
        )

    if image.format and image.format.upper() not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(
            f"Unsupported image format '{image.format}'. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_IMAGE_FORMATS))}."
        )

    if image.mode not in ALLOWED_IMAGE_MODES:
        raise ValueError(
            f"Unsupported image mode '{image.mode}'. "
            f"Allowed color modes are: {', '.join(sorted(ALLOWED_IMAGE_MODES))}."
        )

    width, height = image.size
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid image dimensions: {width}x{height}.")


def validate_passphrase(passphrase: str | bytes) -> None:
    """
    Validates that the provided passphrase is non-empty and well-formed.

    :param passphrase: User-supplied passphrase (str or bytes).
    :raises ValueError: If passphrase is empty or invalid.
    :raises TypeError: If passphrase is of an unsupported type.
    """
    if not isinstance(passphrase, (str, bytes, bytearray)):
        raise TypeError("Passphrase must be a string or byte sequence.")

    if len(passphrase) == 0:
        raise ValueError("Passphrase cannot be empty.")