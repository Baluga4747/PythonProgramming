import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent / "sales_clean.csv"

#bug1: changed "five" tp "5.00" to fix error
df = pd.DataFrame({"unit_price": ["4.50", "5.00", "8.00"]})
df["unit_price"] = df["unit_price"].astype(float)
print(df)
