from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

raw_file = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
output_folder = PROJECT_ROOT / "data" / "processed"
output_file = output_folder / "online_retail_cleaned.csv"

output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(raw_file)

print("Original dataset shape:", df.shape)

# Remove rows without customer IDs
df = df.dropna(subset=["CustomerID"]).copy()

# Remove duplicate records
df = df.drop_duplicates().copy()

# Keep valid sales quantities and prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()

# Create total sales amount
df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("Cleaned dataset shape:", df.shape)
print("Cleaned file saved to:", output_file)
print("Cleaning completed successfully!")