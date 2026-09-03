"""
StegoVault - Image Analysis & Steganalysis Unit Tests
Validates MSE, PSNR, LSB plane decomposition, and Chi-Square statistical attacks.
"""

import pytest
from PIL import Image

from analysis.image_quality import calculate_mse, calculate_psnr
from analysis.steganalysis import chi_square_attack, extract_lsb_plane


@pytest.fixture
def base_rgb_image() -> Image.Image:
    """Creates a deterministic 20x20 RGB image."""
    img = Image.new("RGB", (20, 20), color=(100, 150, 200))
    return img


@pytest.fixture
def base_rgba_image() -> Image.Image:
    """Creates a deterministic 20x20 RGBA image."""
    img = Image.new("RGBA", (20, 20), color=(100, 150, 200, 255))
    return img


# --- 1. Image Quality Metrics (MSE & PSNR) ---

def test_mse_identical_images(base_rgb_image):
    """Verify MSE between identical images is strictly 0.0."""
    identical = base_rgb_image.copy()
    assert calculate_mse(base_rgb_image, identical) == 0.0


def test_psnr_identical_images(base_rgb_image):
    """Verify PSNR of identical images evaluates to infinity."""
    identical = base_rgb_image.copy()
    assert calculate_psnr(base_rgb_image, identical) == float("inf")


def test_mse_known_deviation(base_rgb_image):
    """Verify exact MSE calculation against a known manual pixel perturbation."""
    modified = base_rgb_image.copy()
    pixels = list(modified.getdata())
    # Modify exactly one channel of one pixel by +2
    r, g, b = pixels[0]
    pixels[0] = (r + 2, g, b)
    modified.putdata(pixels)

    # MSE = (2^2) / (20 * 20 * 3) = 4 / 1200 = 1/300
    expected_mse = 4.0 / (20 * 20 * 3)
    assert pytest.approx(calculate_mse(base_rgb_image, modified), rel=1e-5) == expected_mse


def test_psnr_known_deviation(base_rgb_image):
    """Verify PSNR calculation corresponds to expected logarithmic formula."""
    modified = base_rgb_image.copy()
    pixels = list(modified.getdata())
    r, g, b = pixels[0]
    pixels[0] = (r + 1, g, b)
    modified.putdata(pixels)

    mse = calculate_mse(base_rgb_image, modified)
    import math
    expected_psnr = 10.0 * math.log10((255.0 ** 2) / mse)
    assert pytest.approx(calculate_psnr(base_rgb_image, modified), rel=1e-5) == expected_psnr


def test_metrics_rgba_support(base_rgba_image):
    """Verify MSE and PSNR functions accept RGBA images seamlessly."""
    modified = base_rgba_image.copy()
    pixels = list(modified.getdata())
    r, g, b, a = pixels[0]
    pixels[0] = (r + 1, g, b, a)
    modified.putdata(pixels)

    mse = calculate_mse(base_rgba_image, modified)
    assert mse > 0.0
    psnr = calculate_psnr(base_rgba_image, modified)
    assert psnr < float("inf")


def test_metrics_dimension_mismatch_raises():
    """Verify dimensional inequality between carriers raises ValueError."""
    img1 = Image.new("RGB", (10, 10))
    img2 = Image.new("RGB", (10, 12))
    with pytest.raises(ValueError, match="identical dimensions"):
        calculate_mse(img1, img2)

    with pytest.raises(ValueError, match="identical dimensions"):
        calculate_psnr(img1, img2)


def test_metrics_unsupported_mode_raises():
    """Verify unsupported color spaces (e.g., Grayscale 'L') raise ValueError."""
    img1 = Image.new("L", (10, 10))
    img2 = Image.new("L", (10, 10))
    with pytest.raises(ValueError, match="RGB or RGBA mode"):
        calculate_mse(img1, img2)


# --- 2. LSB Plane Extraction ---

def test_extract_lsb_plane_dimensions_and_mode(base_rgb_image):
    """Verify extracted LSB plane preserves dimensions and outputs grayscale ('L')."""
    plane = extract_lsb_plane(base_rgb_image, channel_index=0)
    assert plane.size == base_rgb_image.size
    assert plane.mode == "L"


def test_extract_lsb_plane_channel_values():
    """Verify bit 0 extraction scales strictly to 0 and 255 binary values."""
    img = Image.new("RGB", (2, 1))
    # Pixel 0: R=100 (LSB 0), Pixel 1: R=101 (LSB 1)
    img.putdata([(100, 0, 0), (101, 0, 0)])

    plane = extract_lsb_plane(img, channel_index=0)
    plane_pixels = list(plane.getdata())

    assert plane_pixels[0] == 0
    assert plane_pixels[1] == 255


def test_extract_lsb_plane_invalid_channel(base_rgb_image):
    """Verify invalid channel indices raise ValueError."""
    with pytest.raises(ValueError, match="Channel index must be 0"):
        extract_lsb_plane(base_rgb_image, channel_index=3)


def test_extract_lsb_plane_unsupported_mode():
    """Verify non-RGB/RGBA modes are rejected."""
    gray_img = Image.new("L", (10, 10))
    with pytest.raises(ValueError, match="Unsupported image mode"):
        extract_lsb_plane(gray_img, channel_index=0)


# --- 3. Chi-Square Steganalysis ---

def test_chi_square_output_structure(base_rgb_image):
    """Verify Chi-Square returns a tuple of two valid numeric floats (p_value, chi_stat)."""
    p_val, chi_stat = chi_square_attack(base_rgb_image)
    assert isinstance(p_val, float)
    assert isinstance(chi_stat, float)
    assert 0.0 <= p_val <= 1.0
    assert chi_stat >= 0.0


def test_chi_square_rgba_support(base_rgba_image):
    """Verify Chi-Square analysis operates on RGBA carriers without error."""
    p_val, chi_stat = chi_square_attack(base_rgba_image)
    assert isinstance(p_val, float)
    assert isinstance(chi_stat, float)


def test_chi_square_unsupported_mode():
    """Verify Chi-Square rejects unsupported color modes."""
    gray_img = Image.new("L", (10, 10))
    with pytest.raises(ValueError, match="Unsupported image mode"):
        chi_square_attack(gray_img)