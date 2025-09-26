from __future__ import annotations
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd

from src.ingest import load_excel_auto, summarize_schema
from src.periods import attach_quarter_period, attach_year_month_period
from src.analysis import concentration_table
from src.exporters import export_concentration_excel

app = FastAPI(title="Concentration Analysis API")

LATEST_UPLOAD = "uploads/latest.xlsx"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    with open(LATEST_UPLOAD, "wb") as f:
        f.write(content)
    df = load_excel_auto(LATEST_UPLOAD)
    return {"rows": len(df), "columns": list(df.columns)}

@app.get("/schema")
def schema():
    try:
        df = load_excel_auto(LATEST_UPLOAD)
    except FileNotFoundError:
        return JSONResponse({"error": "no file uploaded yet"}, status_code=400)
    return summarize_schema(df)

@app.post("/analyze")
async def analyze(
    period_mode: str = Form(..., description="quarter|month"),
    group_col: str = Form(...),
    value_col: str = Form(...),
):
    try:
        df = load_excel_auto(LATEST_UPLOAD)
    except FileNotFoundError:
        return JSONResponse({"error": "no file uploaded yet"}, status_code=400)

    if period_mode == "quarter":
        df = attach_quarter_period(df, year_col="year", month_col="month", out_col="period")
    elif period_mode == "month":
        df = attach_year_month_period(df, year_col="year", month_col="month", out_col="period")
    else:
        return JSONResponse({"error": "period_mode must be 'quarter' or 'month'"}, status_code=400)

    table = concentration_table(df, group_col=group_col, value_col=value_col, period_col="period")
    out_name = f"outputs/concentration_{uuid.uuid4().hex[:8]}.xlsx"
    out_path = export_concentration_excel(table, out_name)
    preview = table.fillna(0.0).round(2).to_dict()
    return {"preview": preview, "download": f"/download/{out_name.split('/')[-1]}"}

@app.get("/download/{fname}")
def download(fname: str):
    path = f"outputs/{fname}"
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=fname,
    )
