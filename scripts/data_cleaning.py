import pandas as pd
from pathlib import Path

raw_path = Path("data/raw")
processed_path = Path("data/processed")

processed_path.mkdir(exist_ok=True)

for file in raw_path.glob("*.csv"):

    print(f"\nCleaning {file.name}")

    df = pd.read_csv(file)

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

    output_file = processed_path / file.name

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")

print("\nAll datasets cleaned successfully!")