from __future__ import annotations
import pandas as pd
from typing import Dict, List

def _norm(c: str) -> str:
    return c.strip().lower().replace(" ", "_")

def load_excel_auto(file_path: str) -> pd.DataFrame:

    df = pd.read_excel(file_path)
    df.columns = [_norm(c) for c in df.columns]
    return df

def summarize_schema(df: pd.DataFrame) -> Dict[str, List[str]]:

    numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    categorical = [c for c in df.columns if c not in numeric]
    return {"categorical": categorical, "numeric": numeric}
