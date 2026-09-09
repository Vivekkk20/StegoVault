"""
StegoVault Forensic Risk Scoring Engine
Calculates a transparent, calibrated risk score (0-100) and compiles structured technical findings.
"""
from typing import Dict, Any, List, Tuple


def calculate_risk_score(
    structure_data: Dict[str, Any],
    entropy_data: Dict[str, Any],
    lsb_data: Dict[str, Any],
    histogram_data: Dict[str, Any],
    correlation_data: Dict[str, Any],
    stegovault_detection: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Computes calibrated risk score from individual statistical and structural forensic tests.
    Score brackets:
      0–20:   Very Low
      21–40:  Low
      41–60:  Moderate
      61–80:  High
      81–100: Critical
    """
    base_score = 0
    findings: List[Dict[str, Any]] = []
    indicators: List[Dict[str, Any]] = []

    # 1. StegoVault Signature Detection
    if stegovault_detection and stegovault_detection.get("detected"):
        points = 85
        base_score += points
        indicators.append({
            "name": "StegoVault Payload Header Detected",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Signature",
            "evidence": f"Version {stegovault_detection.get('version')}, Length {stegovault_detection.get('total_payload_bytes')} bytes",
            "explanation": "Definite presence of authenticated StegoVault cryptographic container in LSB plane."
        })
        findings.append({
            "severity": "CRITICAL",
            "category": "Payload",
            "title": "StegoVault Container Detected",
            "description": "The file contains a verified StegoVault binary header and payload structure.",
            "evidence": f"Valid header CRC: {stegovault_detection.get('header_crc_valid')}, Ciphertext length: {stegovault_detection.get('ciphertext_length')} bytes."
        })

    # 2. Trailing Appended Data
    trailing = structure_data.get("trailing_data", {})
    if trailing.get("detected"):
        t_size = trailing.get("trailing_size_bytes", 0)
        points = 35 if t_size > 100 else 20
        base_score += points
        indicators.append({
            "name": "Unauthorized Trailing Binary Data",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Structural",
            "evidence": f"{t_size} bytes past EOF (SHA-256: {trailing.get('sha256')[:16]}...)",
            "explanation": "Binary data found appended past the normal image termination marker."
        })
        findings.append({
            "severity": "HIGH",
            "category": "Structural",
            "title": "Trailing Data Detected After Legal EOF",
            "description": trailing.get("description", "Extra data detected past EOF."),
            "evidence": f"Offset: {trailing.get('legal_eof_offset')}, Size: {t_size} bytes."
        })
    else:
        indicators.append({
            "name": "Clean Binary Structure",
            "impact": "-0",
            "is_positive": False,
            "category": "Structural",
            "evidence": "No trailing data past legal EOF",
            "explanation": "Image concludes exactly at declared termination marker."
        })

    # 3. LSB Bit Distribution & Chi-Square PoV Anomaly
    suspicious_lsb_channels = lsb_data.get("suspicious_channels_count", 0)
    if suspicious_lsb_channels > 0:
        points = min(30, suspicious_lsb_channels * 12)
        base_score += points
        indicators.append({
            "name": "LSB Statistical Distribution Anomaly",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Statistical",
            "evidence": f"{suspicious_lsb_channels} channel(s) flagged suspicious",
            "explanation": "Equalized Pairs of Values (PoV) or artificial bit-plane uniformity detected."
        })
        findings.append({
            "severity": "HIGH" if suspicious_lsb_channels >= 2 else "MEDIUM",
            "category": "LSB",
            "title": "LSB Replacement Artifacts Detected",
            "description": lsb_data.get("summary", "Statistical anomalies observed in LSB bit-planes."),
            "evidence": f"Flagged channels: {suspicious_lsb_channels}/3."
        })
    else:
        indicators.append({
            "name": "Normal LSB Bit-Plane Distribution",
            "impact": "-0",
            "is_positive": False,
            "category": "Statistical",
            "evidence": "All channels within normal Poisson/Gaussian variances",
            "explanation": "LSB planes exhibit natural texture correlation and non-uniform bit balances."
        })

    # 4. Entropy Anomalies
    if entropy_data.get("is_lsb_anomaly"):
        points = 20
        base_score += points
        indicators.append({
            "name": "Elevated LSB Channel Entropy",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Entropy",
            "evidence": f"Channels with H > 0.998: {', '.join(entropy_data.get('suspicious_channels', []))}",
            "explanation": "High LSB entropy indicates compressed or cryptographically encrypted hidden data."
        })
        findings.append({
            "severity": "MEDIUM",
            "category": "Entropy",
            "title": "Abnormally High LSB Shannon Entropy",
            "description": entropy_data.get("evaluation", "Elevated entropy in LSB."),
            "evidence": f"Channel LSB entropies: {entropy_data.get('lsb_bit_entropy')}."
        })

    # 5. Histogram Flattening Anomaly
    if histogram_data.get("is_flattened_anomaly"):
        points = 15
        base_score += points
        indicators.append({
            "name": "Histogram Pair-of-Values Flattening",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Histogram",
            "evidence": f"PoV Deltas: {histogram_data.get('pov_pairing_delta')}",
            "explanation": "Unnatural frequency convergence between adjacent odd/even pixel intensities."
        })
        findings.append({
            "severity": "MEDIUM",
            "category": "Histogram",
            "title": "Adjacent Intensity Pairing Flattening",
            "description": histogram_data.get("evaluation", "PoV flattening detected."),
            "evidence": f"Low PoV pairing delta detected across color channels."
        })

    # 6. Channel Correlation Anomaly
    if correlation_data.get("is_correlation_anomaly"):
        points = 10
        base_score += points
        indicators.append({
            "name": "Inter-Channel Correlation Perturbation",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Correlation",
            "evidence": f"LSB correlations: {correlation_data.get('lsb_plane_correlation')}",
            "explanation": "LSB planes lack expected inter-channel natural color gradient coherence."
        })

    # 7. Metadata Anomalies
    metadata_info = structure_data.get("metadata", {})
    suspicious_tags = metadata_info.get("suspicious_tags", [])
    if suspicious_tags:
        points = 15
        base_score += points
        indicators.append({
            "name": "Suspicious Header Metadata Fields",
            "impact": f"+{points}",
            "is_positive": True,
            "category": "Metadata",
            "evidence": f"{len(suspicious_tags)} non-standard or oversized fields",
            "explanation": "Metadata contains long or suspicious keyword structures."
        })
        findings.append({
            "severity": "LOW",
            "category": "Metadata",
            "title": "Anomalous Metadata Found",
            "description": "Image metadata contains oversized or suspicious tag content.",
            "evidence": f"Tags: {[t['tag'] for t in suspicious_tags]}."
        })

    # Cap score at 100
    final_score = min(100, max(0, base_score))

    # Determine risk level
    if final_score <= 20:
        risk_level = "VERY_LOW"
        assessment = "Normal image. No substantial statistical, structural, or cryptographic indicators of steganography were identified."
    elif final_score <= 40:
        risk_level = "LOW"
        assessment = "Low probability of steganography. Minor statistical fluctuations observed, likely attributable to compression or image texture."
    elif final_score <= 60:
        risk_level = "MODERATE"
        assessment = "Moderate suspicion. Some statistical or structural anomalies detected. Inconclusive without targeted extraction attempts."
    elif final_score <= 80:
        risk_level = "HIGH"
        assessment = "High probability of steganography. Multiple concurrent statistical anomalies (such as LSB pairing equalization or trailing binary data) strongly suggest data hiding."
    else:
        risk_level = "CRITICAL"
        assessment = "Critical certainty. A definitive steganographic container or overwhelming combination of structural and statistical anomalies was confirmed."

    return {
        "score": final_score,
        "risk_level": risk_level,
        "indicators": indicators,
        "findings": findings,
        "final_assessment": assessment,
        "limitations": (
            "Absence of detected indicators does not prove that an image contains no hidden data. "
            "Advanced spread-spectrum, low-embedding-rate, or adaptive matrix steganography techniques "
            "may evade first-order statistical and Chi-square steganalysis."
        )
    }
