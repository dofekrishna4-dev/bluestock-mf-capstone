import sqlite3
import pandas as pd
from pathlib import Path

db_path = "data/db/bluestock_mf.db"

conn = sqlite3.connect(db_path)

processed_path = Path("data/processed")

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

print("\nDatabase created successfully!")

conn.close()