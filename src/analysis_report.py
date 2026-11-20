
import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "analytics_data.csv"
OUTPUT_PATH = ROOT / "results" / "analysis_findings.txt"

df = pd.read_csv(DATA_PATH)
print("\nALL COLUMN NAMES:")
for col in df.columns:
    print(col)
print("COLUMNS:", df.columns.tolist())
df["date"] = pd.to_datetime(df["date"])

lines = []

def add(text=""):
    lines.append(str(text))

add("=" * 65)
add("CARE TRANSITION ANALYTICS - DATA ANALYSIS FINDINGS")
add("=" * 65)

# Dataset overview
add("\n1. DATASET OVERVIEW")
add("-" * 40)
add(f"Total observations: {len(df)}")
add(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
add(f"Unique dates: {df['date'].nunique()}")
add(f"Missing values: {df.isna().sum().sum()}")

# Overall metrics
add("\n2. OVERALL OPERATIONAL METRICS")
add("-" * 40)

metrics = [
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges"
]

for col in metrics:
    add(f"{col}:")
    add(f"  Total: {df[col].sum():,.2f}")
    add(f"  Mean: {df[col].mean():,.2f}")
    add(f"  Median: {df[col].median():,.2f}")
    add(f"  Maximum: {df[col].max():,.2f}")
    add(f"  Minimum: {df[col].min():,.2f}")

# Ratios
add("\n3. TRANSITION INDICATORS")
add("-" * 40)

for col in ["transfer_efficiency", "discharge_effectiveness"]:
    add(f"{col}:")
    add(f"  Mean: {df[col].mean():.4f}")
    add(f"  Median: {df[col].median():.4f}")
    add(f"  Std: {df[col].std():.4f}")

# Correlations
add("\n4. CORRELATION ANALYSIS")
add("-" * 40)

corr = df[metrics].corr()

pairs = []
for i in range(len(metrics)):
    for j in range(i + 1, len(metrics)):
        pairs.append((metrics[i], metrics[j], corr.iloc[i, j]))

pairs.sort(key=lambda x: abs(x[2]), reverse=True)

for a, b, value in pairs:
    add(f"{a} vs {b}: {value:.4f}")

# Monthly trends
add("\n5. MONTHLY TREND ANALYSIS")
add("-" * 40)

df["year_month"] = df["date"].dt.to_period("M")

monthly = df.groupby("year_month")[metrics].mean()

for col in ["cbp_apprehensions", "cbp_transfers", "hhs_discharges"]:
    highest = monthly[col].idxmax()
    lowest = monthly[col].idxmin()

    add(f"\n{col}:")
    add(f"  Highest monthly average: {highest} ({monthly[col].max():.2f})")
    add(f"  Lowest monthly average: {lowest} ({monthly[col].min():.2f})")

monthly.to_csv(ROOT / "results" / "monthly_metrics_report.csv")


# Alert analysis
add("\n6. OPERATIONAL ALERT ANALYSIS")
add("-" * 40)

alert_columns = [
    "cbp_imbalance_alert",
    "hhs_imbalance_alert",
    "discharge_drop_alert"
]

for col in alert_columns:
    count = df[col].sum()
    percentage = (count / len(df)) * 100
    add(f"{col}: {count} observations ({percentage:.2f}%)")

# Yearly summary
add("\n7. YEARLY SUMMARY")
add("-" * 40)

yearly = df.groupby(df["date"].dt.year)[metrics].mean()

add(yearly.round(2).to_string())

yearly.to_csv(ROOT / "results" / "yearly_summary.csv")

# Observed data gaps
add("\n8. REPORTING INTERVAL ANALYSIS")
add("-" * 40)

date_diffs = df["date"].sort_values().diff().dt.days.dropna()

add(f"Average interval between observations: {date_diffs.mean():.2f} days")
add(f"Median interval: {date_diffs.median():.2f} days")
add(f"Intervals greater than 1 day: {(date_diffs > 1).sum()}")
add(f"Maximum gap: {date_diffs.max()} days")

# Save report
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

print("\n".join(lines))
print(f"\nReport saved to: {OUTPUT_PATH}")
