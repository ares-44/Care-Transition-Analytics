# Care Transition Efficiency & Placement Outcome Analytics

An exploratory data analytics project focused on analyzing aggregate operational trends across the Customs and Border Protection (CBP) and Department of Health and Human Services (HHS) stages of the Unaccompanied Alien Children (UAC) Program.

## Overview

This project uses data analytics to examine operational patterns related to apprehensions, custody, transfers, care population, and discharges. It integrates data cleaning, feature engineering, exploratory analysis, operational alert indicators, and an interactive Streamlit dashboard.

## Objectives

- Analyze aggregate CBP and HHS operational data.
- Clean and preprocess the dataset.
- Develop descriptive operational indicators.
- Analyze trends over time.
- Examine correlations between operational variables.
- Identify selected flow imbalance and discharge variation signals.
- Build an interactive dashboard for data exploration.

## Dataset

The dataset covers January 12, 2023, to December 21, 2025.

After preprocessing, the dataset contains 720 observations.

### Variables

- Date
- CBP Apprehensions
- CBP Custody
- CBP Transfers
- HHS Care
- HHS Discharges

## Project Structure

```text
project 2/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── feature_engineering.py
│   ├── eda.py
│   └── analysis_report.py
├── dashboard/
│   └── app.py
├── reports/
│   └── research_paper.md
├── results/
│   ├── figures/
│   ├── analysis_findings.txt
│   ├── monthly_metrics_report.csv
│   ├── yearly_summary.csv
│   ├── eda_summary_statistics.csv
│   ├── monthly_analysis.csv
│   ├── weekday_analysis.csv
│   └── correlation_matrix.csv
└── README.md
```

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Methodology

1. Data inspection
2. Data cleaning and preprocessing
3. Feature engineering
4. Exploratory data analysis
5. Correlation analysis
6. Temporal analysis
7. Operational alert indicators
8. Interactive dashboard development

## Key Analytical Findings

- 720 observations were retained after preprocessing.
- Mean transfer indicator: approximately 69.10%.
- Mean discharge-to-care indicator: approximately 2.37%.
- Apprehensions and CBP custody showed a correlation of 0.9506.
- HHS care and discharges showed a correlation of 0.9209.
- 149 observations were flagged for CBP flow imbalance.
- 238 observations were flagged for HHS flow imbalance.
- 75 observations were flagged for discharge-drop signals.

These indicators are descriptive and should not be interpreted as cohort-level transition probabilities or causal relationships.

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd project-2
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn streamlit
```

### 5. Run the dashboard

```bash
streamlit run dashboard/app.py
```

## Limitations

- The dataset is aggregate rather than individual-level.
- Reporting intervals are irregular.
- The indicators are descriptive.
- Correlation does not imply causation.
- Changes in recorded activity may reflect reporting or operational changes.
- Alert rules have not been independently validated.

## Future Scope

- Cohort-level transition analysis.
- Forecasting of aggregate indicators.
- Advanced anomaly detection.
- Alert validation.
- Calendar-aligned time-series analysis.
- Additional contextual data integration.

## Disclaimer

This project is an exploratory analytics study using aggregate data. It is not intended to establish causal relationships, make individual-level predictions, or independently evaluate policy or operational outcomes.
