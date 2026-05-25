# Amazon Financial Intelligence Platform

An interactive financial analytics and forecasting platform built using Python, SQL, Streamlit, and Power BI to analyze Amazon’s financial performance from 2020–2024. The platform combines KPI monitoring, predictive analytics, anomaly detection, and executive business insights into a modular and deployable analytics system.

---

# Features

* Interactive Streamlit dashboard
* Revenue and profitability KPI tracking
* Executive business insight generation
* Revenue forecasting using Linear Regression
* Interactive Plotly visualizations
* Dynamic year-based filtering
* Operating margin analysis
* Cloud revenue contribution analysis
* Modular analytics architecture
* Anomaly detection engine
* SQL-driven financial preprocessing
* Power BI reporting integration

---

# Dashboard Capabilities

## KPI Monitoring

Track:

* Total Revenue
* Net Income
* Operating Income
* Operating Margin
* Year-over-Year Growth

## Predictive Analytics

Forecast future revenue trends using machine learning models and visualize future business performance interactively.

## Executive Insights

Automatically generated business insights summarizing:

* revenue trends
* cloud business growth
* profitability changes
* operational performance

## Interactive Filtering

Users can dynamically filter dashboard visualizations by year using Streamlit sidebar controls.

---

# Tech Stack

| Category         | Technologies        |
| ---------------- | ------------------- |
| Programming      | Python              |
| Data Processing  | Pandas, NumPy       |
| Visualization    | Plotly, Matplotlib  |
| Dashboarding     | Streamlit, Power BI |
| Machine Learning | Scikit-learn        |
| Database         | SQL                 |
| Version Control  | Git, GitHub         |

---

# Project Structure

```bash
Amazon Financial Intelligence/
│
├── data/
│   └── Amazon_raw_data.xlsx
│
├── Python/
│   ├── app.py
│   ├── preprocessing.py
│   ├── forecasting.py
│   ├── kpi_engine.py
│   ├── anomaly_detection.py
│   ├── visualization.py
│   └── requirements.txt
│
├── Screenshots/
│
├── README.md
└── .gitignore
```

---

# Key Engineering Highlights

* Modular architecture with separated analytics layers
* Reusable preprocessing and forecasting pipelines
* Interactive business intelligence dashboard
* Production-style project organization
* Dynamic forecasting and KPI systems
* Scalable financial analytics design

---

# Forecasting Model

The project currently uses:

* Linear Regression forecasting for revenue prediction

Future planned upgrades:

* ARIMA forecasting
* Prophet integration
* XGBoost forecasting
* Multi-company benchmarking

---

# Installation

Clone the repository:

```bash
git clone <your-repository-link>
```

Navigate into the project:

```bash
cd "Amazon Financial Intelligence"
```

Install dependencies:

```bash
pip install -r Python/requirements.txt
```

Run the Streamlit app:

```bash
python -m streamlit run Python/app.py
```

---

# Dashboard Preview

Add dashboard screenshots here from the `Screenshots/` folder.

Recommended screenshots:

* KPI dashboard
* Revenue trend analysis
* Forecasting visualization
* Executive insights section

---

# Deployment

The application is designed for deployment using:

* Streamlit Community Cloud

Deployment-ready architecture includes:

* modular structure
* dependency management
* reusable pipelines
* interactive dashboarding

---

# Future Enhancements

* Multi-company financial benchmarking
* Advanced forecasting models
* Real-time API integration
* AI-generated business summaries
* Financial anomaly alert system
* Comparative industry analytics

---

# Author

Shivaum Shekhar Sharma

Computer Science Engineering (Data Science)
Manipal Institute of Technology, Bengaluru

---
