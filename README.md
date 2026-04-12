

# ⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**A comprehensive data analytics & machine learning system analyzing 10 years of Toronto Island Ferry operations (2015–2026)**

**operations (2015–2026)**

🚀 [Live Dashboard](https://ferry-analytics-i2sepxvk8ppeubc5erb6pq.streamlit.app/) · 📊 [Dataset](https://open.toronto.ca/dataset/toronto-island-ferry-ticket-counts/) · 📄 [Report](https://github.com/user-attachments/files/26655786/ferry_analytics_report.docx)


---

</div>

## 📌 Project Overview

Ferries operating from **Jack Layton Ferry Terminal** provide year-round transportation to Centre Island, Hanlan's Point, and Ward's Island. Despite rich ticket sales and redemption data being available, ferry operations lacked a structured analytical framework.

This project delivers a **pure operational analytics perspective** — enabling transportation authorities to move from static scheduling toward **data-informed efficiency optimization**.

---

## 🎯 Problem Statement

> Ferry operations lack a structured framework to:
> - 📈 Measure capacity utilization patterns
> - ⚠️ Identify over-utilization and under-utilization windows
> - 💸 Quantify operational inefficiencies during off-peak periods
> - 🧠 Support evidence-based resource allocation decisions

---

## 🏆 Key Findings

| Insight | Value |
|---|---|
| 📊 Total Records Analyzed | 268,195 intervals |
| 🌞 Peak Season | Summer (3x above average) |
| 🔴 Congestion Rate | 25.0% of all intervals |
| 💤 Idle Rate | 23.9% of all intervals |
| 📅 Busiest Day | Saturday & Sunday (10am–4pm) |
| 📉 COVID Impact | Visible dip in 2020 operations |
| 🤖 ML Model R² Score | Random Forest (best performer) |

---

## 📂 Project Structure

```
ferry_analytics/
│
├── 📁 data/
│   ├── ferry_data.csv              ← Raw dataset (Toronto Open Data)
│   ├── ferry_processed.csv         ← Cleaned & feature-engineered data
│   ├── ferry_daily_ml.csv          ← Daily aggregated ML dataset
│   ├── heatmap.png                 ← Hour vs Day activity heatmap
│   ├── kpi_dashboard.png           ← KPI summary visual
│   ├── ml_predictions.png          ← Actual vs Predicted chart
│   ├── seasonal_analysis.png       ← Seasonal breakdown
│   └── yearly_trends.png           ← Year-over-year trends
│
├── 📁 notebooks/
│   └── analysis.ipynb              ← Full EDA + ML notebook
│
├── app.py                          ← Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🔬 Analytical Methodology

### 1️⃣ Data Ingestion & Structuring
- Loaded 10 years of 15-minute interval ticket data (2015–2026)
- Converted timestamps to datetime objects
- Aggregated to multiple resolutions: 15-min, Hourly, Daily

### 2️⃣ Feature Engineering
| Feature | Formula | Purpose |
|---|---|---|
| `Total_Activity` | Sales + Redemption Count | Overall load measure |
| `Redemption_Pressure_Ratio` | Redemption / (Sales + 1) | Boarding pressure |
| `Operational_Load_Index` | Normalized Total Activity | Interval-level pressure |
| `Is_Idle` | Activity < 25th percentile | Under-utilization flag |
| `Is_Congested` | Activity > 75th percentile | Over-utilization flag |

### 3️⃣ KPI Dashboard
| KPI | Description |
|---|---|
| Capacity Utilization Ratio | Measure of ferry load efficiency |
| Congestion Pressure Index | Identifies over-utilized intervals |
| Idle Capacity Percentage | Measures under-utilization |
| Peak Strain Duration | Length of sustained high-pressure periods |
| Operational Variability Score | Stability of utilization patterns |

### 4️⃣ ML Demand Forecasting
- **Model:** Random Forest Regressor (100 estimators)
- **Baseline:** Linear Regression
- **Features:** Rolling averages, lag features, temporal encodings
- **Top Predictor:** 7-day rolling average (78% importance)
- **Train/Test Split:** 2015–2024 train | Last 365 days test

---

## 📊 Dashboard Features

### 🖥️ Built with Streamlit + Plotly

- **KPI Summary Cards** — Utilization, Congestion, Idle rates at a glance
- **Activity Timeline** — Year-over-year ferry usage trends
- **Seasonal Comparison** — Summer vs Winter operational differences
- **Congestion Heatmap** — Hour × Day activity intensity map
- **Operational Status Pie** — Normal vs Idle vs Congested breakdown
- **ML Forecasting Section** — Actual vs Predicted demand + Feature Importance

### 🎛️ User Controls
- Year & Season filters
- Granularity toggle (15-min / Hourly / Daily)
- Threshold-based visual alerts

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Dashboard
```bash
streamlit run app.py
```

### Run the Notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## 📦 Requirements

```
pandas
numpy
matplotlib
seaborn
plotly
streamlit
scikit-learn
openpyxl
jupyter
```

---

## 💡 Key Insights & Recommendations

1. **🌞 Summer Surge** — Deploy additional ferry capacity from June–August; demand is 3× the annual average
2. **🔴 Weekend Congestion** — Saturday & Sunday 10am–4pm require mandatory capacity expansion
3. **💤 Winter Idle Capacity** — Reduce ferry deployment in December–February to cut operational costs
4. **📉 COVID Recovery** — 2021–2022 showed strong recovery; operations have normalized by 2023
5. **🤖 ML Forecasting** — 7-day rolling average is the strongest demand predictor; use it for weekly scheduling

---

## 🗂️ Data Source

- **Provider:** City of Toronto — Toronto Open Data Portal
- **Dataset:** [Toronto Island Ferry Ticket Counts](https://open.toronto.ca/dataset/toronto-island-ferry-ticket-counts/)
- **Period:** 2015 – 2026
- **Granularity:** 15-minute intervals
- **Columns:** `_id`, `Timestamp`, `Sales Count`, `Redemption Count`

---

## 👨‍💻 Author

**Inderjeet Singh**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/inderjeetsingh4)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/InderjeetSingh4)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

⭐ **If you found this project helpful, please give it a star!** ⭐

*Built as part of Unified Mentor Data Analyst Internship*

</div>
