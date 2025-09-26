from __future__ import annotations
import argparse
import pandas as pd
from src.ingest import load_excel_auto
from src.periods import attach_quarter_period, attach_year_month_period
from src.analysis import concentration_table
from src.exporters import export_concentration_excel

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="run_local",
        description="Concentration analysis (Top 10/20/50% per period) on an Excel file."
    )
    parser.add_argument("excel_path", help="Path to Excel (e.g., .\\uploads\\latest.xlsx)")
    parser.add_argument("--group", required=True, help="Group column (e.g., customer_code, industry, revenue_type, product, product_mix)")
    parser.add_argument("--value", required=True, help="Value column (e.g., revenue or gross_profit)")
    parser.add_argument("--period", choices=["quarter", "month"], required=True, help="How to build 'period' from Year/Month")
    parser.add_argument("--out", default="outputs/concentration_local.xlsx", help="Output Excel path")
    args = parser.parse_args()

    df = load_excel_auto(args.excel_path)
    if args.period == "quarter":
        df = attach_quarter_period(df, year_col="year", month_col="month", out_col="period")
    else:
        df = attach_year_month_period(df, year_col="year", month_col="month", out_col="period")

    table = concentration_table(df, group_col=args.group, value_col=args.value, period_col="period")
    out_path = export_concentration_excel(table, args.out)

    with pd.option_context("display.max_columns", None):
        print(table)
    print(f"\nWrote: {out_path}")

if __name__ == "__main__":
    main()
