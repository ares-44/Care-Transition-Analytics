
import pandas as pd
import numpy as np
from pathlib import Path

# Load cleaned dataset
input_path = Path("data/processed/cleaned_uac_data.csv")
df = pd.read_csv(input_path, parse_dates=["date"])

df = df.sort_values("date").reset_index(drop=True)

# =====================================================
# 1. TRANSITION EFFICIENCY
# =====================================================

df["transfer_efficiency"] = np.where(
    df["cbp_custody"] > 0,
    df["cbp_transfers"] / df["cbp_custody"],
    np.nan
)

df["discharge_effectiveness"] = np.where(
    df["hhs_care"] > 0,
    df["hhs_discharges"] / df["hhs_care"],
    np.nan
)

# =====================================================
# 2. PIPELINE FLOW BALANCE INDICATORS
# =====================================================

# CBP: intake vs transfers
df["cbp_flow_balance"] = (
    df["cbp_apprehensions"] - df["cbp_transfers"]
)

# HHS: transfers arriving vs discharges
df["hhs_flow_balance"] = (
    df["cbp_transfers"] - df["hhs_discharges"]
)

# Combined daily flow balance indicator
df["combined_flow_balance"] = (
    df["cbp_apprehensions"] - df["hhs_discharges"]
)

# =====================================================
# 3. CARE LOAD INDICATORS
# =====================================================

df["combined_care_load"] = (
    df["cbp_custody"] + df["hhs_care"]
)

# =====================================================
# 4. THROUGHPUT INDICATOR
# =====================================================

df["pipeline_throughput"] = np.where(
    df["cbp_apprehensions"] > 0,
    df["hhs_discharges"] / df["cbp_apprehensions"],
    np.nan
)

# =====================================================
# 5. TEMPORAL FEATURES
# =====================================================

df["weekday"] = df["date"].dt.day_name()
df["day_of_week"] = df["date"].dt.dayofweek
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
df["year"] = df["date"].dt.year
df["year_month"] = df["date"].dt.to_period("M").astype(str)

# =====================================================
# 6. ROLLING TRENDS (7 OBSERVATIONS)
# =====================================================

rolling_columns = [
    "cbp_apprehensions",
    "cbp_transfers",
    "hhs_discharges",
    "cbp_custody",
    "hhs_care"
]

for col in rolling_columns:
    df[f"{col}_rolling_7"] = (
        df[col].rolling(window=7, min_periods=3).mean()
    )

# =====================================================
# 7. OUTCOME STABILITY
# =====================================================

df["discharge_rolling_std_7"] = (
    df["hhs_discharges"].rolling(
        window=7, min_periods=3
    ).std()
)

df["discharge_stability"] = (
    1 / (1 + df["discharge_rolling_std_7"])
)

# =====================================================
# 8. ALERT INDICATORS
# =====================================================

# Flow imbalance alert
df["cbp_imbalance_alert"] = (
    df["cbp_flow_balance"] > 0
)

df["hhs_imbalance_alert"] = (
    df["hhs_flow_balance"] > 0
)

# Discharge drop compared to rolling mean
df["discharge_drop_alert"] = (
    df["hhs_discharges"] <
    df["hhs_discharges_rolling_7"] * 0.70
)

# =====================================================
# 9. SAVE FEATURE-ENGINEERED DATA
# =====================================================

output_path = Path("data/processed/analytics_data.csv")
df.to_csv(output_path, index=False)

print("Feature engineering completed!")
print("Dataset shape:", df.shape)
print("Saved:", output_path)

print("\n========== KPI SUMMARY ==========")

print("\nAverage Transfer Efficiency:",
      round(df["transfer_efficiency"].mean() * 100, 2), "%")

print("Average Discharge Effectiveness:",
      round(df["discharge_effectiveness"].mean() * 100, 2), "%")

print("Average Pipeline Throughput Indicator:",
      round(df["pipeline_throughput"].mean() * 100, 2), "%")

print("\nCBP Imbalance Alerts:",
      df["cbp_imbalance_alert"].sum())

print("HHS Imbalance Alerts:",
      df["hhs_imbalance_alert"].sum())

print("Discharge Drop Alerts:",
      df["discharge_drop_alert"].sum())

print("\nFeature columns:")
print(df.columns.tolist())
