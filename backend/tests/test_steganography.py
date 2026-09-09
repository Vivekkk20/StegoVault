"""
Unit Tests: LSB Steganography Engine (Capacity, Encoding, Decoding)
"""
import pytest
from PIL import Image
import numpy as np

from app.steganography.capacity import calculate_image_capacity, evaluate_capacity_for_payload
from app.steganography.encoder import embed_payload_into_image
from app.steganography.decoder import extract_payload_from_image, detect_stegovault_payload
from app.core.exceptions import (
    InsufficientCapacityError,
    InvalidPayloadError,
    AuthenticationFailedError,
)


def test_capacity_calculation():
    img = Image.new("RGB", (100, 100))
    cap = calculate_image_capacity(img)
    # 100 * 100 * 3 bits = 30000 bits = 3750 bytes
    assert cap["capacity_bytes"] == 3750
    assert cap["capacity_bits"] == 30000


def test_capacity_evaluation_sufficient():
    img = Image.new("RGB", (100, 100))
    # 500 bytes message + 92 overhead < 3750 bytes
    eval_res = evaluate_capacity_for_payload(img, 500)
    assert eval_res["sufficient_capacity"] is True
    assert eval_res["status"] == "Sufficient capacity"


def test_capacity_evaluation_insufficient():
    img = Image.new("RGB", (10, 10))
    # 10*10*3 bits = 300 bits = 37 bytes. Message of 100 bytes cannot fit
    eval_res = evaluate_capacity_for_payload(img, 100)
    assert eval_res["sufficient_capacity"] is False
    assert eval_res["status"] == "Insufficient capacity"


def test_encode_insufficient_capacity_raises():
    tiny_img = Image.new("RGB", (5, 5))  # Only 9 bytes capacity
    with pytest.raises(InsufficientCapacityError):
        embed_payload_into_image(tiny_img, "This will never fit", "Password")


def test_encode_decode_roundtrip_rgb(sample_clean_image):
    original_arr = np.array(sample_clean_image)
    secret = "StegoVault Classified Mission Alpha 2026"
    password = "SuperStrongPassword987!"

    stego_img, meta = embed_payload_into_image(sample_clean_image, secret, password)
    assert meta["payload_bytes"] > 0

    # Ensure original image object is not mutated
    assert np.array_equal(np.array(sample_clean_image), original_arr)

    # Detect payload
    detection = detect_stegovault_payload(stego_img)
    assert detection["detected"] is True
    assert detection["header_crc_valid"] is True

    # Decode
    extracted, dec_meta = extract_payload_from_image(stego_img, password)
    assert extracted == secret
    assert dec_meta["integrity_verified"] is True


def test_decode_wrong_password_fails(sample_clean_image):
    stego_img, _ = embed_payload_into_image(sample_clean_image, "Secret", "GoodPassword")
    with pytest.raises(AuthenticationFailedError):
        extract_payload_from_image(stego_img, "BadPassword")


def test_decode_clean_image_fails(sample_clean_image):
    with pytest.raises(InvalidPayloadError):
        extract_payload_from_image(sample_clean_image, "AnyPassword")
