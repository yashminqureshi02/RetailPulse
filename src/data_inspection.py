from pathlib import Path
import pandas as pd

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Look for the original dataset
data_file = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"

if not data_file.exists():
    print("Dataset not found!")
    print("Please check the data/raw folder.")
else:
    print("Dataset found successfully!")

    # Load the Excel dataset
    df = pd.read_excel(data_file)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset shape (rows, columns):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values in each column:")
    print(df.isnull().sum())