# Care Transition Efficiency & Placement Outcome Analytics: An Exploratory Analysis of the Unaccompanied Alien Children Program Dataset

## Abstract

This study presents an exploratory data analytics framework for examining operational indicators associated with the care transition pipeline involving Customs and Border Protection (CBP) and the Department of Health and Human Services (HHS). Using an aggregate dataset containing 720 observations covering January 12, 2023, to December 21, 2025, the study analyzes apprehensions, custody levels, transfers, care population, and discharges. Data preprocessing, feature engineering, statistical analysis, temporal trend analysis, correlation analysis, and operational alert indicators were applied. The study recorded an average transfer indicator of approximately 69.10% and a discharge-to-care indicator of approximately 2.37%. Strong positive associations were observed between apprehensions and CBP custody (0.9506), and between HHS care and discharges (0.9209). A dashboard was developed to support monitoring and visualization of operational indicators. The findings demonstrate the potential of data analytics for monitoring aggregate operational patterns while highlighting data coverage and interpretation limitations.

**Keywords:** Data Analytics, Care Transition, CBP, HHS, Operational Monitoring, Exploratory Data Analysis, Dashboard, Data Visualization.

## 1. Introduction

Data-driven decision-making plays an important role in monitoring complex operational systems involving multiple stages, institutions, and resource requirements. Systems involving intake, custody, transfer, care, and discharge require monitoring of activity levels, flow relationships, and variations over time.

The Unaccompanied Alien Children (UAC) Program involves a transition process in which children encountered by Customs and Border Protection (CBP) are transferred to the care of the Department of Health and Human Services (HHS). Monitoring aggregate operational indicators across these stages can help identify trends, variations, and potential areas requiring further investigation.

This project focuses on the development of an analytics framework for examining the available aggregate operational data. Rather than attempting to predict individual placement outcomes, the study emphasizes descriptive analytics, trend monitoring, relationship analysis, and rule-based operational indicators.

## 2. Problem Statement

Aggregate operational data associated with the care transition process contains information about apprehensions, custody, transfers, care population, and discharges. However, interpreting these variables independently may limit the understanding of broader operational patterns.

The problem addressed in this study is the development of an integrated analytics framework capable of cleaning, organizing, analyzing, and visualizing aggregate care transition data to support the monitoring of operational activity and identify observations that may warrant further examination.

## 3. Objectives

The objectives of the study are:

1. To clean and preprocess the available aggregate operational dataset.
2. To analyze trends in apprehensions, custody, transfers, care population, and discharges.
3. To develop descriptive transition indicators for monitoring operational relationships.
4. To examine correlations between selected operational variables.
5. To identify observations exhibiting potential flow imbalance or discharge variation.
6. To develop an interactive dashboard for analytical visualization and data exploration.

## 4. Dataset Description

The dataset used in this study contains aggregate operational observations associated with the Unaccompanied Alien Children Program.

The original dataset contained 1,170 rows and six columns. Following preprocessing, 720 valid observations were retained.

### 4.1 Dataset Variables

| Variable | Description |
|---|---|
| Date | Recorded observation date |
| Children apprehended and placed in CBP custody | Daily apprehension-related indicator |
| Children in CBP custody | Recorded CBP custody population |
| Children transferred out of CBP custody | Recorded transfer activity |
| Children in HHS Care | Recorded HHS care population |
| Children discharged from HHS Care | Recorded discharge activity |

### 4.2 Dataset Coverage

The cleaned dataset covers January 12, 2023, to December 21, 2025. The dataset contains 720 observations, with an average interval of approximately 1.49 days between observations.

The reporting intervals are not uniformly daily. There are 161 intervals greater than one day, and the maximum observed interval is ten days. Therefore, the dataset is treated as an irregularly sampled aggregate time series.

## 5. Methodology

The methodology consists of data preprocessing, feature engineering, exploratory data analysis, operational indicator development, and dashboard implementation.

### 5.1 Data Cleaning

The original dataset was processed using Python and Pandas. The preprocessing procedure included:

- Removal of completely empty rows.
- Removal of duplicate records.
- Standardization of column names.
- Conversion of date fields into datetime format.
- Conversion of numerical fields into appropriate numeric types.
- Removal of invalid date records.
- Chronological sorting of observations.

After cleaning, 720 observations were retained.

### 5.2 Feature Engineering

Additional analytical variables were created to support monitoring and analysis.

**Transfer Efficiency Indicator**

The transfer efficiency indicator was calculated as:

Transfer Efficiency = CBP Transfers / CBP Custody

The indicator represents the relationship between recorded transfers and CBP custody values for the corresponding observation.

**Discharge Effectiveness Indicator**

Discharge effectiveness was calculated as:

Discharge Effectiveness = HHS Discharges / HHS Care

This indicator describes the relationship between recorded discharges and the HHS care population for the observation.

**Flow Balance Indicators**

Flow balance variables were developed to compare selected operational quantities:

- CBP Flow Balance: Apprehensions minus transfers.
- HHS Flow Balance: Transfers minus discharges.
- Combined Flow Balance: Apprehensions minus discharges.

These are descriptive comparison indicators and are not equivalent to validated backlog or cohort measurements.

**Rolling Indicators**

Rolling averages were calculated across seven observed records to monitor short-term variations in apprehensions, transfers, discharges, CBP custody, and HHS care.

Rolling discharge variability was also calculated to support the development of discharge stability and variation-related indicators.

**Alert Indicators**

Rule-based flags were developed to identify selected flow imbalance patterns and discharge reductions relative to rolling averages. These indicators are intended for exploratory monitoring rather than formal operational risk classification.

### 5.3 Exploratory Data Analysis

