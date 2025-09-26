import pandas as pd
from src.periods import attach_quarter_period
from src.analysis import concentration_table

def test_quarter_concentration_basic():
    df = pd.DataFrame({
        "year": [2020, 2020, 2020, 2020],
        "month": [1, 2, 3, 4],
        "customer_code": ["A", "B", "C", "D"],
        "revenue": [100, 60, 40, 20],
    })
    df = attach_quarter_period(df, "year", "month", "period")
    tbl = concentration_table(df, "customer_code", "revenue", "period")
    assert "2020-Q1" in tbl.columns
    assert "2020-Q2" in tbl.columns
    assert tbl.loc["Total", "2020-Q1"] == 200
    assert tbl.loc["Top 10%", "2020-Q1"] == 100
