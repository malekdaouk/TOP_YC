import pandas as pd
from io import BytesIO
from pathlib import Path
from openpyxl import load_workbook

BASE_DIR = Path(__file__).resolve().parent


# -----------------------------------------------------
# BUILD MASTER SPREADSHEET FROM USER INPUT
# -----------------------------------------------------



# -----------------------------------------------------
# PREPARE DATA FOR CALCULATIONS
# -----------------------------------------------------


def prepare_data(master_file):

    df = pd.read_excel(master_file)

    sector_path = BASE_DIR / "data_files" / "StocksSectorMOCK.xlsx"
    stocks_sectors = pd.read_excel(sector_path)

    # standardize column names
    df.columns = df.columns.str.strip()
    stocks_sectors.columns = stocks_sectors.columns.str.strip()

    # ---- FORCE TEXT COLUMNS TO BE OBJECT STRINGS (safe with df.fillna(0) in math_engine) ----
    text_cols = [
        "equity_style",
        "fixed_income_style",
        "hq_country",
        "detailed_security_type",
        "broad_asset_class",
        "category_name",
        "index_fund",
        "Name",
        "fund_family",
        "share_class",
        "Q/NQ",
        "Account",
        "Symbol",
        "Sector",
    ]

    for col in text_cols:
        if col in df.columns:
            # keep dtype as object (not pandas StringDtype) so df.fillna(0) won't crash
            df[col] = df[col].where(df[col].notna(), None).astype(str)

    # merge sector mapping
    if "Symbol" in df.columns and "Symbol" in stocks_sectors.columns:
        if "Sector" in stocks_sectors.columns:
            df = df.merge(
                stocks_sectors[["Symbol", "Sector"]],
                on="Symbol",
                how="left"
            )

    # snapshot before modifications
    style_rows_with_ERR = df.copy()

    # numeric conversion
    exclude_cols = [
        "Q/NQ",
        "Account",
        "Symbol",
        "broad_asset_class",
        "detailed_security_type",
        "category_name",
        "index_fund",
        "equity_style",
        "fixed_income_style",
        "Name",
        "fund_family",
        "share_class",
        "hq_country",
        "Sector",
    ]

    numeric_cols = [c for c in df.columns if c not in exclude_cols]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # normalize alpha columns
    alpha_cols = [
        "alpha_1y_vs_category",
        "alpha_3y_vs_category",
        "alpha_5y_vs_category",
    ]

    for col in alpha_cols:
        if col in df.columns:
            df[col] = df[col] / 100

    return df, style_rows_with_ERR