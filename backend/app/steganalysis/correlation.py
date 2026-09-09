"""
Channel Correlation Steganalysis Module
Computes Pearson correlation coefficients across full color channels and LSB bit planes.
"""
import numpy as np
from PIL import Image
from typing import Dict, Any


def pearson_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Computes Pearson correlation coefficient between two 1D numeric arrays."""
    x_f = x.astype(np.float64).flatten()
    y_f = y.astype(np.float64).flatten()

    std_x = np.std(x_f)
    std_y = np.std(y_f)

    if std_x == 0 or std_y == 0:
        return 1.0  # Constant channel

    cov = np.cov(x_f, y_f)[0, 1]
    r = cov / (std_x * std_y)
    return float(np.clip(r, -1.0, 1.0))


def analyze_channel_correlation(img: Image.Image) -> Dict[str, Any]:
    """
    Evaluates:
    1. Macro channel correlation (R vs G, R vs B, G vs B)
    2. Micro LSB bit-plane correlation
    """
    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # Full channel correlations
    r_g = round(pearson_correlation(r, g), 4)
    r_b = round(pearson_correlation(r, b), 4)
    g_b = round(pearson_correlation(g, b), 4)

    # LSB plane correlations
    r_lsb = r & 1
    g_lsb = g & 1
    b_lsb = b & 1

    r_g_lsb = round(pearson_correlation(r_lsb, g_lsb), 4)
    r_b_lsb = round(pearson_correlation(r_lsb, b_lsb), 4)
    g_b_lsb = round(pearson_correlation(g_lsb, b_lsb), 4)

    # In natural images, full channels usually have correlation > 0.70.
    # Uncorrelated LSB planes (< 0.05) combined with high full channel correlation
    # is characteristic of independent pseudo-random noise insertion.
    is_anomaly = min(r_g, r_b, g_b) < 0.35 or (max(abs(r_g_lsb), abs(r_b_lsb), abs(g_b_lsb)) < 0.01)

    return {
        "channel_correlation": {
            "r_vs_g": r_g,
            "r_vs_b": r_b,
            "g_vs_b": g_b,
        },
        "lsb_plane_correlation": {
            "r_vs_g": r_g_lsb,
            "r_vs_b": r_b_lsb,
            "g_vs_b": g_b_lsb,
        },
        "is_correlation_anomaly": is_anomaly,
        "evaluation": (
            "Inter-channel LSB decorrelation detected, consistent with independent noise or encrypted data streams."
            if is_anomaly else
            "Channel correlation levels reflect typical natural color relationships."
        )
    }
