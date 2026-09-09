"""
Steganalysis Analyzer API Endpoints (/api/v1/analyzer)
Performs forensic inspection of untrusted images without requiring StegoVault payloads.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.security.validation import validate_image_safe
from app.steganalysis.service import perform_forensic_analysis
from app.core.storage import save_report, get_report
from app.core.exceptions import StegoVaultException
from app.core.logging import logger

router = APIRouter(prefix="/analyzer", tags=["Analyzer"])


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...)
):
    """
    Executes full forensic steganalysis suite on uploaded image:
    1. File & Binary structure inspection
    2. Cryptographic hashes (SHA-256, SHA-512)
    3. Metadata & chunk parsing
    4. Multi-layer Shannon entropy
    5. LSB bit-plane distribution & Chi-square PoV test
    6. 256-bin RGB histograms & PoV pairing delta
    7. Pearson channel correlation
    8. Trailing data detection past legal EOF
    9. Transparent risk scoring (0-100) & technical findings
    Saves report to storage and returns full 13-section report.
    """
    try:
        content = await file.read()
        filename = file.filename or "uploaded_image"
        img, _ = validate_image_safe(content)

        report = perform_forensic_analysis(
            data=content,
            img=img,
            filename=filename
        )

        # Persist report for history & export
        save_report(report)

        return report
    except StegoVaultException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error during forensic analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Forensic analysis failed to process image.")


@router.get("/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """
    Retrieves a previously computed forensic analysis report by ID.
    """
    report = get_report(analysis_id)
    if not report:
        raise HTTPException(status_code=404, detail="Forensic analysis report not found.")
    return report


@router.get("/{analysis_id}/lsb-preview")
async def get_lsb_preview(analysis_id: str):
    """
    Retrieves the extracted base64 visual LSB plane for an analysis report.
    """
    report = get_report(analysis_id)
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found.")

    visual_data = report.get("section_5_lsb_analysis", {}).get("visual_lsb_plane")
    if not visual_data:
        raise HTTPException(status_code=404, detail="Visual LSB plane not available.")

    return {"analysis_id": analysis_id, "visual_lsb_plane": visual_data}
