"""
StegoVault - Steganography Package
Provides spatial-domain Least Significant Bit (LSB) embedding and extraction routines.

Modules:
    lsb: Spatial LSB manipulation for RGB and RGBA carriers with alpha channel preservation.
"""

from stego.lsb import embed_lsb, extract_lsb

__all__ = [
    "embed_lsb",
    "extract_lsb",
]
