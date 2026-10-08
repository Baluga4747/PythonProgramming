import pandas as pd

df = pd.DataFrame({
    "unit_price": [4.50, None],
    "quantity": [10, 3]
})

# Separate rows with unknown prices for review
review = df[df["unit_price"].isna()]
accepted = df[df["unit_price"].notna()].copy()

# Calculate revenue only for accepted records
accepted["revenue"] = accepted["unit_price"] * accepted["quantity"]


print("Records for review:")
print(review)

print("Accepted records:")
print(accepted)

print(f"Accepted revenue: ${accepted['revenue'].sum():.2f}")