
import pandas as pd
from pathlib import Path

# Locate raw dataset
files = list(Path("data/raw").glob("*.csv"))

if not files:
    raise FileNotFoundError("No CSV file found in data/raw")

df = pd.read_csv(files[0])

print("Original shape:", df.shape)

# 1. Remove completely empty rows
df = df.dropna(how="all")

# 2. Remove exact duplicate records
df = df.drop_duplicates()

print("Shape after removing empty and duplicate rows:", df.shape)

# 3. Standardize column names
df.columns = [
    "date",
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges"
]

# 4. Convert date
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

# 5. Convert numerical columns
numeric_columns = [
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges"
]

for col in numeric_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# 6. Remove rows with invalid dates
df = df.dropna(subset=["date"])

# 7. Sort chronologically
df = df.sort_values("date").reset_index(drop=True)

# 8. Check remaining missing values
print("\nMissing values:")
print(df.isnull().sum())

# 9. Check duplicates again
print("\nRemaining duplicates:", df.duplicated().sum())

# 10. Check date range
print("\nDate range:")
print("Start:", df["date"].min())
print("End:", df["date"].max())

# 11. Save cleaned data
output_path = Path("data/processed/cleaned_uac_data.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to:", output_path)
print("Final dataset shape:", df.shape)

print("\nFirst 5 cleaned rows:")
print(df.head())

print("\nCleaning completed successfully!")