Exploratory data analysis was performed using statistical summaries, time-series visualizations, monthly aggregation, weekday analysis, distribution analysis, and correlation matrices.

The analysis was used to identify changes in operational activity, relationships among variables, and potential data patterns requiring further investigation.

### 5.4 Dashboard Development

An interactive dashboard was developed using Streamlit. The dashboard integrates key performance indicators, pipeline comparisons, temporal analysis, correlation visualization, alert summaries, and data exploration.

The dashboard provides an integrated view of selected aggregate operational metrics and allows users to explore the dataset through filters and visualizations.

## 6. Results and Analysis

### 6.1 Overall Operational Statistics

The cleaned dataset contains 720 observations.

| Metric | Total | Mean | Median |
|---|---:|---:|---:|
| CBP Apprehensions | 67,337 | 93.52 | 99 |
| CBP Custody | 123,476 | 171.49 | 193 |
| CBP Transfers | 92,641 | 128.67 | 157 |
| HHS Care | 4,364,118 | 6,061.27 | 6,406.50 |
| HHS Discharges | 124,853 | 173.41 | 181 |

The observed values demonstrate variation across operational indicators. The recorded HHS care population had a substantially larger numerical scale than the CBP custody population. These values represent recorded aggregate observations and should not be interpreted as directly comparable cohort sizes without additional methodological information.

### 6.2 Transition Indicators

The mean transfer efficiency indicator was 0.6910, equivalent to approximately 69.10%, with a median of 70.44%.

The mean discharge effectiveness indicator was 0.0237, equivalent to approximately 2.37%, with a median of 2.63%.

These indicators describe the ratios between selected operational variables. They do not measure the proportion of a specific cohort successfully transferred or discharged, because the dataset does not provide individual-level cohort linkage or matching timestamps.

### 6.3 Correlation Analysis

The correlation analysis identified several strong positive associations.

| Variables | Correlation |
|---|---:|
| CBP Apprehensions and CBP Custody | 0.9506 |
| CBP Custody and CBP Transfers | 0.9250 |
| HHS Care and HHS Discharges | 0.9209 |
| CBP Apprehensions and CBP Transfers | 0.8879 |
| CBP Transfers and HHS Care | 0.7139 |
| CBP Apprehensions and HHS Care | 0.6913 |
| CBP Custody and HHS Care | 0.6637 |
| CBP Transfers and HHS Discharges | 0.6573 |
| CBP Apprehensions and HHS Discharges | 0.6278 |
| CBP Custody and HHS Discharges | 0.6021 |

The strongest association was observed between CBP apprehensions and CBP custody, with a correlation coefficient of 0.9506. CBP custody and transfers also demonstrated a strong positive relationship.

HHS care and discharges exhibited a correlation coefficient of 0.9209. These associations indicate that the selected variables tend to vary together within the dataset. Correlation does not establish causation and may reflect shared temporal patterns, operational relationships, or underlying trends.

### 6.4 Monthly Trends

Monthly analysis identified February 2024 as the month with the highest recorded monthly average for both CBP apprehensions and transfers.

| Indicator | Highest Monthly Average | Lowest Monthly Average |
|---|---|---|
| CBP Apprehensions | February 2024: 225.85 | July 2025: 3.33 |
| CBP Transfers | February 2024: 316.60 | July 2025: 4.19 |
| HHS Discharges | December 2023: 358.11 | November 2025: 8.37 |

A substantial reduction in recorded operational activity is observed in the 2025 data compared with the preceding years.

This change is also visible in the annual averages. However, the dataset does not establish whether this change is attributable to actual operational changes, reporting coverage, dataset characteristics, or other external factors. Consequently, the trend should be interpreted as a change in recorded activity rather than definitive evidence of a real-world decline.

### 6.5 Annual Analysis

The annual averages demonstrate considerable variation across the study period.

| Year | Apprehensions | CBP Custody | Transfers | HHS Care | Discharges |
|---|---:|---:|---:|---:|---:|
| 2023 | 117.63 | 200.47 | 157.06 | 8,646.07 | 288.02 |
| 2024 | 148.07 | 276.90 | 209.37 | 7,042.96 | 205.93 |
| 2025 | 13.03 | 32.91 | 16.59 | 2,542.84 | 28.95 |

The annual comparison highlights a major change in the recorded values during 2025. This finding reinforces the importance of considering reporting consistency, temporal coverage, and contextual information before interpreting aggregate trends.

### 6.6 Operational Alert Analysis

The rule-based alert system identified the following observations:

| Alert Type | Flagged Observations | Percentage |
|---|---:|---:|
| CBP Flow Imbalance | 149 | 20.69% |
| HHS Flow Imbalance | 238 | 33.06% |
| Discharge Drop | 75 | 10.42% |

The HHS flow imbalance indicator flagged the highest number of observations. The discharge drop indicator identified observations in which recorded discharge activity met the defined reduction criterion relative to its rolling reference.

These flags are analytical signals generated using predefined rules. They should not be interpreted as confirmed operational failures or validated risk events.

### 6.7 Reporting Interval Analysis

The reporting interval analysis identified:

- Average interval: 1.49 days.
- Median interval: 1 day.
- Intervals greater than one day: 161.
- Maximum observed gap: 10 days.

The irregular reporting intervals may affect rolling calculations and temporal comparisons. Rolling averages in this study are calculated over seven observations rather than seven calendar days.

## 7. Dashboard Implementation

The developed dashboard integrates the analytical components of the study into a single interactive interface.

The dashboard includes:

- Executive overview of key operational indicators.
- Pipeline activity comparison.
- Time-series monitoring.
- Transfer and discharge