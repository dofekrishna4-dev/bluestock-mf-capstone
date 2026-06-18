import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# DATABASE
# ==================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"


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
            xanchor="center",
            y=0.97,
            font=dict(
                size=24,
                color="white"
            )
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            title=None,
            font=dict(size=14)
        ),

        margin=dict(
            l=40,
            r=40,
            t=120,
            b=60
        ),

        autosize=True,
        height=650,

        hovermode="closest"
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        automargin=True
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