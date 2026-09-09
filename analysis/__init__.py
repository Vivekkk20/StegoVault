"""
StegoVault - Analysis & Steganalysis Package
Provides carrier capacity checks, image fidelity error metrics, and statistical steganalysis.

Modules:
    capacity: Computes maximum safe byte capacity and payload fit evaluations.
    image_quality: Computes Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).
    steganalysis: Extracts LSB bit planes and evaluates Chi-Square statistical anomalies.
"""

from analysis.capacity import (
    SAFE_CAPACITY_RATIO,
    calculate_carrier_capacity,
    payload_fits,
)
from analysis.image_quality import (
    calculate_mse,
    calculate_psnr,
)
from analysis.steganalysis import (
    chi_square_attack,
    extract_lsb_plane,
)

__all__ = [
    "calculate_carrier_capacity",
    "payload_fits",
    "calculate_mse",
    "calculate_psnr",
    "extract_lsb_plane",
    "chi_square_attack",
    "SAFE_CAPACITY_RATIO",
]
