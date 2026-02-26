from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user
from datetime import datetime
from fastapi.responses import StreamingResponse
import io
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch



router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/summary")
def get_report_summary(
    start_date: str,
    end_date: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        alerts = supabase.table("alerts") \
            .select("*") \
            .eq("company_id", current_user["company_id"]) \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .execute()

        total_alerts = len(alerts.data)

        high_risk = len([a for a in alerts.data if a["severity"] in ["high", "critical"]])

        resolved = len([a for a in alerts.data if a["status"] == "resolved"])

        return {
            "total_alerts": total_alerts,
            "high_risk": high_risk,
            "resolved": resolved
        }

    except Exception as e:
        print("Report summary error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch report summary")
   

    

@router.get("/download")
def download_report(
    start_date: str,
    end_date: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        alerts = supabase.table("alerts") \
            .select("severity,description,status,created_at") \
            .eq("company_id", current_user["company_id"]) \
            .gte("created_at", start_date) \
            .lte("created_at", end_date) \
            .execute()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []
        styles = getSampleStyleSheet()

        # Title
        elements.append(Paragraph("<b>Security Monitoring Report</b>", styles["Title"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Date Range
        elements.append(Paragraph(f"From: {start_date}", styles["Normal"]))
        elements.append(Paragraph(f"To: {end_date}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Summary
        total_alerts = len(alerts.data)
        high_risk = len([a for a in alerts.data if a["severity"] in ["high", "critical"]])
        resolved = len([a for a in alerts.data if a["status"] == "resolved"])

        elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph(f"Total Alerts: {total_alerts}", styles["Normal"]))
        elements.append(Paragraph(f"High Risk Alerts: {high_risk}", styles["Normal"]))
        elements.append(Paragraph(f"Resolved Alerts: {resolved}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Table Data
        table_data = [["Severity", "Description", "Status", "Created At"]]

        for alert in alerts.data:
            table_data.append([
                alert["severity"],
                alert["description"],
                alert["status"],
                alert["created_at"][:19]
            ])

        table = Table(table_data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ]))

        elements.append(table)

        doc.build(elements)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=security_report.pdf"
            }
        )

    except Exception as e:
        print("PDF Report error:", e)
        raise HTTPException(status_code=500, detail="Failed to generate PDF")