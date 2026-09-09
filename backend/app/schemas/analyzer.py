"""
Pydantic Schemas for Steganalysis & Forensic Reports
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class FindingSchema(BaseModel):
    severity: str
    category: str
    title: str
    description: str
    evidence: str


class IndicatorSchema(BaseModel):
    name: str
    impact: str
    is_positive: bool
    category: str
    evidence: str
    explanation: str


class FileInfoSchema(BaseModel):
    filename: str
    format: str
    file_size_bytes: int
    file_size_kb: float
    dimensions: Dict[str, Any]
    color_mode: str
    channel_count: int


class RiskScoreSchema(BaseModel):
    score: int
    risk_level: str


class FullReportSchema(BaseModel):
    analysis_id: str
    timestamp: str
    section_1_file_information: FileInfoSchema
    section_2_cryptographic_hashes: Dict[str, str]
    section_3_metadata_analysis: Dict[str, Any]
    section_4_entropy_analysis: Dict[str, Any]
    section_5_lsb_analysis: Dict[str, Any]
    section_6_histogram_analysis: Dict[str, Any]
    section_7_channel_correlation: Dict[str, Any]
    section_8_structural_analysis: Dict[str, Any]
    section_9_detected_indicators: List[IndicatorSchema]
    section_10_risk_score: RiskScoreSchema
    section_11_technical_findings: List[FindingSchema]
    section_12_final_assessment: str
    section_13_limitations: str


class ReportSummarySchema(BaseModel):
    analysis_id: str
    timestamp: str
    filename: str
    format: str
    file_size_kb: float
    risk_score: int
    risk_level: str
