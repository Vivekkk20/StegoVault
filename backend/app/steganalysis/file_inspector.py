"""
File & Structural Forensic Inspector
Inspects file metadata, image chunks/headers, and detects unauthorized trailing payload data.
"""
import struct
import hashlib
from typing import Dict, Any, List
from PIL import Image
from PIL.ExifTags import TAGS

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
BMP_SIGNATURE = b"BM"


def inspect_file_structure(data: bytes, img: Image.Image, filename: str = "uploaded_image") -> Dict[str, Any]:
    """
    Performs deep inspection of image headers, chunks, EXIF metadata, and trailing bytes.
    """
    width, height = img.size
    total_file_size = len(data)
    mode = img.mode
    channel_count = len(mode)
    
    file_format = "UNKNOWN"
    if data.startswith(PNG_SIGNATURE):
        file_format = "PNG"
    elif data.startswith(BMP_SIGNATURE):
        file_format = "BMP"

    # Trailing data detection
    trailing_info = detect_trailing_data(data, file_format)

    # Metadata extraction
    metadata_info = extract_metadata(img, data, file_format)

    # Structural chunks / headers
    structure_info = analyze_binary_structure(data, file_format)

    return {
        "filename": filename,
        "format": file_format,
        "file_size_bytes": total_file_size,
        "file_size_kb": round(total_file_size / 1024, 2),
        "dimensions": {
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 2) if height > 0 else 1.0,
            "total_pixels": width * height,
        },
        "color_mode": mode,
        "channel_count": channel_count,
        "trailing_data": trailing_info,
        "metadata": metadata_info,
        "structure": structure_info,
    }


def detect_trailing_data(data: bytes, file_format: str) -> Dict[str, Any]:
    """
    Scans for unauthorized payload data appended past the legal EOF marker.
    """
    total_size = len(data)
    
    if file_format == "PNG" and data.startswith(PNG_SIGNATURE):
        # Walk PNG chunks until IEND
        offset = 8
        data_len = len(data)
        
        while offset + 8 <= data_len:
            length, chunk_type = struct.unpack(">I4s", data[offset:offset + 8])
            chunk_total_len = 12 + length
            
            if chunk_type == b"IEND":
                legal_eof = offset + chunk_total_len
                if legal_eof < total_size:
                    trailing_bytes = data[legal_eof:]
                    trailing_size = len(trailing_bytes)
                    return {
                        "detected": True,
                        "legal_eof_offset": legal_eof,
                        "trailing_size_bytes": trailing_size,
                        "trailing_size_kb": round(trailing_size / 1024, 2),
                        "sha256": hashlib.sha256(trailing_bytes).hexdigest(),
                        "preview_hex": trailing_bytes[:64].hex(),
                        "description": (
                            f"Additional {trailing_size} bytes detected past the PNG IEND chunk. "
                            "This is a common indicator of EOF-appended steganography or file concatenation."
                        )
                    }
                else:
                    return {
                        "detected": False,
                        "legal_eof_offset": legal_eof,
                        "trailing_size_bytes": 0,
                    }
            offset += chunk_total_len

    elif file_format == "BMP" and data.startswith(BMP_SIGNATURE):
        if total_size >= 14:
            bf_size = struct.unpack("<I", data[2:6])[0]
            if 0 < bf_size < total_size:
                trailing_bytes = data[bf_size:]
                trailing_size = len(trailing_bytes)
                return {
                    "detected": True,
                    "legal_eof_offset": bf_size,
                    "trailing_size_bytes": trailing_size,
                    "trailing_size_kb": round(trailing_size / 1024, 2),
                    "sha256": hashlib.sha256(trailing_bytes).hexdigest(),
                    "preview_hex": trailing_bytes[:64].hex(),
                    "description": (
                        f"Additional {trailing_size} bytes detected past the declared BMP file size ({bf_size} bytes). "
                        "Indicates appended data."
                    )
                }
            return {
                "detected": False,
                "legal_eof_offset": bf_size if bf_size > 0 else total_size,
                "trailing_size_bytes": 0,
            }

    return {
        "detected": False,
        "trailing_size_bytes": 0,
    }


def extract_metadata(img: Image.Image, data: bytes, file_format: str) -> Dict[str, Any]:
    """
    Extracts standard and hidden metadata from image headers.
    """
    exif_data = {}
    suspicious_tags = []

    # Pillow EXIF
    raw_exif = img.getexif()
    if raw_exif:
        for tag_id, val in raw_exif.items():
            tag_name = TAGS.get(tag_id, str(tag_id))
            val_str = str(val)[:120]
            exif_data[tag_name] = val_str
            # Check for suspicious or oversized metadata
            if len(str(val)) > 500 or any(keyword in tag_name.lower() for keyword in ["comment", "usercomment", "script"]):
                suspicious_tags.append({"tag": tag_name, "preview": val_str, "length": len(str(val))})

    # PNG specific text chunks
    png_chunks = []
    if file_format == "PNG" and data.startswith(PNG_SIGNATURE):
        offset = 8
        while offset + 8 <= len(data):
            length, chunk_type = struct.unpack(">I4s", data[offset:offset + 8])
            chunk_name = chunk_type.decode(errors="ignore")
            if chunk_name in ("tEXt", "zTXt", "iTXt", "eXIf"):
                chunk_data = data[offset + 8:offset + 8 + length]
                png_chunks.append({
                    "type": chunk_name,
                    "length": length,
                    "preview": chunk_data[:64].decode(errors="ignore")
                })
            offset += 12 + length

    return {
        "has_exif": bool(exif_data),
        "exif_count": len(exif_data),
        "exif_fields": exif_data,
        "png_text_chunks": png_chunks,
        "suspicious_tags": suspicious_tags,
    }


def analyze_binary_structure(data: bytes, file_format: str) -> Dict[str, Any]:
    """
    Analyzes binary integrity and chunk hierarchy.
    """
    chunks_found = []
    anomalies = []

    if file_format == "PNG" and data.startswith(PNG_SIGNATURE):
        offset = 8
        iend_count = 0
        while offset + 8 <= len(data):
            length, chunk_type = struct.unpack(">I4s", data[offset:offset + 8])
            chunk_name = chunk_type.decode(errors="ignore")
            chunks_found.append(chunk_name)
            if chunk_name == "IEND":
                iend_count += 1
            offset += 12 + length

        if iend_count > 1:
            anomalies.append(f"Multiple IEND chunks ({iend_count}) detected in PNG stream.")
        if iend_count == 0:
            anomalies.append("Missing PNG IEND terminal chunk.")

    return {
        "chunks_summary": chunks_found[:15],
        "total_chunks": len(chunks_found),
        "anomalies": anomalies,
    }
