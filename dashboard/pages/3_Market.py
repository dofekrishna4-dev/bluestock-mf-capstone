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
    "📈 Market Analytics Dashboard",
    "Analyze mutual fund industry trends, AUM, SIP inflows and benchmark performance."
)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

conn = get_connection()

aum = pd.read_sql(
    "SELECT * FROM '03_aum_by_fund_house'",
    conn
)

sip = pd.read_sql(
    "SELECT * FROM '04_monthly_sip_inflows'",
    conn
)

category = pd.read_sql(
    "SELECT * FROM '05_category_inflows'",
    conn
)

folios = pd.read_sql(
    "SELECT * FROM '06_industry_folio_count'",
    conn
)

benchmark = pd.read_sql(
    "SELECT * FROM '10_benchmark_indices'",
    conn
)

conn.close()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Market Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi(
        "🏦 Fund Houses",
        aum["fund_house"].nunique()
    )

with c2:
    kpi(
        "💰 Total AUM",
        f"{aum['aum_crore'].sum():,.0f} Cr"
    )

with c3:
    kpi(
        "📥 Total SIP",
        f"{sip['sip_inflow_crore'].sum():,.0f} Cr"
    )

with c4:
    kpi(
        "👥 Latest Folios",
        f"{folios['total_folios_crore'].max():.2f} Cr"
    )

st.divider()

# --------------------------------------------------
# TOP FUND HOUSES BY AUM
# --------------------------------------------------

st.subheader("🏦 Top Fund Houses by AUM")

top_aum = (
    aum
    .groupby("fund_house")["aum_crore"]
    .sum()
    .reset_index()
    .sort_values(
        "aum_crore",
        ascending=False
    )
)

fig = px.bar(
    top_aum,
    x="fund_house",
    y="aum_crore",
    color="aum_crore",
    text="aum_crore",
    title="Top Fund Houses by Assets Under Management"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
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

st.divider()
# --------------------------------------------------
# MONTHLY SIP INFLOWS
# --------------------------------------------------

st.subheader("📈 Monthly SIP Inflows")

fig2 = px.line(
    sip,
    x="month",
    y="sip_inflow_crore",
    markers=True,
    title="Monthly SIP Inflows"
)

fig2.update_traces(
    line=dict(width=3)
)

fig2 = theme(fig2)

fig2.update_yaxes(
    title="SIP Inflows (₹ Crore)"
)

fig2.update_xaxes(
    title=""
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
# CATEGORY-WISE NET INFLOWS
# --------------------------------------------------

st.subheader("📊 Category-wise Net Inflows")

fig3 = px.bar(
    category,
    x="category",
    y="net_inflow_crore",
    color="category",
    text="net_inflow_crore",
    title="Net Inflows by Mutual Fund Category"
)

fig3.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig3 = theme(fig3)

fig3.update_yaxes(
    title="Net Inflows (₹ Crore)"
)

fig3.update_xaxes(
    title=""
)

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
# INDUSTRY FOLIO TREND
# --------------------------------------------------

st.subheader("👥 Industry Folio Growth")

fig4 = px.line(
    folios,
    x="month",
    y="total_folios_crore",
    markers=True,
    title="Industry Folio Growth"
)

fig4.update_traces(
    line=dict(width=3)
)

fig4 = theme(fig4)

fig4.update_yaxes(
    title="Total Folios (Crore)"
)

fig4.update_xaxes(
    title=""
)

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
# BENCHMARK PERFORMANCE
# --------------------------------------------------

st.subheader("📉 Benchmark Performance")

fig5 = px.line(
    benchmark,
    x="date",
    y="close_value",
    color="index_name",
    markers=True,
    title="Benchmark Index Performance"
)

fig5.update_traces(
    line=dict(width=3)
)

fig5 = theme(fig5)

fig5.update_yaxes(
    title="Closing Value"
)

fig5.update_xaxes(
    title=""
)

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

# --------------------------------------------------
# MARKET INSIGHTS
# --------------------------------------------------

st.subheader("📌 Market Insights")

left, right = st.columns([2, 1])

with left:

    highest_aum = top_aum.iloc[0]

    st.info(f"""
### 📊 Market Summary

🏦 **Largest Fund House:** {highest_aum['fund_house']}

💰 **Total Industry AUM:** ₹ {aum['aum_crore'].sum():,.0f} Crore

📥 **Total SIP Inflows:** ₹ {sip['sip_inflow_crore'].sum():,.0f} Crore

👥 **Latest Industry Folios:** {folios['total_folios_crore'].max():.2f} Crore
""")

with right:

    latest = (
        benchmark
        .sort_values("date")
        .groupby("index_name")
        .tail(1)
    )

    st.success("### 📈 Latest Benchmark Levels")

    st.dataframe(
        latest[
            [
                "index_name",
                "close_value"
            ]
        ],
        width="stretch",
        hide_index=True
    )

st.divider()

# --------------------------------------------------
# DASHBOARD SUMMARY
# --------------------------------------------------

st.info(
    """
📌 This dashboard provides an overview of mutual fund industry trends,
including Assets Under Management (AUM), SIP inflows, investor folios,
category-wise inflows, and benchmark index performance to support
market analysis and investment decision-making.
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

Market Analytics Module

Built with Streamlit • Plotly • SQLite

</div>
""",
unsafe_allow_html=True,
)

st.success("✅ Market Dashboard Loaded Successfully")