"""
StegoVault - LSB Unit Tests
Validates bit injection, extraction, channel mask preservation,
mode support (RGB/RGBA), and boundary conditions.
"""

import pytest
from PIL import Image

from core.exceptions import InsufficientCapacityError
from stego.lsb import embed_lsb, extract_lsb


@pytest.fixture
def sample_rgb_image() -> Image.Image:
    """Creates a simple 10x10 RGB image with known baseline pixel values."""
    img = Image.new("RGB", (10, 10), color=(128, 128, 128))
    return img


@pytest.fixture
def sample_rgba_image() -> Image.Image:
    """Creates a simple 10x10 RGBA image with an opaque alpha channel."""
    img = Image.new("RGBA", (10, 10), color=(128, 128, 128, 255))
    return img


def test_embed_and_extract_exact_round_trip_rgb(sample_rgb_image):
    """Verify raw bytes can be embedded into RGB and extracted identically."""
    payload = b"StegoVault LSB Test Payload"
    stego_img = embed_lsb(sample_rgb_image, payload)
    recovered = extract_lsb(stego_img, len(payload))

    assert recovered == payload


def test_embed_and_extract_exact_round_trip_rgba(sample_rgba_image):
    """Verify raw bytes can be embedded into RGBA and extracted identically."""
    payload = b"RGBA Carrier Test Data 12345"
    stego_img = embed_lsb(sample_rgba_image, payload)
    recovered = extract_lsb(stego_img, len(payload))

    assert recovered == payload


def test_alpha_channel_unmodified_in_rgba(sample_rgba_image):
    """Verify embedding in RGBA preserves the alpha channel completely."""
    payload = b"Preserve Alpha Channel"
    stego_img = embed_lsb(sample_rgba_image, payload)

    orig_alpha = [p[3] for p in sample_rgba_image.getdata()]
    stego_alpha = [p[3] for p in stego_img.getdata()]

    assert orig_alpha == stego_alpha


def test_empty_payload_round_trip(sample_rgb_image):
    """Verify zero-byte payloads can be embedded and extracted without error."""
    payload = b""
    stego_img = embed_lsb(sample_rgb_image, payload)
    recovered = extract_lsb(stego_img, 0)

    assert recovered == b""


def test_binary_data_round_trip(sample_rgb_image):
    """Verify arbitrary high-entropy bytes survive bitwise packing intact."""
    import os
    payload = os.urandom(30)
    stego_img = embed_lsb(sample_rgb_image, payload)
    recovered = extract_lsb(stego_img, len(payload))

    assert recovered == payload


def test_capacity_exact_limit_fits():
    """Verify embedding at exact carrier boundary succeeds."""
    # 4x2 image = 8 pixels = 24 RGB channels = 3 bytes capacity
    small_img = Image.new("RGB", (4, 2), color=(100, 100, 100))
    payload = b"ABC"
    stego_img = embed_lsb(small_img, payload)
    recovered = extract_lsb(stego_img, len(payload))

    assert recovered == payload


def test_capacity_overflow_raises_error():
    """Verify embedding beyond capacity raises InsufficientCapacityError."""
    # 2x2 image = 4 pixels = 12 channels = 1 byte capacity (12 bits >= 8 bits, 2 bytes = 16 bits)
    small_img = Image.new("RGB", (2, 2), color=(50, 50, 50))
    payload = b"AB"  # 16 bits > 12 bits

    with pytest.raises(InsufficientCapacityError):
        embed_lsb(small_img, payload)


def test_extraction_exceeding_capacity_raises_error(sample_rgb_image):
    """Verify attempting to extract more bytes than the carrier holds fails."""
    # 10x10 image = 100 pixels = 300 bits = 37 bytes capacity
    with pytest.raises(InsufficientCapacityError):
        extract_lsb(sample_rgb_image, 38)


def test_unsupported_image_mode_embedding():
    """Verify unsupported image formats (e.g., Grayscale 'L', CMYK) are rejected."""
    gray_img = Image.new("L", (10, 10), color=128)
    with pytest.raises(ValueError, match="Unsupported image mode"):
        embed_lsb(gray_img, b"data")


def test_unsupported_image_mode_extraction():
    """Verify extracting from unsupported image modes is rejected."""
    cmyk_img = Image.new("CMYK", (10, 10))
    with pytest.raises(ValueError, match="Unsupported image mode"):
        extract_lsb(cmyk_img, 4)


def test_image_dimensions_preserved_after_embedding(sample_rgb_image):
    """Verify image size and mode remain unchanged after embedding."""
    payload = b"Preserve dimensions"
    stego_img = embed_lsb(sample_rgb_image, payload)

    assert stego_img.size == sample_rgb_image.size
    assert stego_img.mode == sample_rgb_image.mode


def test_minimal_pixel_modification(sample_rgb_image):
    """Verify that only the LSBs are altered (delta between pixels <= 1 per channel)."""
    payload = b"Test"
    stego_img = embed_lsb(sample_rgb_image, payload)

    orig_pixels = list(sample_rgb_image.getdata())
    stego_pixels = list(stego_img.getdata())

    for (r1, g1, b1), (r2, g2, b2) in zip(orig_pixels, stego_pixels):
        assert abs(r1 - r2) <= 1
        assert abs(g1 - g2) <= 1
        assert abs(b1 - b2) <= 1