from __future__ import annotations
import pandas as pd

def attach_quarter_period(df: pd.DataFrame, year_col="year", month_col="month", out_col="period") -> pd.DataFrame:
    out = df.copy()
    if year_col not in out.columns or month_col not in out.columns:
        raise ValueError("Year/Month columns not found in input.")
    y = pd.to_numeric(out[year_col], errors="coerce").astype("Int64")
    m = pd.to_numeric(out[month_col], errors="coerce").astype("Int64")
    q = ((m - 1) // 3 + 1).astype("Int64")
    out[out_col] = y.astype(str) + "-Q" + q.astype(str)
    return out

def attach_year_month_period(df: pd.DataFrame, year_col="year", month_col="month", out_col="period") -> pd.DataFrame:
    out = df.copy()
    if year_col not in out.columns or month_col not in out.columns:
        raise ValueError("Year/Month columns not found in input.")
    y = pd.to_numeric(out[year_col], errors="coerce").astype("Int64")
    m = pd.to_numeric(out[month_col], errors="coerce").astype("Int64")
    out[out_col] = y.astype(str) + "-" + m.astype(str).str.zfill(2)
    return out
