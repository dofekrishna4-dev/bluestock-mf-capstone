from utils import *

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(layout="wide")

load_css()

page_header(
    "📈 Mutual Fund Performance Dashboard",
    "Analyze returns, rankings and risk metrics of mutual funds."
)
st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

conn = get_connection()

df = pd.read_sql(
    "SELECT * FROM '07_scheme_performance'",
    conn
)

conn.close()

# --------------------------------------------------
# PERFORMANCE SCORE
# --------------------------------------------------

df["performance_score"] = (
    df["return_5yr_pct"] * 0.35
    + df["return_3yr_pct"] * 0.25
    + df["sharpe_ratio"] * 15
    + df["sortino_ratio"] * 10
    - abs(df["max_drawdown_pct"]) * 0.20
    - df["expense_ratio_pct"] * 5
    + df["morningstar_rating"] * 5
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Performance Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi(
        "📈 Avg 5Y Return",
        f"{df['return_5yr_pct'].mean():.2f}%"
    )

with c2:
    kpi(
        "🏆 Highest Return",
        f"{df['return_5yr_pct'].max():.2f}%"
    )

with c3:
    kpi(
        "⚖ Avg Sharpe",
        f"{df['sharpe_ratio'].mean():.2f}"
    )

with c4:
    kpi(
        "⭐ Avg Performance",
        f"{df['performance_score'].mean():.2f}"
    )

st.divider()

# --------------------------------------------------
# TOP PERFORMING FUNDS
# --------------------------------------------------

st.subheader("🏆 Top 10 Performing Mutual Funds")

top = (
    df.sort_values(
        "performance_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top[
        [
            "scheme_name",
            "fund_house",
            "category",
            "return_5yr_pct",
            "sharpe_ratio",
            "morningstar_rating",
            "performance_score"
        ]
    ],
    width="stretch",
    hide_index=True
)

fig = px.bar(
    top,
    x="scheme_name",
    y="performance_score",
    color="category",
    text="performance_score",
    title="Top 10 Performance Scores"
)

fig.update_layout(
    xaxis_tickangle=-35
)
fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig = theme(fig)
fig.update_yaxes(title="Performance Score")
fig.update_xaxes(title="")

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
# --------------------------------------------------
# LOWEST PERFORMING FUNDS
# --------------------------------------------------

st.subheader("📉 Lowest Performing Funds")

bottom = (
    df.sort_values(
        "performance_score",
        ascending=True
    )
    .head(10)
)

st.dataframe(
    bottom[
        [
            "scheme_name",
            "category",
            "return_5yr_pct",
            "performance_score"
        ]
    ],
    width="stretch",
    hide_index=True
)

st.divider()

# --------------------------------------------------
# RISK VS RETURN
# --------------------------------------------------

st.subheader("⚖ Risk vs Return")

fig2 = px.scatter(
    df,
    x="sharpe_ratio",
    y="return_5yr_pct",
    color="category",
    size="morningstar_rating",
    hover_name="scheme_name",
    hover_data={
        "return_5yr_pct": ":.2f",
        "sharpe_ratio": ":.2f",
        "morningstar_rating": True,
        "category": False,
        "performance_score": ":.2f"
},
    title="Risk vs Return Analysis"
)

fig2 = theme(fig2)
fig2.update_traces(
    marker=dict(
        line=dict(
            width=1,
            color="white"
        )
    )
)
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

# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

st.subheader("📊 Average Return by Category")

category = (
    df.groupby("category")["return_5yr_pct"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    category,
    x="category",
    y="return_5yr_pct",
    color="category",
    text="return_5yr_pct",
    title="Average Return by Category"
)

fig3.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig3 = theme(fig3)
fig3.update_yaxes(title="Average 5-Year Return (%)")
fig3.update_xaxes(title="")

st.plotly_chart(
    fig3,
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

# --------------------------------------------------
# MORNINGSTAR RATING
# --------------------------------------------------

st.subheader("⭐ Morningstar Rating Distribution")

rating = (
    df["morningstar_rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating.columns = [
    "Rating",
    "Funds"
]

fig4 = px.pie(
    rating,
    names="Rating",
    values="Funds",
    hole=0.45,
    title="Morningstar Rating Distribution"
)
fig4.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig4 = theme(fig4)

st.plotly_chart(
    fig4,
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
# --------------------------------------------------
# PERFORMANCE INSIGHTS
# --------------------------------------------------

st.subheader("📌 Performance Insights")

left, right = st.columns(2)

with left:

    st.info(f"""
### 📊 Key Performance Metrics

📈 **Average 5-Year Return:** {df['return_5yr_pct'].mean():.2f}%

🏆 **Highest 5-Year Return:** {df['return_5yr_pct'].max():.2f}%

⚖ **Average Sharpe Ratio:** {df['sharpe_ratio'].mean():.2f}

⭐ **Average Morningstar Rating:** {df['morningstar_rating'].mean():.2f}
""")

with right:

    best = df.loc[
        df["performance_score"].idxmax()
    ]

    st.success(f"""
### 🏆 Best Performing Fund

**Scheme:** {best['scheme_name']}

**Fund House:** {best['fund_house']}

**Category:** {best['category']}

**5-Year Return:** {best['return_5yr_pct']:.2f}%

**Performance Score:** {best['performance_score']:.2f}
""")

st.divider()
st.info(
    """
📌 This dashboard evaluates mutual fund performance using
returns, risk-adjusted metrics, and a custom performance score
to identify the best investment opportunities.
"""
)

st.divider()
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
---
<div style="text-align:center;color:#94A3B8;font-size:14px">

Bluestock Mutual Fund Analytics Dashboard

Performance Analytics Module

Built with Streamlit • Plotly • SQLite

</div>
""",
    unsafe_allow_html=True,
)

st.success("✅ Performance Dashboard Loaded Successfully")