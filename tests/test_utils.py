"""
StegoVault - Utilities Unit Tests
Validates input validation, cryptographic hashing, and image compatibility utilities.
"""

import pytest
from PIL import Image

from utils.hashing import compute_sha256, verify_sha256
from utils.image_utils import get_pixel_data
from utils.validation import validate_carrier_image, validate_passphrase


# --- 1. Carrier Image Validation Tests ---

def test_validate_carrier_image_valid_rgb():
    """Verify in-memory valid RGB image passes validation."""
    img = Image.new("RGB", (50, 50), color=(100, 150, 200))
    validate_carrier_image(img)


def test_validate_carrier_image_valid_rgba():
    """Verify in-memory valid RGBA image passes validation."""
    img = Image.new("RGBA", (50, 50), color=(100, 150, 200, 255))
    validate_carrier_image(img)


def test_validate_carrier_image_allowed_formats():
    """Verify allowed formats (PNG, BMP, TIFF) pass validation."""
    for fmt in ("PNG", "BMP", "TIFF"):
        img = Image.new("RGB", (20, 20))
        img.format = fmt
        validate_carrier_image(img)


def test_validate_carrier_image_forbidden_lossy_formats():
    """Verify lossy formats (JPEG, JPG, WEBP) are strictly rejected."""
    for fmt in ("JPEG", "JPG", "WEBP", "jpeg"):
        img = Image.new("RGB", (20, 20))
        img.format = fmt
        with pytest.raises(ValueError, match="Lossy image format"):
            validate_carrier_image(img)


def test_validate_carrier_image_unsupported_formats():
    """Verify unrecognized non-lossy formats are rejected."""
    img = Image.new("RGB", (20, 20))
    img.format = "GIF"
    with pytest.raises(ValueError, match="Unsupported image format"):
        validate_carrier_image(img)


def test_validate_carrier_image_unsupported_modes():
    """Verify non-RGB/RGBA modes (Grayscale 'L', 'CMYK', 'P') are rejected."""
    for mode in ("L", "CMYK", "P", "1"):
        img = Image.new(mode, (20, 20))
        with pytest.raises(ValueError, match="Unsupported image mode"):
            validate_carrier_image(img)


def test_validate_carrier_image_invalid_dimensions():
    """Verify zero or negative dimensions are rejected."""
    img = Image.new("RGB", (10, 10))
    img._size = (0, 10)
    with pytest.raises(ValueError, match="Invalid image dimensions"):
        validate_carrier_image(img)

    img._size = (10, -5)
    with pytest.raises(ValueError, match="Invalid image dimensions"):
        validate_carrier_image(img)


# --- 2. Passphrase Validation Tests ---

def test_validate_passphrase_valid():
    """Verify valid string and byte passphrases pass."""
    validate_passphrase("secure_password_123")
    validate_passphrase(b"byte_password_456")
    validate_passphrase(bytearray(b"bytearray_password"))


def test_validate_passphrase_empty():
    """Verify empty passphrases raise ValueError."""
    with pytest.raises(ValueError, match="Passphrase cannot be empty"):
        validate_passphrase("")

    with pytest.raises(ValueError, match="Passphrase cannot be empty"):
        validate_passphrase(b"")


def test_validate_passphrase_invalid_type():
    """Verify non-string/non-byte types raise TypeError."""
    with pytest.raises(TypeError, match="Passphrase must be a string or byte sequence"):
        validate_passphrase(12345)

    with pytest.raises(TypeError, match="Passphrase must be a string or byte sequence"):
        validate_passphrase(None)

    with pytest.raises(TypeError, match="Passphrase must be a string or byte sequence"):
        validate_passphrase(["password"])


# --- 3. Hashing Utility Tests ---

def test_compute_sha256_known_vector():
    """Verify SHA-256 calculation matches standard test vector."""
    # SHA-256 of empty bytes
    assert compute_sha256(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    # Known string hash
    expected = "4ba3ac44710702efa09e89e191f753c223ddc500dc07a80f79197880646be0e5"
    assert compute_sha256(b"StegoVault") == expected


def test_verify_sha256_matching_and_mismatch():
    """Verify SHA-256 verification returns True on match and False on mismatch."""
    data = b"Verify Integrity Payload"
    digest = compute_sha256(data)

    assert verify_sha256(data, digest) is True
    assert verify_sha256(data, digest.upper()) is True  # Case insensitive
    assert verify_sha256(data, "0" * 64) is False
    assert verify_sha256(b"Altered Data", digest) is False


# --- 4. Image Compatibility Utility Tests ---

def test_get_pixel_data_rgb():
    """Verify get_pixel_data returns all pixel tuples correctly for RGB images."""
    img = Image.new("RGB", (4, 4), color=(10, 20, 30))
    pixels = list(get_pixel_data(img))
    assert len(pixels) == 16
    assert pixels[0] == (10, 20, 30)


def test_get_pixel_data_rgba():
    """Verify get_pixel_data returns all pixel tuples correctly for RGBA images."""
    img = Image.new("RGBA", (3, 3), color=(50, 60, 70, 200))
    pixels = list(get_pixel_data(img))
    assert len(pixels) == 9
    assert pixels[0] == (50, 60, 70, 200)
