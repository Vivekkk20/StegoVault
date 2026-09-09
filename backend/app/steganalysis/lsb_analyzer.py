"""
LSB Distribution, Chi-Square PoV Attack & Visual Bit-Plane Steganalysis
Implements statistical detection of LSB replacement via Westfeld-Pfitzmann Pairs of Values (PoVs)
and bit-plane visual forensic rendering.
"""
import io
import base64
import numpy as np
from PIL import Image
from scipy.stats import chi2
from typing import Dict, Any, List


def analyze_channel_lsb_distribution(channel_arr: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes the bit-plane distribution of 0s vs 1s in the LSB of a single channel.
    Encrypted data will force 1s ratio very close to 50.00%.
    """
    lsb_bits = (channel_arr & 1).flatten()
    total_bits = len(lsb_bits)
    count_1 = int(np.count_nonzero(lsb_bits))
    count_0 = total_bits - count_1

    ratio_1 = count_1 / total_bits if total_bits > 0 else 0.5
    pct_1 = round(ratio_1 * 100.0, 2)
    pct_0 = round((count_0 / total_bits) * 100.0, 2)
    
    # Deviation from pure randomness (50%)
    dev_from_half = abs(ratio_1 - 0.5)

    # Suspicious if deviation is extremely small (< 0.2% on reasonably sized image)
    # or if it exhibits flat randomness
    is_suspicious_uniform = dev_from_half < 0.0025 and total_bits > 10000

    return {
        "count_0": count_0,
        "count_1": count_1,
        "percentage_0": pct_0,
        "percentage_1": pct_1,
        "deviation_from_50": round(dev_from_half * 100.0, 3),
        "status": "Suspicious (High Uniformity)" if is_suspicious_uniform else "Normal",
    }


def perform_chi_square_pov_test(channel_arr: np.ndarray) -> Dict[str, Any]:
    """
    Westfeld-Pfitzmann Chi-Square test on Pairs of Values (PoVs: 2k and 2k+1).
    Calculates chi2 statistic and p-value.
    A low p-value (< 0.05) indicates artificial pairing equalization typical of LSB stego.
    """
    flat = channel_arr.flatten()
    counts = np.bincount(flat, minlength=256)

    chi2_stat = 0.0
    valid_pairs = 0

    for k in range(128):
        c_even = counts[2 * k]
        c_odd = counts[2 * k + 1]
        pair_sum = c_even + c_odd

        if pair_sum > 5:  # Sufficient frequency threshold
            # Expected frequency under LSB replacement
            e_k = pair_sum / 2.0
            chi2_stat += ((c_even - e_k) ** 2) / e_k
            valid_pairs += 1

    df = max(1, valid_pairs - 1)
    p_value = float(chi2.sf(chi2_stat, df=df)) if valid_pairs > 1 else 1.0

    # If p-value < 0.05 and chi2 is relatively low compared to expected degrees of freedom,
    # or if pairing deviation is flattened:
    is_stego_likely = p_value > 0.95 or p_value < 0.01

    return {
        "chi2_statistic": round(float(chi2_stat), 2),
        "degrees_of_freedom": df,
        "p_value": round(p_value, 6),
        "evaluated_pairs": valid_pairs,
        "is_suspicious": is_stego_likely,
        "status": "Suspicious" if is_stego_likely else "Normal",
    }


def generate_lsb_visual_plane(img: Image.Image) -> str:
    """
    Extracts the LSB bit-plane across RGB channels, scales bits to 0 or 255,
    and returns a base64-encoded PNG image for frontend visual forensic display.
    """
    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb)

    # Scale LSB (0 or 1) to full range (0 or 255)
    lsb_arr = ((arr & 1) * 255).astype(np.uint8)

    lsb_img = Image.fromarray(lsb_arr, mode="RGB")
    buf = io.BytesIO()
    lsb_img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def analyze_lsb(img: Image.Image) -> Dict[str, Any]:
    """
    Comprehensive LSB Steganalysis:
    1. Bit distribution for R, G, B, A
    2. Chi-Square PoV pairing test per channel
    3. Base64 Visual LSB Plane
    """
    img_rgb = img.convert("RGB") if img.mode not in ("RGB", "RGBA") else img
    arr = np.array(img_rgb)

    channels = ["red", "green", "blue"]
    if img.mode == "RGBA":
        channels.append("alpha")

    distribution_results = {}
    chi_square_results = {}
    suspicious_count = 0

    for i, ch_name in enumerate(channels):
        if i < arr.shape[2]:
            ch_data = arr[:, :, i]
            dist = analyze_channel_lsb_distribution(ch_data)
            distribution_results[ch_name] = dist

            if ch_name != "alpha":
                chi = perform_chi_square_pov_test(ch_data)
                chi_square_results[ch_name] = chi
                if chi["is_suspicious"] or dist["status"].startswith("Suspicious"):
                    suspicious_count += 1

    visual_plane_b64 = generate_lsb_visual_plane(img)

    return {
        "channels": {
            ch: {
                "distribution": distribution_results.get(ch),
                "chi_square": chi_square_results.get(ch),
                "status": "Suspicious" if (
                    (chi_square_results.get(ch, {}).get("is_suspicious", False)) or 
                    (distribution_results.get(ch, {}).get("status", "").startswith("Suspicious"))
                ) else "Normal",
            }
            for ch in channels
        },
        "suspicious_channels_count": suspicious_count,
        "visual_lsb_plane": visual_plane_b64,
        "summary": (
            f"LSB analysis detected statistical anomalies across {suspicious_count} channels."
            if suspicious_count > 0 else
            "All color channels exhibit normal, natural LSB bit-plane distributions."
        )
    }
