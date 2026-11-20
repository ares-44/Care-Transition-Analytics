
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = Path("data/processed/analytics_data.csv")

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.2);
        padding: 15px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return df.sort_values("date").reset_index(drop=True)

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load dataset: {e}")
    st.stop()

# =========================================================
# HEADER
# =========================================================

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.caption(
    "UAC Program | Operational monitoring and transition analytics"
)

st.markdown(
    """
    This dashboard analyzes reporting patterns across CBP custody,
    transfers into HHS care, care loads, and HHS discharges.
    """
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Dashboard Controls")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select reporting period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

if filtered.empty:
    st.warning("No records available for the selected date range.")
    st.stop()

ratio_display = st.sidebar.toggle(
    "Display ratios as percentages",
    value=True
)

show_alerts = st.sidebar.toggle(
    "Show alert indicators",
    value=True
)

st.sidebar.divider()

st.sidebar.info(
    "All date-based analyses use observed records. "
    "Missing reporting dates are not assumed to represent zero activity."
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

mean_transfer = filtered["transfer_efficiency"].mean()

mean_discharge = filtered["discharge_effectiveness"].mean()

mean_discharge_intake = (
    filtered["hhs_discharges"].sum() /
    filtered["cbp_apprehensions"].sum()
    if filtered["cbp_apprehensions"].sum() > 0
    else np.nan
)

total_apprehensions = filtered["cbp_apprehensions"].sum()
total_transfers = filtered["cbp_transfers"].sum()
total_discharges = filtered["hhs_discharges"].sum()

latest = filtered.iloc[-1]

# =========================================================
# OVERVIEW
# =========================================================

st.header("Executive Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Apprehensions",
    f"{total_apprehensions:,.0f}"
)

k2.metric(
    "Total CBP Transfers",
    f"{total_transfers:,.0f}"
)

k3.metric(
    "Total HHS Discharges",
    f"{total_discharges:,.0f}"
)

k4.metric(
    "Avg Transfer Indicator",
    f"{mean_transfer:.1%}" if pd.notna(mean_transfer) else "N/A"
)

k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "Avg HHS Care Load",
    f"{filtered['hhs_care'].mean():,.0f}"
)

k6.metric(
    "Avg CBP Custody",
    f"{filtered['cbp_custody'].mean():,.0f}"
)

k7.metric(
    "Discharge / HHS Care",
    f"{mean_discharge:.2%}" if pd.notna(mean_discharge) else "N/A"
)

k8.metric(
    "Discharges / Apprehensions",
    f"{mean_discharge_intake:.2%}"
    if pd.notna(mean_discharge_intake)
    else "N/A"
)

st.caption(
    "Ratios are descriptive indicators. They do not measure "
    "individual case processing time or cohort-based success."
)

# =========================================================
# PIPELINE SNAPSHOT
# =========================================================

st.header("Care Pipeline Snapshot")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("CBP Custody")
    st.metric(
        "Latest reported CBP custody",
        f"{latest['cbp_custody']:,.0f}"
    )
    st.metric(
        "Latest apprehensions",
        f"{latest['cbp_apprehensions']:,.0f}"
    )

with col2:
    st.subheader("CBP → HHS")
    st.metric(
        "Latest transfers",
        f"{latest['cbp_transfers']:,.0f}"
    )
    st.metric(
        "Transfer indicator",
        f"{latest['transfer_efficiency']:.1%}"
        if pd.notna(latest["transfer_efficiency"])
        else "N/A"
    )

with col3:
    st.subheader("HHS Care")
    st.metric(
        "Latest HHS care load",
        f"{latest['hhs_care']:,.0f}"
    )
    st.metric(
        "Latest discharges",
        f"{latest['hhs_discharges']:,.0f}"
    )

# =========================================================
# PIPELINE FLOW CHART
# =========================================================

st.header("Pipeline Flow Visualization")

pipeline_fig = go.Figure()

pipeline_fig.add_trace(
    go.Bar(
        x=["Apprehensions", "CBP Transfers", "HHS Discharges"],
        y=[
            total_apprehensions,
            total_transfers,
            total_discharges
        ],
        text=[
            f"{total_apprehensions:,.0f}",
            f"{total_transfers:,.0f}",
            f"{total_discharges:,.0f}"
        ],
        textposition="auto"
    )
)

pipeline_fig.update_layout(
    title="Total Observed Pipeline Activity",
    yaxis_title="Total recorded events",
    template="plotly_white"
)

st.plotly_chart(pipeline_fig, use_container_width=True)

st.caption(
    "This compares event totals during the selected period. "
    "The stages are not a matched cohort and these totals should "
    "not be interpreted as conversion rates."
)

# =========================================================
# TIME SERIES
# =========================================================

st.header("Pipeline Activity Over Time")

activity_options = st.multiselect(
    "Select metrics to visualize",
    [
        "Apprehensions",
        "CBP Transfers",
        "HHS Discharges",
        "CBP Custody",
        "HHS Care"
    ],
    default=[
        "Apprehensions",
        "CBP Transfers",
        "HHS Discharges"
    ]
)

column_mapping = {
    "Apprehensions": "cbp_apprehensions",
    "CBP Transfers": "cbp_transfers",
    "HHS Discharges": "hhs_discharges",
    "CBP Custody": "cbp_custody",
    "HHS Care": "hhs_care"
}

time_fig = go.Figure()

for option in activity_options:
    column = column_mapping[option]

    time_fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered[column],
            mode="lines",
            name=option
        )
    )

