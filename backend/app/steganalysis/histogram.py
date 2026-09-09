"""
Histogram & Pair of Values (PoV) Steganalysis Module
Generates 256-bin RGB channel histograms and evaluates PoV flattening metrics.
"""
import numpy as np
from PIL import Image
from typing import Dict, Any, List


def calculate_channel_histogram(arr_channel: np.ndarray) -> List[int]:
    """Calculates 256-bin histogram counts for an 8-bit channel."""
    counts = np.bincount(arr_channel.flatten(), minlength=256)
    return counts.tolist()


def calculate_pov_flattening_metric(arr_channel: np.ndarray) -> float:
    """
    Measures the average relative difference between adjacent even/odd pairs (2k, 2k+1).
    Lower values indicate artificial equalization (LSB replacement steganography).
    """
    counts = np.bincount(arr_channel.flatten(), minlength=256)
    c_even = counts[0::2]
    c_odd = counts[1::2]
    
    pair_sums = c_even + c_odd
    valid_mask = pair_sums > 10
    
    if np.count_nonzero(valid_mask) == 0:
        return 1.0
        
    abs_diffs = np.abs(c_even[valid_mask] - c_odd[valid_mask])
    relative_diffs = abs_diffs / pair_sums[valid_mask]
    return float(np.mean(relative_diffs))


def analyze_histograms(img: Image.Image) -> Dict[str, Any]:
    """
    Analyzes histograms for Red, Green, Blue channels and overall luminance.
    """
    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb)

    r_hist = calculate_channel_histogram(arr[:, :, 0])
    g_hist = calculate_channel_histogram(arr[:, :, 1])
    b_hist = calculate_channel_histogram(arr[:, :, 2])

    # Luminance histogram (Rec. 601)
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)
    lum_hist = calculate_channel_histogram(lum)

    r_pov = round(calculate_pov_flattening_metric(arr[:, :, 0]), 4)
    g_pov = round(calculate_pov_flattening_metric(arr[:, :, 1]), 4)
    b_pov = round(calculate_pov_flattening_metric(arr[:, :, 2]), 4)

    # Anomaly indicator: PoV relative difference unusually low (< 0.04)
    is_anomaly = any(pov < 0.04 for pov in (r_pov, g_pov, b_pov))

    return {
        "histograms": {
            "red": r_hist,
            "green": g_hist,
            "blue": b_hist,
            "luminance": lum_hist,
        },
        "pov_pairing_delta": {
            "red": r_pov,
            "green": g_pov,
            "blue": b_pov,
        },
        "is_flattened_anomaly": is_anomaly,
        "evaluation": (
            "Adjacent histogram value pairs exhibit unnatural flattening, indicating possible LSB bit replacement."
            if is_anomaly else
            "Histogram distributions exhibit natural gradient transitions between adjacent pixel values."
        )
    }
