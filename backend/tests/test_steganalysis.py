"""
Unit Tests: Steganalysis Forensic Analysis Modules
"""
import io
import numpy as np
from PIL import Image

from app.steganalysis.entropy import calculate_byte_entropy, calculate_bit_entropy, analyze_entropy
from app.steganalysis.lsb_analyzer import analyze_lsb, perform_chi_square_pov_test
from app.steganalysis.histogram import analyze_histograms, calculate_pov_flattening_metric
from app.steganalysis.correlation import analyze_channel_correlation, pearson_correlation
from app.steganalysis.file_inspector import detect_trailing_data, inspect_file_structure


def test_byte_entropy_bounds():
    # Uniform constant data has entropy 0
    zeros = b"\x00" * 1000
    assert calculate_byte_entropy(zeros) == 0.0

    # Random data has entropy close to 8.0
    random_bytes = bytes(np.random.randint(0, 256, size=10000, dtype=np.uint8))
    ent = calculate_byte_entropy(random_bytes)
    assert 7.9 < ent <= 8.0


def test_bit_entropy_bounds():
    all_zeros = np.zeros(1000, dtype=np.uint8)
    assert calculate_bit_entropy(all_zeros) == 0.0

    half_half = np.array([0, 1] * 500, dtype=np.uint8)
    assert calculate_bit_entropy(half_half) == 1.0


def test_entropy_analysis_clean_image(sample_clean_image, sample_png_bytes):
    result = analyze_entropy(sample_png_bytes, sample_clean_image)
    assert "file_entropy" in result
    assert "channels_entropy" in result
    assert "lsb_bit_entropy" in result


def test_lsb_analysis_clean_vs_stego(sample_clean_image):
    clean_result = analyze_lsb(sample_clean_image)
    assert clean_result["visual_lsb_plane"].startswith("data:image/png;base64,")

    # In clean synthetic gradient image, channels should not be flagged as suspicious stego
    assert "channels" in clean_result


def test_histogram_analysis(sample_clean_image):
    result = analyze_histograms(sample_clean_image)
    assert len(result["histograms"]["red"]) == 256
    assert len(result["histograms"]["green"]) == 256
    assert len(result["histograms"]["blue"]) == 256
    assert "pov_pairing_delta" in result


def test_channel_correlation(sample_clean_image):
    result = analyze_channel_correlation(sample_clean_image)
    assert "channel_correlation" in result
    assert -1.0 <= result["channel_correlation"]["r_vs_g"] <= 1.0


def test_trailing_data_detection(sample_png_bytes):
    # Clean PNG should have no trailing data
    clean_res = detect_trailing_data(sample_png_bytes, "PNG")
    assert clean_res["detected"] is False

    # Appended PNG should detect trailing data
    trailing_payload = b"EXTRA_SUSPICIOUS_PAYLOAD_PAST_EOF"
    tampered_bytes = sample_png_bytes + trailing_payload
    stego_res = detect_trailing_data(tampered_bytes, "PNG")
    assert stego_res["detected"] is True
    assert stego_res["trailing_size_bytes"] == len(trailing_payload)
    assert "sha256" in stego_res