time_fig.update_layout(
    template="plotly_white",
    title="Daily Reporting Trends",
    xaxis_title="Date",
    yaxis_title="Children / Recorded Events",
    hovermode="x unified"
)

st.plotly_chart(time_fig, use_container_width=True)

# =========================================================
# EFFICIENCY ANALYSIS
# =========================================================

st.header("Transition Efficiency Analysis")

eff_col1, eff_col2 = st.columns(2)

with eff_col1:

    transfer_fig = px.line(
        filtered,
        x="date",
        y="transfer_efficiency",
        title="CBP Transfer Activity / CBP Custody"
    )

    if ratio_display:
        transfer_fig.update_yaxes(tickformat=".0%")

    transfer_fig.update_layout(
        template="plotly_white",
        yaxis_title="Ratio"
    )

    st.plotly_chart(
        transfer_fig,
        use_container_width=True
    )

with eff_col2:

    discharge_fig = px.line(
        filtered,
        x="date",
        y="discharge_effectiveness",
        title="HHS Discharges / HHS Care"
    )

    if ratio_display:
        discharge_fig.update_yaxes(tickformat=".0%")

    discharge_fig.update_layout(
        template="plotly_white",
        yaxis_title="Ratio"
    )

    st.plotly_chart(
        discharge_fig,
        use_container_width=True
    )

# =========================================================
# MONTHLY ANALYSIS
# =========================================================

st.header("Monthly Trend Analysis")

monthly = filtered.groupby("year_month").agg(
    apprehensions=("cbp_apprehensions", "mean"),
    transfers=("cbp_transfers", "mean"),
    discharges=("hhs_discharges", "mean"),
    cbp_care=("cbp_custody", "mean"),
    hhs_care=("hhs_care", "mean")
).reset_index()

monthly_fig = px.line(
    monthly,
    x="year_month",
    y=["apprehensions", "transfers", "discharges"],
    title="Monthly Average Daily Activity",
    markers=True
)

monthly_fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Average count per observation"
)

st.plotly_chart(monthly_fig, use_container_width=True)

# =========================================================
# WEEKDAY ANALYSIS
# =========================================================

st.header("Weekday Activity Analysis")

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_data = filtered.groupby("weekday").agg(
    apprehensions=("cbp_apprehensions", "mean"),
    transfers=("cbp_transfers", "mean"),
    discharges=("hhs_discharges", "mean")
).reindex(weekday_order)

weekday_data = weekday_data.dropna(how="all")

weekday_fig = px.bar(
    weekday_data.reset_index(),
    x="weekday",
    y=["apprehensions", "transfers", "discharges"],
    barmode="group",
    title="Average Activity by Recorded Weekday"
)

weekday_fig.update_layout(
    template="plotly_white",
    xaxis_title="Weekday",
    yaxis_title="Average count per observation"
)

st.plotly_chart(
    weekday_fig,
    use_container_width=True
)

st.warning(
    "Weekday comparisons may be affected by missing reporting dates "
    "and uneven coverage. Saturday has no observations in the "
    "currently cleaned dataset."
)

