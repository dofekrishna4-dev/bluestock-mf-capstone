import sqlite3
import pandas as pd

print("Starting compute_metrics.py...\n")

DB_PATH = "data/db/bluestock_mf.db"

conn = sqlite3.connect(DB_PATH)

print("Database connected.")

df = pd.read_sql(
    "SELECT * FROM '07_scheme_performance'",
    conn
)

print(f"Rows loaded: {len(df)}")

df["performance_score"] = (
    df["return_5yr_pct"] * 0.35
    + df["return_3yr_pct"] * 0.25
    + df["sharpe_ratio"] * 15
    + df["sortino_ratio"] * 10
    - abs(df["max_drawdown_pct"]) * 0.20
    - df["expense_ratio_pct"] * 5
    + df["morningstar_rating"] * 5
)

top10 = (
    df.sort_values("performance_score", ascending=False)
      [["scheme_name", "category", "performance_score"]]
      .head(10)
)

print("\nTop 10 Mutual Funds Based on Performance Score\n")
print(top10.to_string(index=False))

conn.close()

print("\nPerformance metrics computed successfully.")