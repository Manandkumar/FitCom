# ============================================================
# FitCom - Athlete Comparison
# Author: Anand Kumar
#
# Notes:
# - Compare latest metrics across multiple athletes
# - Includes bar + radar visualization
# - Age is hidden from UI (privacy)
# ============================================================

import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# -------------------------------------------------------
# Load shared sidebar (consistent UI across app)
# -------------------------------------------------------

from sidebar import render_sidebar
render_sidebar()

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

st.title("🏅 Athlete Comparison")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):

    st.info("No reports available yet.")
    st.stop()

# Load dataset
df = pd.read_csv(FILE_NAME)

# Ensure Date column is proper datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# CLEAN DATA FOR UI
# -------------------------------------------------------
# Remove sensitive fields (Age not shown)

df_display = df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

athletes = sorted(df["Name"].unique())

selected = st.multiselect(
    "Select athletes to compare",
    athletes,
    default=athletes[:2] if len(athletes) >= 2 else athletes
)

# Handle empty selection
if len(selected) == 0:
    st.info("Select at least one athlete.")
    st.stop()

# Filter selected athletes
compare_df = df[df["Name"].isin(selected)]

# -------------------------------------------------------
# GET LATEST RECORD PER ATHLETE
# -------------------------------------------------------
# Important: Always compare latest available data

latest = (
    compare_df
    .sort_values("Date")
    .groupby("Name")
    .tail(1)
    .set_index("Name")
)

# Remove Age from display table
latest_display = latest.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# DISPLAY TABLE
# -------------------------------------------------------

st.subheader("📊 Latest Metrics")
st.dataframe(latest_display, use_container_width=True)

# -------------------------------------------------------
# BAR CHART COMPARISON
# -------------------------------------------------------
# Simple comparison across key metrics

st.subheader("📊 Metric Comparison")

metrics = ["BMI", "BodyFat", "MuscleMass", "BodyWater", "VisceralFat"]

# Handle missing columns safely
available_metrics = [m for m in metrics if m in latest.columns]

if available_metrics:
    st.bar_chart(latest[available_metrics])
else:
    st.warning("No comparable metrics available.")

# -------------------------------------------------------
# RADAR CHART (ADVANCED VISUAL)
# -------------------------------------------------------

st.subheader("🕸️ Body Composition Radar")

fig = go.Figure()

for athlete in latest.index:

    values = []
    labels = []

    # Build dynamically to avoid missing column errors
    for metric in metrics:
        if metric in latest.columns:
            values.append(latest.loc[athlete][metric])
            labels.append(metric)

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        name=athlete
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)