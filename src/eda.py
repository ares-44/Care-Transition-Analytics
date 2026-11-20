
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/analytics_data.csv",
    parse_dates=["date"]
)

fig_dir = Path("results/figures")
fig_dir.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# ==========================================
# 1. DAILY INTAKE VS DISCHARGES
# ==========================================

plt.figure(figsize=(14, 6))

plt.plot(
    df["date"],
    df["cbp_apprehensions"],
    label="CBP Apprehensions",
    alpha=0.8
)

plt.plot(
    df["date"],
    df["hhs_discharges"],
    label="HHS Discharges",
    alpha=0.8
)

plt.title("Daily Apprehensions vs HHS Discharges")
plt.xlabel("Date")
plt.ylabel("Number of Children")
plt.legend()
plt.tight_layout()

plt.savefig(fig_dir / "intake_vs_discharges.png", dpi=300)
plt.close()

# ==========================================
# 2. CBP AND HHS CARE LOAD
# ==========================================

plt.figure(figsize=(14, 6))

plt.plot(
    df["date"],
    df["cbp_custody"],
    label="Children in CBP Custody"
)

plt.plot(
    df["date"],
    df["hhs_care"],
    label="Children in HHS Care"
)

plt.title("CBP and HHS Care Load Over Time")
plt.xlabel("Date")
plt.ylabel("Children in Care")
plt.legend()
plt.tight_layout()

plt.savefig(fig_dir / "care_load_trend.png", dpi=300)
plt.close()

# ==========================================
# 3. TRANSFER EFFICIENCY
# ==========================================

plt.figure(figsize=(14, 6))

plt.plot(
    df["date"],
    df["transfer_efficiency"] * 100,
    label="Transfer Efficiency Indicator"
)

plt.axhline(
    100,
    linestyle="--",
    label="100% Reference"
)

plt.title("CBP Transfer Efficiency Indicator")
plt.xlabel("Date")
plt.ylabel("Ratio (%)")
plt.legend()
plt.tight_layout()

plt.savefig(fig_dir / "transfer_efficiency.png", dpi=300)
plt.close()

# ==========================================
# 4. DISCHARGE EFFECTIVENESS
# ==========================================

plt.figure(figsize=(14, 6))

plt.plot(
    df["date"],
    df["discharge_effectiveness"] * 100,
    label="Discharge-to-HHS-Care Ratio"
)

plt.title("Daily Discharge-to-HHS-Care Ratio")
plt.xlabel("Date")
plt.ylabel("Ratio (%)")
plt.legend()
plt.tight_layout()

plt.savefig(fig_dir / "discharge_effectiveness.png", dpi=300)
plt.close()

# ==========================================
# 5. MONTHLY TRENDS
# ==========================================

monthly = df.groupby("year_month").agg(
    apprehensions=("cbp_apprehensions", "mean"),
    transfers=("cbp_transfers", "mean"),
    discharges=("hhs_discharges", "mean"),
    cbp_care=("cbp_custody", "mean"),
    hhs_care=("hhs_care", "mean")
).reset_index()

plt.figure(figsize=(14, 6))

plt.plot(
    monthly["year_month"],
    monthly["apprehensions"],
    label="Avg Apprehensions"
)

plt.plot(
    monthly["year_month"],
    monthly["transfers"],
    label="Avg Transfers"
)

plt.plot(
    monthly["year_month"],
    monthly["discharges"],
    label="Avg Discharges"
)

plt.title("Monthly Average Pipeline Activity")
plt.xlabel("Month")
plt.ylabel("Average Daily Count")
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()

plt.savefig(fig_dir / "monthly_pipeline_trend.png", dpi=300)
plt.close()

# ==========================================
# 6. WEEKDAY ANALYSIS
# ==========================================

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_data = df.groupby("weekday").agg(
    apprehensions=("cbp_apprehensions", "mean"),
    transfers=("cbp_transfers", "mean"),
    discharges=("hhs_discharges", "mean")
).reindex(weekday_order)

weekday_data.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Average Pipeline Activity by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Average Count")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(fig_dir / "weekday_analysis.png", dpi=300)
plt.close()

# ==========================================
# 7. DISCHARGE DISTRIBUTION
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    df["hhs_discharges"],
    bins=30,
    kde=True
)

plt.title("Distribution of Daily HHS Discharges")
plt.xlabel("Daily Discharges")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig(fig_dir / "discharge_distribution.png", dpi=300)
plt.close()

# ==========================================
# 8. CORRELATION ANALYSIS
# ==========================================

correlation_columns = [
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges"
]

correlation = df[correlation_columns].corr()

plt.figure(figsize=(10, 8))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True
)

plt.title("Care Pipeline Variable Correlation")
plt.tight_layout()

plt.savefig(fig_dir / "correlation_heatmap.png", dpi=300)
plt.close()

# ==========================================
# 9. SUMMARY STATISTICS
# ==========================================

summary = df[
    correlation_columns
].describe()

summary.to_csv("results/eda_summary_statistics.csv")

# ==========================================
# 10. MONTHLY DATA EXPORT
# ==========================================

monthly.to_csv(
    "results/monthly_analysis.csv",
    index=False
)

weekday_data.to_csv(
    "results/weekday_analysis.csv"
)

correlation.to_csv(
    "results/correlation_matrix.csv"
)

# ==========================================
# FINAL
# ==========================================

print("\n========== EDA COMPLETE ==========")

print("\nSummary Statistics:")
print(summary)

print("\nMonthly Analysis:")
print(monthly.head())

print("\nWeekday Analysis:")
print(weekday_data)

print("\nCorrelation Matrix:")
print(correlation)

print("\nCharts saved in:", fig_dir)
print("EDA outputs saved in results/")
