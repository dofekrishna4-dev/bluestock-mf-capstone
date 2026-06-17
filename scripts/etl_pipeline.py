import sqlite3
import pandas as pd
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

raw_path = Path("data/raw")
processed_path = Path("data/processed")
db_path = "data/db/bluestock_mf.db"

processed_path.mkdir(parents=True, exist_ok=True)

# ============================================================
# STEP 1 : DATA INSPECTION
# ============================================================

print("\n" + "=" * 70)
print("STEP 1 : DATA INSPECTION")
print("=" * 70)

files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in files:

    print("\n" + "=" * 60)
    print(f"FILE : {file}")
    print("=" * 60)

    df = pd.read_csv(raw_path / file)

    print("\nShape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicates:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())


# ============================================================
# STEP 2 : DATA CLEANING
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 : DATA CLEANING")
print("=" * 70)

for file in files:

    print(f"\nCleaning {file}")

    df = pd.read_csv(raw_path / file)

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert date columns
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # NAV validation
    if "nav" in df.columns:
        df = df[df["nav"] > 0]

    # Expense ratio validation
    if "expense_ratio_pct" in df.columns:
        df = df[
            (df["expense_ratio_pct"] >= 0.1)
            & (df["expense_ratio_pct"] <= 2.5)
        ]

    output_file = processed_path / file

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")

print("\nAll datasets cleaned successfully!")


# ============================================================
# STEP 3 : DATABASE CREATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 3 : DATABASE CREATION")
print("=" * 70)

conn = sqlite3.connect(db_path)

for file in processed_path.glob("*.csv"):

    table_name = file.stem

    print(f"Loading {table_name}")

    df = pd.read_csv(file)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

conn.close()

print("\nDatabase created successfully!")
print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")