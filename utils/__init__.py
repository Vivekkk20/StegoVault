"""
StegoVault - Utilities Package
Provides cryptographic hashing, input and carrier validation, and image compatibility helpers.

Modules:
    hashing: SHA-256 computation and constant-time integrity verification.
    validation: Lossless carrier format enforcement and passphrase validation.
    image_utils: Cross-version Pillow pixel data extraction avoiding deprecation warnings.
"""

from utils.hashing import compute_sha256, verify_sha256
from utils.image_utils import get_pixel_data
from utils.validation import validate_carrier_image, validate_passphrase

__all__ = [
    "compute_sha256",
    "verify_sha256",
    "get_pixel_data",
    "validate_carrier_image",
    "validate_passphrase",
]
