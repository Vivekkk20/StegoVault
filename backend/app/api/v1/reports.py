"""
Forensic Reports API Endpoints (/api/v1/reports)
Lists, views, exports, and deletes forensic analysis reports.
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional

from app.core.storage import list_reports, get_report, delete_report, generate_html_report
from app.schemas.analyzer import ReportSummarySchema, FullReportSchema

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", response_model=List[ReportSummarySchema])
async def get_all_reports(limit: int = Query(default=50, ge=1, le=200)):
    """Lists summary cards of saved forensic analysis reports."""
    return list_reports(limit=limit)


@router.get("/{report_id}")
async def get_single_report(report_id: str):
    """Retrieves full 13-section report by ID."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report


@router.get("/{report_id}/export")
async def export_report(
    report_id: str,
    format: str = Query(default="html", pattern="^(html|json)$")
):
    """
    Exports a forensic report as standalone printable HTML or raw JSON.
    """
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    if format == "json":
        return JSONResponse(
            content=report,
            headers={"Content-Disposition": f'attachment; filename="stegovault_report_{report_id[:8]}.json"'}
        )
    else:
        html_content = generate_html_report(report)
        return HTMLResponse(
            content=html_content,
            headers={"Content-Disposition": f'inline; filename="stegovault_report_{report_id[:8]}.html"'}
        )


@router.delete("/{report_id}")
async def remove_report(report_id: str):
    """Deletes a forensic report from storage."""
    deleted = delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found.")
    return {"success": True, "message": f"Report {report_id} deleted."}
