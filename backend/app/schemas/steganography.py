"""
Pydantic Schemas for Steganography Operations
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CapacityResponse(BaseModel):
    width: int
    height: int
    total_pixels: int
    channels_used: int
    bits_per_channel: int
    capacity_bits: int
    capacity_bytes: int
    capacity_kb: float
    required_bytes: Optional[int] = None
    required_kb: Optional[float] = None
    sufficient_capacity: Optional[bool] = None
    utilization_percentage: Optional[float] = None
    status: Optional[str] = None


class EncodeResponse(BaseModel):
    success: bool
    message: str
    output_filename: str
    dimensions: str
    mode: str
    payload_bytes: int
    capacity_bytes: int
    capacity_utilization: float
    cover_sha256: str
    stego_sha256: str
    download_url: str


class DecodeResponse(BaseModel):
    success: bool
    secret_message: str
    payload_bytes: int
    ciphertext_bytes: int
    version: int
    compressed: bool
    integrity_verified: bool
    stego_sha256: str


class DetectionResponse(BaseModel):
    detected: bool
    version: Optional[int] = None
    flags: Optional[int] = None
    compressed: Optional[bool] = None
    ciphertext_length: Optional[int] = None
    total_payload_bytes: Optional[int] = None
    header_crc_valid: Optional[bool] = None
    reason: Optional[str] = None
