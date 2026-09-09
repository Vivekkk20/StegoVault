"""
Report Storage & Retrieval Manager
Persists forensic analysis reports to storage/reports/ and generates HTML/JSON exports.
"""
import json
import html
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import settings


def save_report(report_data: Dict[str, Any]) -> str:
    """Saves a forensic report as JSON."""
    report_id = report_data.get("analysis_id")
    if not report_id:
        raise ValueError("Report missing analysis_id")

    reports_dir = settings.REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    file_path = reports_dir / f"{report_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    return report_id


def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single report by ID."""
    file_path = settings.REPORTS_DIR / f"{report_id}.json"
    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_reports(limit: int = 50) -> List[Dict[str, Any]]:
    """Lists summary cards of saved reports sorted newest first."""
    reports_dir = settings.REPORTS_DIR
    if not reports_dir.exists():
        return []

    summaries = []
    for p in sorted(reports_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                summaries.append({
                    "analysis_id": data.get("analysis_id"),
                    "timestamp": data.get("timestamp"),
                    "filename": data.get("section_1_file_information", {}).get("filename", "unknown"),
                    "format": data.get("section_1_file_information", {}).get("format", "unknown"),
                    "file_size_kb": data.get("section_1_file_information", {}).get("file_size_kb", 0),
                    "risk_score": data.get("section_10_risk_score", {}).get("score", 0),
                    "risk_level": data.get("section_10_risk_score", {}).get("risk_level", "UNKNOWN"),
                })
        except Exception:
            continue

    return summaries


def delete_report(report_id: str) -> bool:
    """Deletes a report by ID."""
    file_path = settings.REPORTS_DIR / f"{report_id}.json"
    if file_path.exists():
        file_path.unlink()
        return True
    return False


def generate_html_report(report: Dict[str, Any]) -> str:
    """
    Renders a standalone, printable, forensic-styled HTML report document.
    """
    r_id = html.escape(report.get("analysis_id", ""))
    timestamp = html.escape(report.get("timestamp", ""))
    file_info = report.get("section_1_file_information", {})
    hashes = report.get("section_2_cryptographic_hashes", {})
    risk = report.get("section_10_risk_score", {})
    score = risk.get("score", 0)
    risk_level = html.escape(risk.get("risk_level", "UNKNOWN"))
    findings = report.get("section_11_technical_findings", [])
    assessment = html.escape(report.get("section_12_final_assessment", ""))
    limitations = html.escape(report.get("section_13_limitations", ""))

    score_color = "#10b981" if score <= 20 else "#06b6d4" if score <= 40 else "#f59e0b" if score <= 60 else "#f97316" if score <= 80 else "#ef4444"

    findings_html = "".join(f"""
        <div class="finding-card finding-{f.get('severity', 'LOW').lower()}">
            <div class="finding-header">
                <span class="badge badge-{f.get('severity', 'LOW').lower()}">{html.escape(f.get('severity', 'LOW'))}</span>
                <strong>{html.escape(f.get('title', 'Finding'))}</strong>
                <span class="category-tag">{html.escape(f.get('category', ''))}</span>
            </div>
            <p>{html.escape(f.get('description', ''))}</p>
            <div class="evidence-box"><code>{html.escape(f.get('evidence', ''))}</code></div>
        </div>
    """ for f in findings)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>StegoVault Forensic Security Report - {r_id}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background: #0f172a; color: #e2e8f0; margin: 0; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 36px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        h1 {{ color: #38bdf8; margin-top: 0; font-size: 26px; border-bottom: 2px solid #334155; padding-bottom: 12px; }}
        h2 {{ color: #94a3b8; font-size: 18px; margin-top: 28px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #334155; padding-bottom: 6px; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 24px; }}
        .meta-item {{ background: #0f172a; padding: 12px; border-radius: 6px; font-size: 13px; }}
        .meta-label {{ color: #64748b; text-transform: uppercase; font-size: 11px; }}
        .score-banner {{ display: flex; align-items: center; justify-content: space-between; background: #0f172a; border-left: 6px solid {score_color}; padding: 18px; border-radius: 6px; margin: 24px 0; }}
        .score-number {{ font-size: 38px; font-weight: bold; color: {score_color}; }}
        .finding-card {{ background: #0f172a; border-radius: 6px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #64748b; }}
        .finding-critical {{ border-left-color: #ef4444; }}
        .finding-high {{ border-left-color: #f97316; }}
        .finding-medium {{ border-left-color: #f59e0b; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 8px; }}
        .badge-critical {{ background: #ef4444; color: #fff; }}
        .badge-high {{ background: #f97316; color: #fff; }}
        .badge-medium {{ background: #f59e0b; color: #000; }}
        .badge-low {{ background: #06b6d4; color: #000; }}
        .category-tag {{ color: #64748b; font-size: 12px; margin-left: 8px; }}
        .evidence-box {{ background: #020617; padding: 8px 12px; border-radius: 4px; margin-top: 8px; font-size: 12px; color: #38bdf8; word-break: break-all; }}
        .disclaimer-box {{ background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 14px; margin-top: 30px; font-size: 13px; color: #fca5a5; }}
        code {{ font-family: monospace; word-break: break-all; }}
        @media print {{ body {{ background: #fff; color: #000; }} .container {{ border: none; box-shadow: none; background: #fff; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>StegoVault Forensic Security Report</h1>
        <p style="color: #94a3b8; font-size: 13px;">Report ID: <code>{r_id}</code> | Generated: {timestamp}</p>

        <div class="score-banner">
            <div>
                <div style="color: #94a3b8; text-transform: uppercase; font-size: 12px;">Steganography Risk Assessment</div>
                <div style="font-size: 20px; font-weight: bold; color: {score_color};">{risk_level} RISK</div>
            </div>
            <div class="score-number">{score} <span style="font-size: 18px; color: #64748b;">/ 100</span></div>
        </div>

        <h2>1. File Information</h2>
        <div class="meta-grid">
            <div class="meta-item"><div class="meta-label">Filename</div><strong>{html.escape(str(file_info.get("filename")))}</strong></div>
            <div class="meta-item"><div class="meta-label">Format</div><strong>{html.escape(str(file_info.get("format")))}</strong></div>
            <div class="meta-item"><div class="meta-label">Size</div><strong>{file_info.get("file_size_kb")} KB ({file_info.get("file_size_bytes")} bytes)</strong></div>
            <div class="meta-item"><div class="meta-label">Dimensions</div><strong>{file_info.get("dimensions", {}).get("width")} x {file_info.get("dimensions", {}).get("height")} px ({file_info.get("color_mode")})</strong></div>
        </div>

        <h2>2. Cryptographic Integrity Hashes</h2>
        <div class="meta-item" style="margin-bottom: 8px;"><div class="meta-label">SHA-256</div><code>{hashes.get("sha256")}</code></div>
        <div class="meta-item"><div class="meta-label">SHA-512</div><code>{hashes.get("sha512")}</code></div>

        <h2>3. Final Forensic Assessment</h2>
        <p style="line-height: 1.6; font-size: 14px;">{assessment}</p>

        <h2>4. Technical Findings ({len(findings)})</h2>
        {findings_html if findings else "<p style='color: #64748b;'>No anomalous technical findings flagged.</p>"}

        <div class="disclaimer-box">
            <strong>Limitation Statement:</strong> {limitations}
        </div>
    </div>
</body>
</html>"""
