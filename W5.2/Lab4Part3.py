import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_clean.csv"


#bug3:
df = pd.DataFrame({
    "sale_id": ["S001", "S005"],
    "product_id": ["P100", "P100"],
    "revenue": [45.00, 27.00]
})
df = df.drop_duplicates(subset=["sale_id"])

print(f"Total revenue: ${df['revenue'].sum():.2f}")