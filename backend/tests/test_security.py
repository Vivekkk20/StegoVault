"""
Security Tests: File Security, Magic Bytes, Malformed Data & Path Traversal
"""
import pytest
from app.security.validation import validate_image_safe, detect_and_validate_format, validate_file_size
from app.security.sanitization import sanitize_filename
from app.core.exceptions import (
    FileTooLargeError,
    UnsupportedFormatError,
    FileSecurityError,
)


def test_magic_byte_validation_fake_extension():
    # File named image.png but containing ASCII text
    fake_png = b"This is plain text pretending to be a PNG image."
    with pytest.raises(UnsupportedFormatError):
        detect_and_validate_format(fake_png)


def test_magic_byte_validation_jpeg_rejected():
    # JPEG magic bytes \xFF\xD8\xFF
    fake_jpeg = b"\xFF\xD8\xFF\xE0\x00\x10JFIF"
    with pytest.raises(UnsupportedFormatError):
        detect_and_validate_format(fake_jpeg)


def test_oversized_file_rejected():
    # 25MB buffer
    huge_data = b"0" * (25 * 1024 * 1024)
    with pytest.raises(FileTooLargeError):
        validate_file_size(huge_data)


def test_malformed_image_rejected_safely():
    # PNG signature followed by corrupted random garbage
    malformed_png = b"\x89PNG\r\n\x1a\n" + b"\xFF" * 100
    with pytest.raises(FileSecurityError):
        validate_image_safe(malformed_png)


def test_path_traversal_sanitization():
    # Attacking with path traversal filenames
    dangerous_names = [
        "../../../../etc/passwd",
        "..\\..\\windows\\system32\\cmd.exe",
        "nested/dir/stego.png",
        "../../../secret.bmp",
        "<script>alert(1)</script>.png",
        "normal_name.png",
    ]

    for d in dangerous_names:
        clean = sanitize_filename(d)
        assert "/" not in clean
        assert "\\" not in clean
        assert ".." not in clean
        assert clean.endswith(".png") or clean.endswith(".bmp")
