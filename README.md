# 📈 Bluestock MF Capstone

A Data Engineering and Analytics project built using Python, Pandas, SQLite, SQL, and Jupyter Notebook to analyze Mutual Fund datasets and generate investment insights.

---

# 📌 Project Overview

This project processes multiple mutual fund datasets, stores them in SQLite, performs exploratory data analysis, computes performance metrics, and recommends top-performing mutual funds based on risk and return.

---

# 🛠 Tech Stack

- Python
- Pandas
- SQLite
- SQL
- Matplotlib
- Jupyter Notebook
- Git & GitHub

---

# 📂 Project Structure

```
bluestock_mf_capstone/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│       └── bluestock_mf.db
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── reports/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset

The project uses **10 Mutual Fund datasets**

- Fund Master
- NAV History
- AUM by Fund House
- Monthly SIP Inflows
- Category Inflows
- Industry Folio Count
- Scheme Performance
- Investor Transactions
- Portfolio Holdings
- Benchmark Indices

---

# 🚀 Features

✔ Data Ingestion

✔ Data Cleaning

✔ SQLite Database Creation

✔ SQL Analysis

✔ Exploratory Data Analysis (EDA)

✔ Performance Score Calculation

✔ Mutual Fund Recommendation Engine

✔ Portfolio Analytics

✔ Investment Transaction Analysis

---

# 📈 Performance Score Formula

Performance Score is calculated using:

```
0.35 × 5-Year Return
+0.25 × 3-Year Return
+15 × Sharpe Ratio
+10 × Sortino Ratio
-0.20 × Maximum Drawdown
-5 × Expense Ratio
+5 × Morningstar Rating
```

---

# ▶️ How to Run

Install dependencies

```
pip install -r requirements.txt
```

Run Performance Metrics

```
python scripts/compute_metrics.py
```

Run Recommendation Engine

```
python scripts/recommender.py
```

---

# 📷 Outputs

The project generates

- Performance Rankings
- Category Analysis
- Portfolio Holdings Analysis
- Transaction Analysis
- Mutual Fund Recommendations

---

# 📌 Future Improvements

- Interactive Dashboard
- Live NAV API Integration
- Machine Learning Based Recommendation
- Portfolio Risk Prediction

---

# 👨‍💻 Author

Krishna Dofe

IIT Madras BS Degree in Data Science