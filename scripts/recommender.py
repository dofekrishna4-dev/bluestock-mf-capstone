import sqlite3
import pandas as pd

print("Mutual Fund Recommendation System")
print("-" * 40)

conn = sqlite3.connect("data/db/bluestock_mf.db")

df = pd.read_sql(
    "SELECT * FROM '07_scheme_performance'",
    conn
)

df["performance_score"] = (
    df["return_5yr_pct"] * 0.35
    + df["return_3yr_pct"] * 0.25
    + df["sharpe_ratio"] * 15
    + df["sortino_ratio"] * 10
    - abs(df["max_drawdown_pct"]) * 0.20
    - df["expense_ratio_pct"] * 5
    + df["morningstar_rating"] * 5
)

print("\nAvailable Categories:\n")
print(df["category"].unique())

category = input("\nEnter category: ")

result = (
    df[df["category"] == category]
    .sort_values("performance_score", ascending=False)
)

print("\nRecommended Mutual Funds\n")

print(
    result[
        [
            "scheme_name",
            "fund_house",
            "category",
            "performance_score",
            "return_5yr_pct",
            "morningstar_rating",
            "risk_grade",
        ]
    ].head(5)
)

conn.close()