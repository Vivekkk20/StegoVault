"""
StegoVault - Integration and End-to-End Workflow Tests
Validates the complete pipeline: payload ingestion, compression, key derivation,
AES-256-GCM authenticated encryption, LSB embedding, extraction, authentication,
decryption, and decompression across image modes and edge conditions.
"""

import os
import pytest
from PIL import Image

from core.decoder import decode_payload
from core.encoder import encode_payload
from core.exceptions import (
    AuthenticationError,
    InsufficientCapacityError,
)
from core.payload import PAYLOAD_TYPE_BINARY, PAYLOAD_TYPE_TEXT


@pytest.fixture
def carrier_rgb_large() -> Image.Image:
    """100x100 RGB carrier image providing ~3,750 bytes capacity."""
    return Image.new("RGB", (100, 100), color=(70, 130, 180))


@pytest.fixture
def carrier_rgba_large() -> Image.Image:
    """100x100 RGBA carrier image with full opacity."""
    return Image.new("RGBA", (100, 100), color=(70, 130, 180, 255))


def test_text_round_trip(carrier_rgb_large):
    """Verify standard text payloads encode, embed, extract, and decrypt correctly."""
    passphrase = "CorrectMasterPassphrase!123"
    message = "StegoVault confidential transmission test string.".encode("utf-8")

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=message,
        passphrase=passphrase,
        payload_type=PAYLOAD_TYPE_TEXT,
    )

    recovered_data, recovered_type = decode_payload(stego_img, passphrase)

    assert recovered_type == PAYLOAD_TYPE_TEXT
    assert recovered_data == message


def test_unicode_text_round_trip(carrier_rgb_large):
    """Verify multibyte UTF-8 Unicode characters survive full pipeline execution."""
    passphrase = "UnicodeSecurePassphrase_🔐"
    unicode_text = "StegoVault 🔒 密碼學 • 🔐 • Проверка • 日本語テスト".encode("utf-8")

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=unicode_text,
        passphrase=passphrase,
        payload_type=PAYLOAD_TYPE_TEXT,
    )

    recovered_data, recovered_type = decode_payload(stego_img, passphrase)

    assert recovered_type == PAYLOAD_TYPE_TEXT
    assert recovered_data.decode("utf-8") == unicode_text.decode("utf-8")


def test_binary_file_round_trip(carrier_rgb_large):
    """Verify arbitrary high-entropy binary sequences survive intact."""
    passphrase = "BinaryKeyVerificationPassphrase"
    binary_data = os.urandom(512)

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=binary_data,
        passphrase=passphrase,
        payload_type=PAYLOAD_TYPE_BINARY,
    )

    recovered_data, recovered_type = decode_payload(stego_img, passphrase)

    assert recovered_type == PAYLOAD_TYPE_BINARY
    assert recovered_data == binary_data


def test_empty_payload_round_trip(carrier_rgb_large):
    """Verify zero-byte payloads can be compressed, encrypted, and recovered."""
    passphrase = "EmptyPayloadPassword"
    empty_payload = b""

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=empty_payload,
        passphrase=passphrase,
        payload_type=PAYLOAD_TYPE_TEXT,
    )

    recovered_data, recovered_type = decode_payload(stego_img, passphrase)

    assert recovered_type == PAYLOAD_TYPE_TEXT
    assert recovered_data == b""


def test_wrong_password_fails_safely(carrier_rgb_large):
    """Verify supplying an invalid passphrase triggers AuthenticationError without leakage."""
    correct_pass = "ValidPassphrase123"
    wrong_pass = "WrongPassphrase456"
    payload = b"Top secret data to be protected"

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=payload,
        passphrase=correct_pass,
        payload_type=PAYLOAD_TYPE_TEXT,
    )

    with pytest.raises(AuthenticationError):
        decode_payload(stego_img, wrong_pass)


def test_tampered_stego_image_fails_safely(carrier_rgb_large):
    """Verify altering even a single bit in the carrier triggers tag verification failure."""
    passphrase = "TamperDetectionPassword"
    payload = b"Critical operational instructions requiring integrity"

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=payload,
        passphrase=passphrase,
        payload_type=PAYLOAD_TYPE_TEXT,
    )

    # Flip LSB of first pixel in stego image
    pixel_list = list(stego_img.getdata())
    r, g, b = pixel_list[0]
    pixel_list[0] = (r ^ 1, g, b)

    tampered_img = Image.new("RGB", stego_img.size)
    tampered_img.putdata(pixel_list)

    with pytest.raises(AuthenticationError):
        decode_payload(tampered_img, passphrase)


def test_insufficient_image_capacity():
    """Verify attempting to embed into an undersized carrier raises InsufficientCapacityError."""
    passphrase = "CapacityCheckPassword"
    # Small 4x4 image = 16 pixels = 48 bits = 6 bytes capacity
    small_carrier = Image.new("RGB", (4, 4), color=(0, 0, 0))
    large_payload = b"Payload far too large to fit inside a tiny 4x4 image wire envelope"

    with pytest.raises(InsufficientCapacityError):
        encode_payload(
            carrier_image=small_carrier,
            payload=large_payload,
            passphrase=passphrase,
        )


def test_image_dimensions_and_mode_preserved(carrier_rgb_large):
    """Verify output stego carrier retains exact geometry and color profile."""
    passphrase = "GeometryPreservationPass"
    payload = b"Test metadata preservation"

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=payload,
        passphrase=passphrase,
    )

    assert stego_img.size == carrier_rgb_large.size
    assert stego_img.mode == carrier_rgb_large.mode


def test_rgb_carrier_round_trip(carrier_rgb_large):
    """Explicitly verify complete pipeline under 3-channel RGB mode."""
    passphrase = "RGBPassphraseVerification"
    payload = b"Payload stored strictly in RGB carrier channels"

    stego_img = encode_payload(
        carrier_image=carrier_rgb_large,
        payload=payload,
        passphrase=passphrase,
    )

    recovered_data, _ = decode_payload(stego_img, passphrase)
    assert recovered_data == payload


def test_rgba_carrier_round_trip(carrier_rgba_large):
    """Explicitly verify complete pipeline under 4-channel RGBA mode."""
    passphrase = "RGBAPassphraseVerification"
    payload = b"Payload stored strictly in RGBA carrier with untouched alpha"

    stego_img = encode_payload(
        carrier_image=carrier_rgba_large,
        payload=payload,
        passphrase=passphrase,
    )

    recovered_data, _ = decode_payload(stego_img, passphrase)
    assert recovered_data == payload
    assert stego_img.mode == "RGBA"