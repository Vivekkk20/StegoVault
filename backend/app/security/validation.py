"""
Input Validation & File Security
Verifies file size, MIME types, and magic bytes to prevent malformed or malicious file execution.
"""
import io
from typing import Tuple
from PIL import Image

from app.core.exceptions import (
    FileSecurityError,
    FileTooLargeError,
    UnsupportedFormatError,
)
from app.config import settings

# Magic byte signatures
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
BMP_MAGIC = b"BM"

SUPPORTED_FORMATS = {"PNG", "BMP"}


def validate_file_size(data: bytes) -> None:
    """Verifies data does not exceed maximum upload size."""
    if len(data) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise FileTooLargeError(
            f"File size ({len(data)} bytes) exceeds maximum permitted limit "
            f"of {settings.MAX_UPLOAD_SIZE_BYTES} bytes ({settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB)."
        )


def detect_and_validate_format(data: bytes) -> str:
    """
    Validates magic bytes to ensure file is genuinely a PNG or BMP.
    Returns format string: 'PNG' or 'BMP'.
    """
    if data.startswith(PNG_MAGIC):
        return "PNG"
    elif data.startswith(BMP_MAGIC):
        return "BMP"
    else:
        raise UnsupportedFormatError(
            "Unsupported or invalid image format. "
            "Only lossless PNG and BMP images are supported. "
            "File header does not match expected magic bytes."
        )


def validate_image_safe(data: bytes) -> Tuple[Image.Image, str]:
    """
    Validates file size, magic bytes, and safely decodes image with Pillow.
    Ensures image is valid and not a decompression bomb or corrupted stream.
    """
    validate_file_size(data)
    img_format = detect_and_validate_format(data)

    try:
        # Pillow verify step
        with Image.open(io.BytesIO(data)) as test_img:
            test_img.verify()
        
        # Load image into memory safely
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception as e:
        raise FileSecurityError(f"Malformed or corrupted image file: {str(e)}")

    if img.format not in SUPPORTED_FORMATS and img_format not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(f"Image format {img.format} is not supported.")

    # Convert grayscale or other modes to RGB or RGBA for consistent steganography
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    return img, img_format
