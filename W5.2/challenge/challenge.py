import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "Sales_messy_challenge.csv"
df = pd.read_csv(file_path, dtype=str)
source_count = len(df)

#inspect missing values and exact duplicates
print("Missing Values:")
print(df.isna().sum())
print("Exact Duplicates:")
print(df[df.duplicated(keep=False)])

# Clean whitespace and remove extra duplicates
df = df.apply(lambda col: col.str.strip()).replace("", pd.NA)
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates().copy()

#Convert price and quantity to numbers
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["category"] = df["category"].fillna("Unknown")

#Separate valid sales from rejected records
def validate_sales(data):
    missing = data[["sale_id", "product_id", "product",
                    "category", "unit_price", "quantity", "region"]].isna().any(axis=1)
    invalid_price = data["unit_price"].isna() | (data["unit_price"] <= 0)
    invalid_quantity = (
        data["quantity"].isna()
        | (data["quantity"] <= 0)
        | (data["quantity"] % 1 != 0)
    )

    rejected = data[missing | invalid_price | invalid_quantity].copy()
    accepted = data[~(missing | invalid_price | invalid_quantity)].copy()
    return accepted, rejected

accepted, rejected = validate_sales(df)

#calculate revenue and export the results
accepted["revenue"] = accepted["unit_price"] * accepted["quantity"]
folder = Path(__file__).resolve().parent

accepted.to_csv(folder / "challenge_clean.csv", index=False)
rejected.to_csv(folder / "challenge_review.csv", index=False)

# Summarize sales by category
summary = accepted.groupby("category", as_index=False).agg(
    quantity=("quantity", "sum"),
    revenue=("revenue", "sum")
).sort_values("revenue", ascending=False)

summary.to_csv(folder / "challenge_summary.csv", index=False)

#Check record counts and revenue totals
print("Source Rows:", source_count)
print("Duplicates Removed:", duplicate_count)
print("Accepted Rows:", len(accepted))
print("Rejected Rows:", len(rejected))
print("Rows Accounted For:", duplicate_count + len(accepted) + len(rejected))
print("Total Units:", int(accepted["quantity"].sum()))
print("Total Revenue: ${:.2f}".format(accepted["revenue"].sum()))
print(summary.to_string(index=False))
print("Revenue Totals Match:",
      round(summary["revenue"].sum(), 2) == round(accepted["revenue"].sum(), 2))