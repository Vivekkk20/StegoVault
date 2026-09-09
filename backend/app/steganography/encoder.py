"""
LSB Steganography Encoder Module
Embeds authenticated encrypted binary payloads into lossless RGB/RGBA image channels.
Guarantees non-destructive processing: never overwrites the cover image.
"""
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Any

from app.core.exceptions import InsufficientCapacityError
from app.steganography.payload import pack_payload
from app.steganography.capacity import calculate_image_capacity


def embed_payload_into_image(
    cover_image: Image.Image,
    message: str,
    password: str,
    compress: bool = True
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Encrypts message and embeds structured payload into cover_image via LSB.
    Returns:
        (stego_image, metadata)
    """
    capacity_info = calculate_image_capacity(cover_image)
    max_bytes = capacity_info["capacity_bytes"]

    # Generate encrypted, structured binary payload
    payload_bytes = pack_payload(message=message, password=password, compress=compress)
    payload_len = len(payload_bytes)

    if payload_len > max_bytes:
        raise InsufficientCapacityError(
            f"Payload length ({payload_len} bytes) exceeds available image capacity "
            f"({max_bytes} bytes / {capacity_info['capacity_kb']} KB)."
        )

    # Convert payload bytes to array of individual bits (0 or 1)
    payload_bits = np.unpackbits(np.frombuffer(payload_bytes, dtype=np.uint8))
    num_bits = len(payload_bits)

    # Convert image to numpy array
    img_array = np.array(cover_image, copy=True)
    height, width = img_array.shape[:2]
    mode = cover_image.mode

    if mode == "RGB":
        # Flatten all 3 channels
        flattened = img_array.reshape(-1)
        # Clear LSB and OR with payload bits
        flattened[:num_bits] = (flattened[:num_bits] & 0xFE) | payload_bits
        stego_array = flattened.reshape((height, width, 3))
    elif mode == "RGBA":
        # Preserve alpha channel; embed strictly into RGB
        rgb_view = img_array[:, :, :3].reshape(-1)
        rgb_view[:num_bits] = (rgb_view[:num_bits] & 0xFE) | payload_bits
        img_array[:, :, :3] = rgb_view.reshape((height, width, 3))
        stego_array = img_array
    else:
        # Fallback convert to RGB
        rgb_img = cover_image.convert("RGB")
        img_array = np.array(rgb_img, copy=True)
        flattened = img_array.reshape(-1)
        flattened[:num_bits] = (flattened[:num_bits] & 0xFE) | payload_bits
        stego_array = flattened.reshape((height, width, 3))
        mode = "RGB"

    stego_image = Image.fromarray(stego_array, mode=mode)

    metadata = {
        "payload_bytes": payload_len,
        "payload_bits": num_bits,
        "capacity_bytes": max_bytes,
        "capacity_utilization": round((payload_len / max_bytes) * 100.0, 2),
        "dimensions": f"{width}x{height}",
        "mode": mode,
        "compressed": compress,
    }

    return stego_image, metadata
