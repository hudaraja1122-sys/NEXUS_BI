from __future__ import annotations

import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.services.llm_engine import run_autonomous_investigation
from app.services.report_service import generate_executive_pdf_report

router = APIRouter(prefix="/analysis", tags=["analysis"])
REPORTS_DIR = os.path.join(settings.DATA_DIR, "reports")


class InvestigationRequest(BaseModel):
    dataset_id: str
    prompt: str


class PDFReportRequest(BaseModel):
    dataset_name: str
    query_text: str
    summary_text: str
    kpis: Dict[str, Any]
    findings: List[Dict[str, str]] = []
    recommendations: List[Dict[str, str]] = []


@router.post("/query")
def run_investigation(req: InvestigationRequest) -> Dict[str, Any]:
    try:
        return run_autonomous_investigation(req.dataset_id, req.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Investigation failed: {e}")


@router.post("/export-pdf")
def create_report_pdf(req: PDFReportRequest) -> Dict[str, str]:
    """Generates the executive PDF brief and returns the download token."""
    report_id = f"nexus_brief_{uuid.uuid4().hex[:8]}"
    try:
        generate_executive_pdf_report(
            report_id=report_id,
            dataset_name=req.dataset_name,
            query_text=req.query_text,
            summary_text=req.summary_text,
            kpis=req.kpis,
            findings=req.findings,
            recommendations=req.recommendations,
        )
        return {"report_id": report_id, "download_url": f"/api/analysis/reports/{report_id}/download"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")


@router.get("/reports/{report_id}/download")
def download_pdf(report_id: str):
    """Downloads the generated PDF report."""
    pdf_path = os.path.join(REPORTS_DIR, f"{report_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Requested report does not exist.")
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{report_id}.pdf",
    )