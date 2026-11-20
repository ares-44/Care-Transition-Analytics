
import pandas as pd
from pathlib import Path

files = list(Path("data/raw").glob("*.csv"))

if not files:
    print("No CSV file found in data/raw")
    exit()

file_path = files[0]
df = pd.read_csv(file_path)

print("\n========== DATASET INFORMATION ==========")
print("File:", file_path.name)
print("Shape:", df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

print("\n========== STATISTICS ==========")
print(df.describe(include="all"))
