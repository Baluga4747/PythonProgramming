import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("Error: sales.csv was not found.")
    exit()

df["revenue"] = df["quantity"] * df["unit_price"]

total_rev = df["revenue"].sum()
total_quan = df["quantity"].sum()
num_sales = len(df)
mean_rev = df["revenue"].mean()

print(f"Total revenue: ${total_rev:.2f}")
print(f"Total quantity: {total_quan}")
print(f"Number of sales: {num_sales}")
print(f"Mean revenue per sale: ${mean_rev:.2f}")

print("Top 3 sales:")
print(df.sort_values(by="revenue", ascending=False).head(3))

region = input("\nEnter a region: ").strip().title()
region_sales = df[df["region"] == region]

if len(region_sales) == 0:
    print(f"No sales were found for the region '{region}'.")
else:
    region_count = len(region_sales)
    region_revenue = region_sales["revenue"].sum()

    print(f"Region: {region}")
    print(f"Record count: {region_count}")
    print(f"Revenue: ${region_revenue:.2f}")