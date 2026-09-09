"""
Dataset Tests: Verifies all 7 safe synthetic test images generated in test_data/
"""
from pathlib import Path
from PIL import Image
from app.steganalysis.service import perform_forensic_analysis
from app.steganography.decoder import extract_payload_from_image, detect_stegovault_payload
from app.core.exceptions import (
    AuthenticationFailedError,
    CorruptedPayloadError,
    InvalidPayloadError,
)

DATASET_DIR = Path(__file__).resolve().parent.parent.parent / "test_data"
TEST_PASSWORD = "StegoVaultTestPassword2026!"


def test_normal_png():
    path = DATASET_DIR / "normal.png"
    assert path.exists()
    data = path.read_bytes()
    img = Image.open(path)
    report = perform_forensic_analysis(data, img, "normal.png")
    assert report["section_10_risk_score"]["score"] <= 40
    assert report["section_10_risk_score"]["risk_level"] in ("VERY_LOW", "LOW")
    assert report["section_8_structural_analysis"]["trailing_data"]["detected"] is False


def test_stego_low_png():
    path = DATASET_DIR / "stego_low.png"
    assert path.exists()
    img = Image.open(path)
    detection = detect_stegovault_payload(img)
    assert detection["detected"] is True

    plaintext, meta = extract_payload_from_image(img, TEST_PASSWORD)
    assert "Agent 007" in plaintext
    assert meta["integrity_verified"] is True


def test_stego_medium_png():
    path = DATASET_DIR / "stego_medium.png"
    assert path.exists()
    img = Image.open(path)
    plaintext, meta = extract_payload_from_image(img, TEST_PASSWORD)
    assert "Incident Report" in plaintext
    assert meta["integrity_verified"] is True


def test_stego_high_png():
    path = DATASET_DIR / "stego_high.png"
    assert path.exists()
    data = path.read_bytes()
    img = Image.open(path)
    report = perform_forensic_analysis(data, img, "stego_high.png")
    # StegoVault detected + elevated LSB density -> High/Critical risk
    assert report["section_10_risk_score"]["score"] >= 80
    assert report["section_10_risk_score"]["risk_level"] in ("HIGH", "CRITICAL")


def test_corrupted_png():
    path = DATASET_DIR / "corrupted.png"
    assert path.exists()
    img = Image.open(path)
    # Tampered LSB bits must fail either header magic/CRC or tag verification
    try:
        extract_payload_from_image(img, TEST_PASSWORD)
        assert False, "Should have failed on corrupted image"
    except (InvalidPayloadError, AuthenticationFailedError, CorruptedPayloadError):
        pass  # Expected


def test_metadata_test_png():
    path = DATASET_DIR / "metadata_test.png"
    assert path.exists()
    data = path.read_bytes()
    img = Image.open(path)
    report = perform_forensic_analysis(data, img, "metadata_test.png")
    meta = report["section_3_metadata_analysis"]
    assert meta["has_exif"] or len(meta["png_text_chunks"]) > 0


def test_trailing_data_test_png():
    path = DATASET_DIR / "trailing_data_test.png"
    assert path.exists()
    data = path.read_bytes()
    img = Image.open(path)
    report = perform_forensic_analysis(data, img, "trailing_data_test.png")
    trailing = report["section_8_structural_analysis"]["trailing_data"]
    assert trailing["detected"] is True
    assert trailing["trailing_size_bytes"] > 0
    assert report["section_10_risk_score"]["score"] >= 30
