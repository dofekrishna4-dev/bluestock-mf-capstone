from utils import *

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(layout="wide")

load_css()

page_header(
    "📊 Dashboard Overview",
    "Executive overview of Bluestock Mutual Funds"
)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# DATABASE
# -------------------------------------------------------

conn = get_connection()

funds = pd.read_sql(
    "SELECT * FROM '01_fund_master'",
    conn
)

performance = pd.read_sql(
    "SELECT * FROM '07_scheme_performance'",
    conn
)

conn.close()

# -------------------------------------------------------
# SUMMARY
# -------------------------------------------------------

total_funds = len(funds)

total_categories = funds["category"].nunique()

total_fund_houses = performance["fund_house"].nunique()

avg_return = performance["return_5yr_pct"].mean()

highest_return = performance["return_5yr_pct"].max()

avg_rating = performance["morningstar_rating"].mean()

# -------------------------------------------------------
# EXECUTIVE SUMMARY
# -------------------------------------------------------

st.subheader("📊 Executive Summary")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    kpi(
        "📂 Funds",
        total_funds
    )

with c2:
    kpi(
        "🏢 Fund Houses",
        total_fund_houses
    )

with c3:
    kpi(
        "📁 Categories",
        total_categories
    )

with c4:
    kpi(
        "📈 Avg Return",
        f"{avg_return:.2f}%"
    )

with c5:
    kpi(
        "🏆 Highest Return",
        f"{highest_return:.2f}%"
    )

st.divider()

# -------------------------------------------------------
# CATEGORY DISTRIBUTION
# -------------------------------------------------------

left,right = st.columns([2,1])

category = (
    funds
    .groupby("category")
    .size()
    .reset_index(name="Funds")
)

with left:

    st.subheader("📊 Category Distribution")

    fig = px.bar(
        category,
        x="category",
        y="Funds",
        color="category",
        text="Funds",
        title="Number of Mutual Funds by Category"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig = theme(fig)

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

with right:

    st.subheader("🥧 Portfolio Distribution")

    fig2 = px.pie(
        category,
        names="category",
        values="Funds",
        hole=.55,
        title="Category Share"
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
# -------------------------------------------------------
# TOP PERFORMING FUNDS
# -------------------------------------------------------

st.subheader("🏆 Top 10 Performing Mutual Funds")

top = (
    performance
    .sort_values(
        "return_5yr_pct",
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
            "morningstar_rating",
            "risk_grade"
        ]
    ],
    width="stretch",
    hide_index=True
)

fig3 = px.bar(
    top,
    x="scheme_name",
    y="return_5yr_pct",
    color="category",
    text="return_5yr_pct",
    title="Top 10 Mutual Funds by 5-Year Return"
)

fig3.update_layout(
    xaxis_tickangle=-35
)

fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig3 = theme(fig3)

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

# -------------------------------------------------------
# FUND HOUSE ANALYSIS
# -------------------------------------------------------

st.subheader("🏢 Fund House Analysis")

houses = (
    performance
    .groupby("fund_house")
    .size()
    .reset_index(name="Funds")
    .sort_values(
        "Funds",
        ascending=False
    )
)

fig4 = px.bar(
    houses,
    x="fund_house",
    y="Funds",
    color="Funds",
    text="Funds",
    title="Number of Funds by Fund House"
)

fig4.update_traces(
    textposition="outside"
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

# -------------------------------------------------------
# CATEGORY RETURNS
# -------------------------------------------------------

st.subheader("📈 Average Return by Category")

avg_cat = (
    performance
    .groupby("category")["return_5yr_pct"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    avg_cat,
    x="category",
    y="return_5yr_pct",
    color="category",
    text="return_5yr_pct",
    title="Average 5-Year Return by Category"
)

fig5.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig5 = theme(fig5)

st.plotly_chart(
    fig5,
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
# -------------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------------

st.subheader("📌 Executive Insights")

left, right = st.columns([2, 1])

with left:

    st.info(f"""
### 📊 Portfolio Summary

📂 **Total Mutual Funds:** {total_funds}

🏢 **Fund Houses:** {total_fund_houses}

📁 **Categories:** {total_categories}

📈 **Average 5-Year Return:** {avg_return:.2f}%

⭐ **Average Morningstar Rating:** {avg_rating:.2f}

🏆 **Highest Return:** {highest_return:.2f}%
""")

with right:

    best = performance.loc[
        performance["return_5yr_pct"].idxmax()
    ]

    st.success(f"""
### 🏆 Best Performing Fund

**{best['scheme_name']}**

🏢 **Fund House:** {best['fund_house']}

📁 **Category:** {best['category']}

📈 **5-Year Return:** {best['return_5yr_pct']:.2f}%

⭐ **Morningstar Rating:** {best['morningstar_rating']}

⚖ **Risk Grade:** {best['risk_grade']}
""")

st.divider()

# -------------------------------------------------------
# DASHBOARD SUMMARY
# -------------------------------------------------------

st.info(
    """
📌 This dashboard provides an executive overview of mutual fund categories,
fund houses, top-performing schemes, and return trends to support investment
analysis and decision-making.
"""
)

st.divider()

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown(
"""
---
<div style="text-align:center; padding:20px; color:#94A3B8;">

<h4>Bluestock Mutual Fund Analytics Dashboard</h4>

Executive Overview Module

Built with Streamlit • Plotly • SQLite

</div>
""",
unsafe_allow_html=True
)

st.success("✅ Executive Dashboard Loaded Successfully")