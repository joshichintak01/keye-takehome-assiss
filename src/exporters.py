from __future__ import annotations
import pandas as pd
from pathlib import Path

def export_concentration_excel(table: pd.DataFrame, out_path: str) -> str:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as xlw:
        table.to_excel(xlw, sheet_name="concentration", index=True)
    return str(out)
