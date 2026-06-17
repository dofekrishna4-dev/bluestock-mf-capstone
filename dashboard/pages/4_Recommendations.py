from utils import *

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(layout="wide")

load_css()

page_header(
    "🎯 Mutual Fund Recommendation System",
    "Discover the best mutual funds based on performance, risk and ratings."
)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

conn = get_connection()

df = pd.read_sql(
    "SELECT * FROM '07_scheme_performance'",
    conn
)

conn.close()

# ------------------------------------------------
# PERFORMANCE SCORE
# ------------------------------------------------

df["performance_score"] = (
    df["return_5yr_pct"] * 0.35
    + df["return_3yr_pct"] * 0.25
    + df["sharpe_ratio"] * 15
    + df["sortino_ratio"] * 10
    - abs(df["max_drawdown_pct"]) * 0.20
    - df["expense_ratio_pct"] * 5
    + df["morningstar_rating"] * 5
)

# ------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------

st.sidebar.header("🎯 Recommendation Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique())
)

risk = st.sidebar.selectbox(
    "Risk Grade",
    ["All"] + sorted(df["risk_grade"].unique())
)

rating = st.sidebar.slider(
    "Minimum Morningstar Rating",
    1,
    5,
    3
)

# ------------------------------------------------
# FILTER DATA
# ------------------------------------------------

filtered = df.copy()

if category != "All":
    filtered = filtered[
        filtered["category"] == category
    ]

if risk != "All":
    filtered = filtered[
        filtered["risk_grade"] == risk
    ]

filtered = filtered[
    filtered["morningstar_rating"] >= rating
]

recommended = (
    filtered
    .sort_values(
        "performance_score",
        ascending=False
    )
    .head(10)
)

# ------------------------------------------------
# KPI CARDS
# ------------------------------------------------

st.subheader("📊 Recommendation Summary")

c1, c2, c3 = st.columns(3)

with c1:
    kpi(
        "🏆 Recommended Funds",
        len(recommended)
    )

with c2:
    kpi(
        "⭐ Avg Rating",
        f"{recommended['morningstar_rating'].mean():.1f}"
    )

with c3:
    kpi(
        "📈 Avg 5Y Return",
        f"{recommended['return_5yr_pct'].mean():.2f}%"
    )

st.divider()
# ------------------------------------------------
# TOP RECOMMENDATIONS
# ------------------------------------------------

st.subheader("🏆 Top Recommended Mutual Funds")

st.dataframe(
    recommended[
        [
            "scheme_name",
            "fund_house",
            "category",
            "risk_grade",
            "return_5yr_pct",
            "morningstar_rating",
            "performance_score",
        ]
    ],
    width="stretch",
    hide_index=True,
)

# ------------------------------------------------
# PERFORMANCE CHART
# ------------------------------------------------

fig = px.bar(
    recommended,
    x="scheme_name",
    y="performance_score",
    color="category",
    text="performance_score",
    title="Top Recommended Mutual Funds"
)

fig.update_layout(
    xaxis_tickangle=-35
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig = theme(fig)

fig.update_yaxes(
    title="Performance Score"
)

fig.update_xaxes(
    title=""
)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "displaylogo": False,
        "responsive": True,
        "scrollZoom": False,
        "modeBarButtonsToRemove": [
            "lasso2d",
            "select2d"
        ]
    }
)

st.divider()

# ------------------------------------------------
# CATEGORY DISTRIBUTION
# ------------------------------------------------

st.subheader("📊 Recommended Fund Categories")

category_summary = (
    recommended
    .groupby("category")
    .size()
    .reset_index(name="Funds")
)

fig2 = px.pie(
    category_summary,
    names="category",
    values="Funds",
    hole=0.45,
    title="Recommendation Distribution"
)

fig2.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig2 = theme(fig2)

st.plotly_chart(
    fig2,
    width="stretch",
    config={
        "displaylogo": False,
        "responsive": True,
        "scrollZoom": False,
        "modeBarButtonsToRemove": [
            "lasso2d",
            "select2d"
        ]
    }
)

st.divider()

# ------------------------------------------------
# DOWNLOAD CSV
# ------------------------------------------------

csv = recommended.to_csv(index=False).encode()

st.download_button(
    "📥 Download Recommended Funds (CSV)",
    data=csv,
    file_name="recommended_mutual_funds.csv",
    mime="text/csv",
)

st.divider()
# ------------------------------------------------
# RECOMMENDATION INSIGHTS
# ------------------------------------------------

st.subheader("📌 Recommendation Insights")

left, right = st.columns([2, 1])

with left:

    st.info(f"""
### 📊 Recommendation Summary

🏆 **Recommended Funds:** {len(recommended)}

⭐ **Average Rating:** {recommended['morningstar_rating'].mean():.2f}

📈 **Average 5-Year Return:** {recommended['return_5yr_pct'].mean():.2f}%

⚖ **Average Performance Score:** {recommended['performance_score'].mean():.2f}
""")

with right:

    best = recommended.iloc[0]

    st.success(f"""
### 🏆 Best Recommendation

**Scheme:** {best['scheme_name']}

🏢 **Fund House:** {best['fund_house']}

📁 **Category:** {best['category']}

⚖ **Risk Grade:** {best['risk_grade']}

⭐ **Rating:** {best['morningstar_rating']}

📈 **5-Year Return:** {best['return_5yr_pct']:.2f}%

🏆 **Performance Score:** {best['performance_score']:.2f}
""")

st.divider()

# ------------------------------------------------
# DASHBOARD SUMMARY
# ------------------------------------------------

st.info(
    """
📌 This recommendation engine evaluates mutual funds using
historical returns, risk-adjusted performance metrics,
Morningstar ratings, expense ratio, and drawdown analysis to
identify the most suitable investment opportunities.
"""
)

st.divider()

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown(
"""
---
<div style="text-align:center;color:#94A3B8;font-size:14px">

Bluestock Mutual Fund Analytics Dashboard

Recommendation Engine Module

Built with Streamlit • Plotly • SQLite

</div>
""",
unsafe_allow_html=True,
)

st.success("✅ Recommendation Engine Loaded Successfully")