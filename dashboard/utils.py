import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# DATABASE
# ==================================================

DB_PATH = "../data/db/bluestock_mf.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ==================================================
# LOAD CSS
# ==================================================

def load_css():
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ==================================================
# PAGE HEADER
# ==================================================

def page_header(title, subtitle=""):

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.markdown("")


# ==================================================
# KPI CARD
# ==================================================

def kpi(title, value):

    st.metric(
        label=title,
        value=value
    )


# ==================================================
# SECTION TITLE
# ==================================================

def section(title):
    st.subheader(title)


# ==================================================
# PLOTLY THEME
# ==================================================

def theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font=dict(
            family="Segoe UI",
            color="white",
            size=15
        ),

        title=dict(
            x=0.5,
            font=dict(
                size=24,
                color="white"
            )
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=13),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        ),

        height=500,

        hovermode="x unified"
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    return fig


# ==================================================
# ALERT BOXES
# ==================================================

def success(message):
    st.success(message)


def info(message):
    st.info(message)


def warning(message):
    st.warning(message)