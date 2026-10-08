import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_messy.csv"
df = pd.read_csv(file_path, dtype=str)

print("Shape:", df.shape)

print("Column Names:")
print(df.columns.tolist())

print("Missing Value Counts:")
print(df.isna().sum())

print("Exact Duplicate Groups:")
print(df[df.duplicated(keep=False)])

print("Repeated Sale-ID Groups:")
repeated_ids = df["sale_id"].duplicated(keep=False) & df["sale_id"].notna()
print(df[repeated_ids])

print("Values That Need Validation:")
print(df.loc[[11, 12], ["sale_id", "unit_price", "quantity"]])

