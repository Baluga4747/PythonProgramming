import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_clean.csv"

df = pd.DataFrame({"category": ["Gifts"], "revenue": [138.00]})
output_path = Path(__file__).resolve().parent / "debug_summary.csv"
df.to_csv(output_path, index=False)
print(pd.read_csv(output_path).columns)