"""
Capacity Calculation Module
Accurately determines available embedding capacity in bytes and bits for given cover images.
"""
from PIL import Image
from typing import Dict, Any


def calculate_image_capacity(
    img: Image.Image,
    bits_per_channel: int = 1,
    channels_to_use: int = 3  # RGB channels
) -> Dict[str, Any]:
    """
    Calculates the exact lossless LSB embedding capacity for an image.
    Uses RGB channels (3 channels) even in RGBA images to preserve alpha transparency integrity.
    """
    width, height = img.size
    total_pixels = width * height
    total_bits = total_pixels * channels_to_use * bits_per_channel
    total_bytes = total_bits // 8

    return {
        "width": width,
        "height": height,
        "total_pixels": total_pixels,
        "channels_used": channels_to_use,
        "bits_per_channel": bits_per_channel,
        "capacity_bits": total_bits,
        "capacity_bytes": total_bytes,
        "capacity_kb": round(total_bytes / 1024, 2),
    }


def evaluate_capacity_for_payload(
    img: Image.Image,
    message_len_bytes: int,
    fixed_overhead: int = 92
) -> Dict[str, Any]:
    """
    Evaluates whether an image has sufficient capacity for a given secret message length.
    """
    capacity_info = calculate_image_capacity(img)
    total_capacity = capacity_info["capacity_bytes"]
    required_bytes = message_len_bytes + fixed_overhead
    
    sufficient = total_capacity >= required_bytes
    utilization = (required_bytes / total_capacity * 100.0) if total_capacity > 0 else 0.0

    return {
        **capacity_info,
        "required_bytes": required_bytes,
        "required_kb": round(required_bytes / 1024, 2),
        "sufficient_capacity": sufficient,
        "utilization_percentage": round(min(utilization, 100.0), 2),
        "status": "Sufficient capacity" if sufficient else "Insufficient capacity",
    }
