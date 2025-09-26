from __future__ import annotations
import math
import pandas as pd
from typing import Dict

def _require(df: pd.DataFrame, cols):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def _top_share(series: pd.Series, frac: float) -> float:
    n = len(series)
    if n == 0:
        return 0.0
    k = max(1, math.floor(n * frac))
    return float(series.sort_values(ascending=False).head(k).sum())

def concentration_table(df: pd.DataFrame, group_col: str, value_col: str, period_col: str) -> pd.DataFrame:

    _require(df, [group_col, value_col, period_col])

    work = df[[group_col, value_col, period_col]].copy()
    work[value_col] = pd.to_numeric(work[value_col], errors="coerce").fillna(0.0)

    results: Dict[str, Dict[str, float]] = {}
    for period, g in work.groupby(period_col, dropna=False):
        agg = g.groupby(group_col, dropna=False)[value_col].sum()
        total = float(agg.sum())
        top10 = _top_share(agg, 0.10)
        top20 = _top_share(agg, 0.20)
        top50 = _top_share(agg, 0.50)
        results[str(period)] = {"Top 10%": top10, "Top 20%": top20, "Top 50%": top50, "Total": total}

    out = pd.DataFrame(results)
    out = out.reindex(["Top 10%", "Top 20%", "Top 50%", "Total"])
    return out
