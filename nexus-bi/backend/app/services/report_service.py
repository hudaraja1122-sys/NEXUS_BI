from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from app.core.config import settings

REPORTS_DIR = os.path.join(settings.DATA_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_executive_pdf_report(
    report_id: str,
    dataset_name: str,
    query_text: str,
    summary_text: str,
    kpis: Dict[str, Any],
    findings: List[Dict[str, str]],
    recommendations: List[Dict[str, str]],
) -> str:
    """Generates a C-suite formatted executive PDF investigation report using ReportLab."""
    pdf_path = os.path.join(REPORTS_DIR, f"{report_id}.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#121624")
    accent_cyan = colors.HexColor("#00bfa5")
    dark_slate = colors.HexColor("#222a44")
    muted_text = colors.HexColor("#555566")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=22,
        leading=26,
        textColor=primary_color,
        fontName="Helvetica-Bold",
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=muted_text,
        fontName="Helvetica",
    )
    h2_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=dark_slate,
        fontName="Helvetica-Bold",
        spaceBefore=14,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#222233"),
        fontName="Helvetica",
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("NEXUS BI — EXECUTIVE DECISION BRIEF", ParagraphStyle(
        "BrandHeader", fontName="Helvetica-Bold", fontSize=8, textColor=accent_cyan, spaceAfter=4
    )))
    story.append(Paragraph("Autonomous Investigation & Diagnostic Report", title_style))
    story.append(Paragraph(
        f"<b>Dataset:</b> {dataset_name} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Inquiry:</b> {query_text} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Generated:</b> {datetime.now().strftime('%b %d, %Y - %H:%M')}",
        meta_style,
    ))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_cyan, spaceBefore=4, spaceAfter=14))

    # 2. Executive Summary
    story.append(Paragraph("1. EXECUTIVE SUMMARY", h2_style))
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 12))

    # 3. Macro KPI Table
    story.append(Paragraph("2. MEASURED BASELINE METRICS", h2_style))
    kpi_data = [
        [
            Paragraph("<b>Total Revenue</b>", meta_style),
            Paragraph("<b>Total Net Profit</b>", meta_style),
            Paragraph("<b>Total Transactions</b>", meta_style),
            Paragraph("<b>Avg Discount Applied</b>", meta_style),
        ],
        [
            Paragraph(f"<b>${kpis.get('total_revenue', 0):,.2f}</b>", body_style),
            Paragraph(f"<b>${kpis.get('total_profit', 0):,.2f}</b>", body_style),
            Paragraph(f"<b>{kpis.get('total_orders', 0):,}</b>", body_style),
            Paragraph(f"<b>{kpis.get('avg_discount_pct', 0)}%</b>", body_style),
        ],
    ]
    t_kpi = Table(kpi_data, colWidths=[130, 130, 130, 130])
    t_kpi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fb")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e4e7ed")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 14))

    # 4. Key Calculated Findings
    if findings:
        story.append(Paragraph("3. ROOT-CAUSE FINDINGS", h2_style))
        finding_rows = [[
            Paragraph("<b>Dimension / Focus</b>", meta_style),
            Paragraph("<b>Calculated Metric</b>", meta_style),
            Paragraph("<b>Evidence Observation</b>", meta_style),
        ]]
        for f in findings:
            finding_rows.append([
                Paragraph(f"<b>{f.get('title', '')}</b>", body_style),
                Paragraph(f"<font color='#d9383a'><b>{f.get('metric', '')}</b></font>", body_style),
                Paragraph(f.get("detail", ""), body_style),
            ])
        t_findings = Table(finding_rows, colWidths=[130, 110, 280])
        t_findings.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_findings)
        story.append(Spacer(1, 14))

    # 5. Evidence-Grounded Recommendations
    if recommendations:
        story.append(KeepTogether([
            Paragraph("4. ACTIONABLE DIRECTIVES", h2_style),
            Spacer(1, 4)
        ]))
        rec_rows = [[
            Paragraph("<b>Priority</b>", meta_style),
            Paragraph("<b>Strategic Action</b>", meta_style),
            Paragraph("<b>Data Justification</b>", meta_style),
        ]]
        for r in recommendations:
            pri = r.get("priority", "Medium")
            tag_color = "#d9383a" if pri == "High" else "#e67e22"
            rec_rows.append([
                Paragraph(f"<font color='{tag_color}'><b>{pri}</b></font>", body_style),
                Paragraph(f"<b>{r.get('action', '')}</b>", body_style),
                Paragraph(r.get("reason", ""), body_style),
            ])
        t_recs = Table(rec_rows, colWidths=[65, 185, 270])
        t_recs.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_recs)

    # 6. Audit Stamp Footer
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d0d4dc"), spaceAfter=8))
    story.append(Paragraph(
        "NEXUS BI Autonomous Analytical Architecture • Deterministic DuckDB Processing • Zero Arbitrary Code Generation",
        ParagraphStyle("Footer", fontName="Helvetica", fontSize=7, textColor=colors.HexColor("#888899"), alignment=1),
    ))

    doc.build(story)
    return pdf_path