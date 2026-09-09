"""
Shannon Entropy Steganalysis Module
Calculates information entropy across raw file bytes, color channels, and LSB planes.
Theoretical range for 8-bit symbols: 0.0 to 8.0 bits/symbol.
Theoretical range for 1-bit LSB plane: 0.0 to 1.0 bit/symbol.
"""
import math
import numpy as np
from PIL import Image
from typing import Dict, Any, Union


def calculate_byte_entropy(data: Union[bytes, bytearray, np.ndarray]) -> float:
    """
    Computes Shannon entropy of an arbitrary byte sequence:
    H(X) = -sum(p(x) * log2(p(x)))
    """
    if len(data) == 0:
        return 0.0

    if isinstance(data, (bytes, bytearray)):
        arr = np.frombuffer(data, dtype=np.uint8)
    else:
        arr = data.flatten()

    counts = np.bincount(arr, minlength=256)
    probabilities = counts[counts > 0] / len(arr)
    return float(-np.sum(probabilities * np.log2(probabilities)))


def calculate_bit_entropy(bits: np.ndarray) -> float:
    """
    Computes Shannon entropy of a binary array (0s and 1s).
    Max theoretical entropy is 1.0 (perfectly random/encrypted).
    """
    if len(bits) == 0:
        return 0.0
    
    total = len(bits)
    count_1 = np.count_nonzero(bits)
    count_0 = total - count_1

    if count_0 == 0 or count_1 == 0:
        return 0.0

    p0 = count_0 / total
    p1 = count_1 / total
    return float(-(p0 * math.log2(p0) + p1 * math.log2(p1)))


def analyze_entropy(data: bytes, img: Image.Image) -> Dict[str, Any]:
    """
    Performs multi-layer entropy analysis:
    1. Overall raw file entropy
    2. Overall pixel array entropy
    3. Per-channel byte entropy (Red, Green, Blue, Alpha if present)
    4. Per-channel LSB bit-plane entropy
    """
    file_entropy = calculate_byte_entropy(data)

    img_rgb = img.convert("RGB") if img.mode not in ("RGB", "RGBA") else img
    arr = np.array(img_rgb)
    
    pixel_entropy = calculate_byte_entropy(arr)

    channel_names = ["red", "green", "blue"]
    if img.mode == "RGBA":
        channel_names.append("alpha")

    channels_entropy = {}
    lsb_entropy = {}
    suspicious_channels = []

    for i, ch_name in enumerate(channel_names):
        if i < arr.shape[2]:
            ch_data = arr[:, :, i]
            ch_ent = round(calculate_byte_entropy(ch_data), 4)
            channels_entropy[ch_name] = ch_ent

            # Extract LSB bit plane
            lsb_bits = (ch_data & 1).flatten()
            lsb_ent = round(calculate_bit_entropy(lsb_bits), 4)
            lsb_entropy[ch_name] = lsb_ent

            # In natural images, LSB entropy typically ranges from 0.70 to 0.96.
            # When encrypted/compressed data is embedded, LSB entropy rises towards ~0.995-1.000.
            if lsb_ent > 0.998 and ch_name != "alpha":
                suspicious_channels.append(ch_name)

    # Anomaly indicator evaluation
    is_lsb_anomaly = len(suspicious_channels) >= 2

    return {
        "file_entropy": round(file_entropy, 4),
        "pixel_entropy": round(pixel_entropy, 4),
        "channels_entropy": channels_entropy,
        "lsb_bit_entropy": lsb_entropy,
        "suspicious_channels": suspicious_channels,
        "is_lsb_anomaly": is_lsb_anomaly,
        "evaluation": (
            "Elevated LSB entropy detected in multiple color channels (~1.0 bit/symbol), "
            "consistent with high-entropy cryptographic or compressed embedded payloads."
            if is_lsb_anomaly else
            "LSB entropy levels are within expected statistical ranges for natural photography/graphics."
        )
    }
