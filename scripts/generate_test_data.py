"""
Synthetic Test Data Generator for StegoVault
Generates 7 safe, synthetic test images for unit, integration, and security testing:
1. normal.png (Clean cover image with natural gradients)
2. stego_low.png (Low-density LSB payload)
3. stego_medium.png (Medium-density LSB payload)
4. stego_high.png (High-density LSB payload near capacity)
5. corrupted.png (Corrupted stego payload bytes causing tamper detection)
6. metadata_test.png (Image containing custom forensic metadata chunks)
7. trailing_data_test.png (Image containing unauthorized binary payload past EOF)
"""
import io
import struct
import zlib
import numpy as np
from PIL import Image, PngImagePlugin
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "test_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import backend modules
import sys
sys.path.insert(0, str(ROOT_DIR / "backend"))

from app.steganography.encoder import embed_payload_into_image
from app.steganography.capacity import calculate_image_capacity

TEST_PASSWORD = "StegoVaultTestPassword2026!"


def create_base_synthetic_image(width: int = 300, height: int = 300) -> Image.Image:
    """Creates a smooth color gradient with geometric shapes to simulate natural photography."""
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    xx, yy = np.meshgrid(x, y)

    r = (np.sin(xx * np.pi) * 200 + 40).astype(np.uint8)
    g = (np.cos(yy * np.pi) * 180 + 50).astype(np.uint8)
    b = ((xx + yy) / 2.0 * 220 + 30).astype(np.uint8)

    arr = np.dstack((r, g, b))
    return Image.fromarray(arr, mode="RGB")


def generate_all_test_data():
    print(f"Generating synthetic test dataset in: {OUTPUT_DIR}")

    # 1. normal.png
    base_img = create_base_synthetic_image(300, 300)
    normal_path = OUTPUT_DIR / "normal.png"
    base_img.save(normal_path, format="PNG")
    print(f" [+] Generated {normal_path.name}")

    # 2. stego_low.png (small message: ~40 chars)
    low_msg = "StegoVault confidential test dispatch: Agent 007 online."
    stego_low_img, meta_low = embed_payload_into_image(
        base_img, low_msg, TEST_PASSWORD, compress=True
    )
    low_path = OUTPUT_DIR / "stego_low.png"
    stego_low_img.save(low_path, format="PNG")
    print(f" [+] Generated {low_path.name} (Utilization: {meta_low['capacity_utilization']}%)")

    # 3. stego_medium.png (medium message: ~1.5 KB)
    medium_msg = (
        "StegoVault Forensic Incident Report:\n"
        "Security incident #2026-09-09. Multiple unauthenticated extraction attempts "
        "detected against sensitive telemetry endpoints. Cryptographic verification "
        "confirmed zero data leakage. All perimeter guards operational.\n" * 6
    )
    stego_med_img, meta_med = embed_payload_into_image(
        base_img, medium_msg, TEST_PASSWORD, compress=True
    )
    med_path = OUTPUT_DIR / "stego_medium.png"
    stego_med_img.save(med_path, format="PNG")
    print(f" [+] Generated {med_path.name} (Utilization: {meta_med['capacity_utilization']}%)")

    # 4. stego_high.png (dense payload: ~20 KB to trigger high LSB density)
    high_msg = ("CRITICAL FORENSIC DATA STREAM " + "0123456789ABCDEF" * 64 + "\n") * 18
    stego_high_img, meta_high = embed_payload_into_image(
        base_img, high_msg, TEST_PASSWORD, compress=False
    )
    high_path = OUTPUT_DIR / "stego_high.png"
    stego_high_img.save(high_path, format="PNG")
    print(f" [+] Generated {high_path.name} (Utilization: {meta_high['capacity_utilization']}%)")

    # 5. corrupted.png (stego image with bit-flips in payload area causing CRC/tag failure)
    corrupted_arr = np.array(stego_med_img, copy=True)
    # Tamper with LSB bits in first 50 pixels
    corrupted_arr[:10, :5, 0] ^= 1
    corrupted_img = Image.fromarray(corrupted_arr, mode="RGB")
    corrupted_path = OUTPUT_DIR / "corrupted.png"
    corrupted_img.save(corrupted_path, format="PNG")
    print(f" [+] Generated {corrupted_path.name} (Tampered LSB bits)")

    # 6. metadata_test.png (image with embedded tEXt / comment metadata)
    meta_info = PngImagePlugin.PngInfo()
    meta_info.add_text("Author", "StegoVault Forensic Lab")
    meta_info.add_text("Classification", "SECRET//NOFORN")
    meta_info.add_text("UserComment", "Forensic analysis target with custom non-standard chunk tags.")
    meta_path = OUTPUT_DIR / "metadata_test.png"
    base_img.save(meta_path, format="PNG", pnginfo=meta_info)
    print(f" [+] Generated {meta_path.name} (Custom PNG chunks)")

    # 7. trailing_data_test.png (valid PNG followed by appended secret payload)
    buf = io.BytesIO()
    base_img.save(buf, format="PNG")
    clean_bytes = buf.getvalue()
    
    trailing_payload = (
        b"\n\n=========================================\n"
        b"STEGOVAULT FORENSIC EXTRACTION TARGET:\n"
        b"CONFIDENTIAL APPENDED CIPHERTEXT DUMP\n"
        b"=========================================\n"
        b"OFFSET: PAST_IEND_CHUNK_EOF\n"
    )
    trailing_bytes = clean_bytes + trailing_payload
    trailing_path = OUTPUT_DIR / "trailing_data_test.png"
    with open(trailing_path, "wb") as f:
        f.write(trailing_bytes)
    print(f" [+] Generated {trailing_path.name} (Appended {len(trailing_payload)} bytes past EOF)")

    print("\nDataset generation completed successfully.")


if __name__ == "__main__":
    generate_all_test_data()
