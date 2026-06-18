from utils import *

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Dashboard Overview",
    page_icon="📊",
    layout="wide"
)

load_css()

page_header(
    "📊 Dashboard Overview",
    "Executive overview of Bluestock Mutual Funds"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# DATABASE
# ==========================================================

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

# ==========================================================
# SUMMARY METRICS
# ==========================================================

total_funds = len(funds)
total_categories = funds["category"].nunique()
total_fund_houses = performance["fund_house"].nunique()
avg_return = performance["return_5yr_pct"].mean()
highest_return = performance["return_5yr_pct"].max()
avg_rating = performance["morningstar_rating"].mean()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📊 Executive Summary")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    kpi("📂 Funds", total_funds)

with c2:
    kpi("🏢 Fund Houses", total_fund_houses)

with c3:
    kpi("📁 Categories", total_categories)

with c4:
    kpi("📈 Avg Return", f"{avg_return:.2f}%")

with c5:
    kpi("🏆 Highest Return", f"{highest_return:.2f}%")

st.divider()
# ==========================================================
# CATEGORY DISTRIBUTION
# ==========================================================

category = (
    funds
    .groupby("category")
    .size()
    .reset_index(name="Funds")
)

# ----------------------------------------------------------
# CATEGORY DISTRIBUTION (BAR CHART)
# ----------------------------------------------------------

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

fig.update_layout(

    height=620,

    title=dict(
        text="Number of Mutual Funds by Category",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),

    legend=dict(
        orientation="h",
        y=1.08,
        x=0.5,
        xanchor="center",
        title=""
    ),

    margin=dict(
        t=120,
        l=60,
        r=60,
        b=70
    ),

    xaxis_title="Category",

    yaxis_title="Number of Funds"
)

st.plotly_chart(
    fig,
    use_container_width=True,
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

# ==========================================================
# PORTFOLIO DISTRIBUTION
# ==========================================================

st.subheader("🥧 Portfolio Distribution")

fig2 = px.pie(
    category,
    names="category",
    values="Funds",
    hole=0.60,
    title="Category Share"
)

fig2.update_traces(

    textposition="inside",

    textinfo="percent+label",

    textfont_size=18
)

fig2 = theme(fig2)

fig2.update_layout(

    height=720,

    title=dict(
        text="Category Share",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),

    legend=dict(
        orientation="h",
        y=1.06,
        x=0.5,
        xanchor="center",
        title=""
    ),

    margin=dict(
        t=120,
        l=80,
        r=80,
        b=80
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True,
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
# ==========================================================
# TOP PERFORMING FUNDS
# ==========================================================

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
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# TOP PERFORMING FUNDS CHART
# ==========================================================

fig3 = px.bar(
    top,
    x="scheme_name",
    y="return_5yr_pct",
    color="category",
    text="return_5yr_pct",
    title="Top 10 Mutual Funds by 5-Year Return"
)

fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig3 = theme(fig3)

fig3.update_layout(

    height=650,

    title=dict(
        text="Top 10 Mutual Funds by 5-Year Return",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),

    xaxis_tickangle=-35,

    legend=dict(
        orientation="h",
        y=1.08,
        x=0.5,
        xanchor="center",
        title=""
    ),

    margin=dict(
        t=120,
        l=60,
        r=60,
        b=90
    ),

    xaxis_title="Scheme Name",
    yaxis_title="5-Year Return (%)"
)

st.plotly_chart(
    fig3,
    use_container_width=True,
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

# ==========================================================
# FUND HOUSE ANALYSIS
# ==========================================================

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

fig4.update_layout(

    height=650,

    title=dict(
        text="Number of Funds by Fund House",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),

    margin=dict(
        t=120,
        l=60,
        r=60,
        b=90
    ),

    xaxis_tickangle=-35,

    showlegend=False,

    xaxis_title="Fund House",

    yaxis_title="Total Funds"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
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

# ==========================================================
# CATEGORY RETURN ANALYSIS
# ==========================================================

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

fig5.update_layout(

    title=dict(
        text="Average 5-Year Return by Category",
        x=0.5,
        xanchor="center"
    ),

    showlegend=False,

    margin=dict(
        t=100,
        l=50,
        r=50,
        b=80
    ),

    height=650,

    xaxis_tickangle=-30,

    xaxis_title="Category",

    yaxis_title="Average Return (%)"
)

st.plotly_chart(
    fig5,
    use_container_width=True,
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
# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.subheader("📌 Executive Insights")

left, right = st.columns([2, 1], gap="large")

with left:

    st.info(f"""
### 📊 Portfolio Summary

📂 **Total Mutual Funds:** **{total_funds}**

🏢 **Fund Houses:** **{total_fund_houses}**

📁 **Categories:** **{total_categories}**

📈 **Average 5-Year Return:** **{avg_return:.2f}%**

⭐ **Average Morningstar Rating:** **{avg_rating:.2f}**

🏆 **Highest Return:** **{highest_return:.2f}%**
""")

with right:

    best = performance.loc[
        performance["return_5yr_pct"].idxmax()
    ]

    st.success(f"""
### 🏆 Best Performing Fund

**Scheme Name**

{best['scheme_name']}

---

🏢 **Fund House**

{best['fund_house']}

📁 **Category**

{best['category']}

📈 **5-Year Return**

{best['return_5yr_pct']:.2f}%

⭐ **Morningstar Rating**

{best['morningstar_rating']}

⚖ **Risk Grade**

{best['risk_grade']}
""")

st.divider()

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.subheader("📋 Dashboard Summary")

st.markdown(
"""
This dashboard provides an executive overview of the mutual fund industry through
interactive visualizations and performance analytics.

### Key Highlights

- 📂 Analyze Mutual Fund Categories
- 🏢 Compare Fund Houses
- 📈 Evaluate 5-Year Returns
- ⭐ Morningstar Rating Analysis
- 🏆 Identify Top Performing Funds
- 📊 Interactive Plotly Visualizations
- 💾 SQLite Database Integration
- ⚡ Built with Streamlit & Python
"""
)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
<div style="
text-align:center;
padding:30px;
margin-top:20px;
border-top:1px solid #334155;
color:#94A3B8;
">

<h2 style="color:white;">
📈 Bluestock Mutual Fund Analytics Dashboard
</h2>

<p style="font-size:18px;">
Executive Overview Module
</p>

<p>
Built using
<b>Python</b> •
<b>Streamlit</b> •
<b>Plotly</b> •
<b>SQLite</b>
</p>

<p style="font-size:15px;">
Developed by Krishna Dofe
</p>

</div>
""",
unsafe_allow_html=True
)

st.success("✅ Dashboard Loaded Successfully")