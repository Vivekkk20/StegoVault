"""
StegoVault Forensic Steganalysis Service
Orchestrates full forensic analysis across all detection modules and compiles reports.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from PIL import Image

from app.security.hashes import calculate_hashes
from app.steganography.decoder import detect_stegovault_payload
from app.steganalysis.file_inspector import inspect_file_structure
from app.steganalysis.entropy import analyze_entropy
from app.steganalysis.lsb_analyzer import analyze_lsb
from app.steganalysis.histogram import analyze_histograms
from app.steganalysis.correlation import analyze_channel_correlation
from app.steganalysis.risk_engine import calculate_risk_score


def perform_forensic_analysis(
    data: bytes,
    img: Image.Image,
    filename: str = "uploaded_image"
) -> Dict[str, Any]:
    """
    Executes complete forensic steganalysis suite on provided image bytes and PIL image.
    Compiles a comprehensive 13-section forensic analysis report.
    """
    analysis_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1 & 8. File Information & Structural Inspection (including Trailing Data)
    structure_info = inspect_file_structure(data, img, filename)

    # 2. Cryptographic Hashes
    hashes_info = calculate_hashes(data)

    # StegoVault Signature Detection Probe
    stegovault_detection = detect_stegovault_payload(img)

    # 4. Entropy Analysis
    entropy_info = analyze_entropy(data, img)

    # 5. LSB Analysis
    lsb_info = analyze_lsb(img)

    # 6. Histogram Analysis
    histogram_info = analyze_histograms(img)

    # 7. Channel Correlation
    correlation_info = analyze_channel_correlation(img)

    # 9 & 10 & 11 & 12 & 13. Risk Scoring & Technical Findings
    risk_info = calculate_risk_score(
        structure_data=structure_info,
        entropy_data=entropy_info,
        lsb_data=lsb_info,
        histogram_data=histogram_info,
        correlation_data=correlation_info,
        stegovault_detection=stegovault_detection,
    )

    # Assemble complete 13-section report
    report = {
        "analysis_id": analysis_id,
        "timestamp": timestamp,
        "section_1_file_information": {
            "filename": filename,
            "format": structure_info["format"],
            "file_size_bytes": structure_info["file_size_bytes"],
            "file_size_kb": structure_info["file_size_kb"],
            "dimensions": structure_info["dimensions"],
            "color_mode": structure_info["color_mode"],
            "channel_count": structure_info["channel_count"],
        },
        "section_2_cryptographic_hashes": hashes_info,
        "section_3_metadata_analysis": structure_info["metadata"],
        "section_4_entropy_analysis": entropy_info,
        "section_5_lsb_analysis": {
            "channels": lsb_info["channels"],
            "suspicious_channels_count": lsb_info["suspicious_channels_count"],
            "summary": lsb_info["summary"],
            "visual_lsb_plane": lsb_info["visual_lsb_plane"],
        },
        "section_6_histogram_analysis": histogram_info,
        "section_7_channel_correlation": correlation_info,
        "section_8_structural_analysis": {
            "trailing_data": structure_info["trailing_data"],
            "chunks_summary": structure_info["structure"]["chunks_summary"],
            "anomalies": structure_info["structure"]["anomalies"],
            "stegovault_signature": stegovault_detection,
        },
        "section_9_detected_indicators": risk_info["indicators"],
        "section_10_risk_score": {
            "score": risk_info["score"],
            "risk_level": risk_info["risk_level"],
        },
        "section_11_technical_findings": risk_info["findings"],
        "section_12_final_assessment": risk_info["final_assessment"],
        "section_13_limitations": risk_info["limitations"],
    }

    return report
