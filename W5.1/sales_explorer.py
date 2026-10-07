import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales.csv"
df = pd.read_csv(file_path)

print(df.head(5))
print(df.columns)
print(df.shape)
print(df.dtypes)


df.info()

print(df[["sale_id", "product", "region"]])