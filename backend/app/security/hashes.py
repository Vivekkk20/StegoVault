"""
Cryptographic Hashing Utilities
Provides SHA-256 and SHA-512 calculation for file streams and memory buffers.
"""
import hashlib
from typing import Dict, Union
from pathlib import Path


def calculate_hashes(data_or_path: Union[bytes, str, Path]) -> Dict[str, str]:
    """
    Calculate both SHA-256 and SHA-512 hashes for given bytes or file path.
    Uses chunked streaming for memory efficiency.
    """
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()

    if isinstance(data_or_path, (str, Path)):
        path = Path(data_or_path)
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
                sha512.update(chunk)
    elif isinstance(data_or_path, (bytes, bytearray)):
        sha256.update(data_or_path)
        sha512.update(data_or_path)
    else:
        raise ValueError("Unsupported type for hash calculation")

    return {
        "sha256": sha256.hexdigest(),
        "sha512": sha512.hexdigest(),
    }


def calculate_sha256(data: bytes) -> str:
    """Calculate single SHA-256 hash."""
    return hashlib.sha256(data).hexdigest()
