import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_clean.csv"

# Check that the cleaned file exists
if not file_path.exists():
    print("Error: sales_clean.csv was not found. Please run Lab 2 first.")
    exit()

# Load the cleaned sales data
df = pd.read_csv(file_path)

# Calculate overall results
record_count = len(df)
total_units = df["quantity"].sum()
total_revenue = df["revenue"].sum()
mean_revenue = df["revenue"].mean()

print("Overall Sales Summary")
print("Accepted records:", record_count)
print("Total units:", int(total_units))
print("Total revenue: ${:.2f}".format(total_revenue))
print("Mean revenue per sale: ${:.2f}".format(mean_revenue))

# Group sales by category
category_summary = df.groupby("category", as_index=False).agg(
    quantity=("quantity", "sum"),
    revenue=("revenue", "sum")
)

# Sort category summary by revenue
category_summary = category_summary.sort_values(
    "revenue", ascending=False
)

# Group sales by region
region_summary = df.groupby("region", as_index=False).agg(
    quantity=("quantity", "sum"),
    revenue=("revenue", "sum")
)

# Sort region summary by revenue
region_summary = region_summary.sort_values(
    "revenue", ascending=False
)

# Export summary files
category_file_path = Path(__file__).resolve().parent / "category_summary.csv"
region_file_path = Path(__file__).resolve().parent / "region_summary.csv"

category_summary.to_csv(category_file_path, index=False)
region_summary.to_csv(region_file_path, index=False)

# Display category summary
print("Category Summary")
print(category_summary.to_string(index=False))

# Display region summary
print("Region Summary")
print(region_summary.to_string(index=False))

# Compare grouped totals with overall revenue
category_total = category_summary["revenue"].sum()
region_total = region_summary["revenue"].sum()

print("Revenue Checks")
print("Overall revenue: ${:.2f}".format(total_revenue))
print("Category summary revenue: ${:.2f}".format(category_total))
print("Region summary revenue: ${:.2f}".format(region_total))

print("Category total matches overall:",
      category_total == total_revenue)

print("Region total matches overall:",
      region_total == total_revenue)

print("Category summary file:", category_file_path)
print("Region summary file:", region_file_path)