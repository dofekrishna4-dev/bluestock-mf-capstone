import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/combo-chart.png",
        width=80
    )

    st.markdown("## Bluestock")
    st.caption("Professional Mutual Fund Analytics")

    st.divider()

    st.markdown("### 📑 Navigation")

    st.markdown("""
📊 **Overview**

📈 **Performance**

🌍 **Market**

🎯 **Recommendations**
""")

    st.divider()

    st.success("🟢 Database Connected")

    st.caption("Version 1.0")

# -----------------------------
# Hero Section
# -----------------------------

st.title("📈 Bluestock Mutual Fund Analytics Dashboard")

st.markdown(
"""
### Professional Investment Analytics Platform

Gain deep insights into mutual fund performance, market trends,
risk analysis and AI-powered recommendations from one dashboard.
"""
)

st.divider()

# -----------------------------
# Feature Cards
# -----------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.info("""
## 📊 Analytics

Executive dashboard with
business insights and KPIs.
""")

with c2:
    st.success("""
## 📈 Performance

Analyze returns, risk,
Sharpe ratio and rankings.
""")

with c3:
    st.warning("""
## 🎯 Recommendations

AI-inspired mutual fund
recommendation engine.
""")

st.divider()

# -----------------------------
# Welcome
# -----------------------------

left, right = st.columns([2,1])

with left:

    st.markdown("""
### Welcome

Use the sidebar to navigate through the dashboard.

You can explore:

- Executive Overview
- Fund Performance
- Market Analytics
- Recommendation Engine

Every page provides interactive charts,
tables and professional analytics.
""")

with right:

    st.metric(
        "Modules",
        "4"
    )

    st.metric(
        "Database",
        "Connected"
    )

    st.metric(
        "Status",
        "Ready"
    )

st.success("🚀 Dashboard Ready")