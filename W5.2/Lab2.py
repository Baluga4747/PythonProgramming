import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_messy.csv"

# Check that the source file exists
if not file_path.exists():
    print("Error: sales_messy.csv was not found.")
    exit()

# Load all columns as strings
df = pd.read_csv(file_path, dtype=str)

# Preserve the original source DataFrame
source_df = df.copy()

# Check that all required columns exist
required_columns = [
    "sale_id",
    "product_id",
    "product",
    "category",
    "unit_price",
    "quantity",
    "region"
]

missing_columns = [column for column in required_columns if column not in df.columns]

if missing_columns:
    print("Error: Missing required columns:", missing_columns)
    exit()

source_count = len(df)

# Trim whitespace and convert blank strings to missing values
df = df.apply(lambda column: column.str.strip())
df = df.replace("", pd.NA)

# Remove extra exact duplicates
duplicate_rows = df.duplicated(keep="first")
duplicate_count = duplicate_rows.sum()
df = df[~duplicate_rows].copy()

# Reject conflicting sale IDs after duplicate removal
conflicting_ids = df.groupby("sale_id")["product_id"].nunique(dropna=True)
conflicting_ids = conflicting_ids[conflicting_ids > 1].index

conflicting_rows = df["sale_id"].isin(conflicting_ids)

# Preserve original values for rejected records
rejected = df[conflicting_rows].copy()
df = df[~conflicting_rows].copy()

# Convert price and quantity to numbers
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Fill only missing categories
df["category"] = df["category"].fillna("Unknown")

# Identify records with missing required fields
missing_required = df[required_columns].isna().any(axis=1)

# Identify invalid prices
invalid_prices = df["unit_price"].isna() | (df["unit_price"] < 0)

# Identify invalid quantities
invalid_quantities = (
    df["quantity"].isna()
    | (df["quantity"] < 0)
    | (df["quantity"] % 1 != 0)
)

# Combine all rejected records
reject_mask = missing_required | invalid_prices | invalid_quantities

new_rejected = df[reject_mask].copy()
accepted = df[~reject_mask].copy()

# Add rejected records to the rejection DataFrame
rejected = pd.concat([rejected, new_rejected], ignore_index=True)

# Calculate revenue for accepted records
accepted["revenue"] = accepted["unit_price"] * accepted["quantity"]

# Export cleaned and rejected files
clean_file_path = Path(__file__).resolve().parent / "sales_clean.csv"
rejected_file_path = Path(__file__).resolve().parent / "sales_rejected.csv"

accepted.to_csv(clean_file_path, index=False)
rejected.to_csv(rejected_file_path, index=False)

# Print results
accepted_count = len(accepted)
rejected_count = len(rejected)

print("Source rows:", source_count)
print("Exact duplicates removed:", duplicate_count)
print("Accepted rows:", accepted_count)
print("Rejected rows:", rejected_count)
print("Rows accounted for:", duplicate_count + accepted_count + rejected_count)

print("Accepted units:", int(accepted["quantity"].sum()))
print("Accepted revenue: ${:.2f}".format(accepted["revenue"].sum()))

print("Clean file:", clean_file_path)
print("Rejected file:", rejected_file_path)