# =========================================================
# BACKLOG / FLOW IMBALANCE INDICATORS
# =========================================================

st.header("Flow Imbalance Monitoring")

imbalance_fig = go.Figure()

imbalance_fig.add_trace(
    go.Scatter(
        x=filtered["date"],
        y=filtered["cbp_flow_balance"],
        mode="lines",
        name="CBP Intake − Transfers"
    )
)

imbalance_fig.add_trace(
    go.Scatter(
        x=filtered["date"],
        y=filtered["hhs_flow_balance"],
        mode="lines",
        name="Transfers − Discharges"
    )
)

imbalance_fig.add_hline(
    y=0,
    line_dash="dash"
)

imbalance_fig.update_layout(
    title="Daily Flow Balance Indicators",
    xaxis_title="Date",
    yaxis_title="Difference in daily events",
    template="plotly_white"
)

st.plotly_chart(
    imbalance_fig,
    use_container_width=True
)

st.caption(
    "Positive values indicate that daily incoming events exceed "
    "daily outgoing events for the corresponding comparison. "
    "These are flow-balance indicators, not direct measurements "
    "of accumulated backlog."
)

# =========================================================
# ALERT SYSTEM
# =========================================================

if show_alerts:

    st.header("Operational Alert Indicators")

    cbp_alert_count = filtered["cbp_imbalance_alert"].sum()
    hhs_alert_count = filtered["hhs_imbalance_alert"].sum()
    discharge_alert_count = filtered["discharge_drop_alert"].sum()

    a1, a2, a3 = st.columns(3)

    a1.metric(
        "CBP Intake > Transfers",
        f"{cbp_alert_count} observations"
    )

    a2.metric(
        "Transfers > Discharges",
        f"{hhs_alert_count} observations"
    )

    a3.metric(
        "Discharge Drop Signals",
        f"{discharge_alert_count} observations"
    )

    st.subheader("Flagged Records")

    alert_df = filtered[
        filtered["cbp_imbalance_alert"] |
        filtered["hhs_imbalance_alert"] |
        filtered["discharge_drop_alert"]
    ].copy()

    alert_df["alert_type"] = alert_df.apply(
        lambda row: ", ".join(
            [
                label
                for label, condition in [
                    ("CBP imbalance", row["cbp_imbalance_alert"]),
                    ("HHS flow imbalance", row["hhs_imbalance_alert"]),
                    ("Discharge drop", row["discharge_drop_alert"])
                ]
                if condition
            ]
        ),
        axis=1
    )

    st.dataframe(
        alert_df[
            [
                "date",
                "cbp_apprehensions",
                "cbp_transfers",
                "hhs_discharges",
                "cbp_flow_balance",
                "hhs_flow_balance",
                "alert_type"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# DISTRIBUTION
# =========================================================

st.header("Discharge Distribution")

distribution_fig = px.histogram(
    filtered,
    x="hhs_discharges",
    nbins=30,
    title="Distribution of HHS Daily Discharges"
)

distribution_fig.update_layout(
    template="plotly_white",
    xaxis_title="Daily discharges",
    yaxis_title="Frequency"
)

st.plotly_chart(
    distribution_fig,
    use_container_width=True
)

# =========================================================
# CORRELATION
# =========================================================

st.header("Correlation Analysis")

correlation_columns = [
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges"
]

correlation = filtered[correlation_columns].corr()

corr_fig = px.imshow(
    correlation,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Between Pipeline Variables",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1
)

st.plotly_chart(
    corr_fig,
    use_container_width=True
)

# =========================================================
# DATA EXPLORER
# =========================================================

st.header("Data Explorer")

explorer_columns = [
    "date",
    "cbp_apprehensions",
    "cbp_custody",
    "cbp_transfers",
    "hhs_care",
    "hhs_discharges",
    "transfer_efficiency",
    "discharge_effectiveness",
    "cbp_flow_balance",
    "hhs_flow_balance",
    "combined_care_load"
]

st.dataframe(
    filtered[explorer_columns],
    use_container_width=True,
    hide_index=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Analytics Data",
    data=csv_data,
    file_name="care_transition_analytics.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Care Transition Efficiency & Placement Outcome Analytics | "
    "Exploratory and descriptive analytics | "
    "Indicators are not individual-level outcome measures."
)
