import pandas as pd
from pathlib import Path

data_path = Path("data/raw")

for file in data_path.glob("*.csv"):
    print("\n" + "="*60)
    print(file.name)
    print("="*60)

    df = pd.read_csv(file)

    print("\nShape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicates:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 3 rows:")
    print(df.head(3))