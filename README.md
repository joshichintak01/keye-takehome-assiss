# Keye — Data Infrastructure & Analytics (POC)

This repo contains a minimal, working proof-of-concept for:
- Ingesting an Excel file (no schema hard-coding; columns are normalized automatically)
- Building a period column from `Year`/`Month` (Quarterly or Monthly)
- Running a **Concentration Analysis** (Top 10% / 20% / 50% + Total) for any chosen group and metric, per period
- Returning results as both JSON (via API) and a downloadable Excel file

The code is intentionally small and readable. It is organized so transformations are easy to audit and extend.

---

## Folder Structure

.
├─ api/
│ └─ main.py # FastAPI service (upload, schema, analyze, download)
├─ src/
│ ├─ ingest.py # Excel load + column normalization + schema summary
│ ├─ periods.py # Helpers to build period from Year/Month (quarter or month)
│ ├─ analysis.py # Concentration analysis
│ ├─ exporters.py # Excel export for results
│ └─ run_local.py # CLI runner (no API needed)
├─ tests/
│ └─ test_concentration.py # Basic sanity test
├─ uploads/ # Stores last uploaded Excel (API flow)
├─ outputs/ # Generated analysis result files (Excel)
└─ requirements.txt


Create the folders above if they don't exist.

---

## Prerequisites

- Python 3.10+ installed
- Windows PowerShell or VS Code terminal

---

## Setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
