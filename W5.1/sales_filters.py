import pandas as pd
from pathlib import Path


file_path = Path(__file__).resolve().parent / "sales.csv"
df = pd.read_csv(file_path)

print(df.loc[df["quantity"] >= 10, ["sale_id", "product", "quantity"]])

print(df.loc[(df["region"] == "North") & (df["quantity"] >= 5), ["sale_id", "product", "quantity", "region"]])

print(df.loc[df["category"] == "Gifts", ["sale_id", "product", "unit_price"]].sort_values(by="unit_price", ascending=False))