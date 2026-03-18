# ============================================================
# FitCom - Athlete Comparison (Final Refactored Version)
# Author: Anand Kumar
#
# Purpose:
# Compare multiple athletes side-by-side using latest data
# ============================================================

import streamlit as st
import pandas as pd
import os

from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

FILE_NAME = "fitcom_reports.csv"

page_header("Athlete Comparison", "Compare fitness metrics side-by-side")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):
    st.info("No reports available yet.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# Ensure date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# SELECT ATHLETES
# -------------------------------------------------------

section("Select Athletes")

card_start()

users = sorted(df["Name"].dropna().unique())

selected_users = st.multiselect(
    "Choose Athletes (2+ recommended)",
    users,
    default=users[:2]
)

card_end()

if len(selected_users) < 1:
    st.warning("Select at least one athlete.")
    st.stop()

# -------------------------------------------------------
# GET LATEST RECORDS
# -------------------------------------------------------

latest_df = (
    df[df["Name"].isin(selected_users)]
    .sort_values("Date")
    .groupby("Name")
    .tail(1)
)

# -------------------------------------------------------
# DISPLAY TABLE (SIDE-BY-SIDE)
# -------------------------------------------------------

section("Comparison Table")

card_start()

# Transpose for better comparison (same as original intent)
comparison_df = latest_df.set_index("Name").T

# Optional: remove less useful fields
comparison_df = comparison_df.drop(
    index=["Photo", "Date"],
    errors="ignore"
)

st.dataframe(comparison_df, use_container_width=True)

card_end()

# -------------------------------------------------------
# VISUAL COMPARISON
# -------------------------------------------------------

section("Visual Comparison")

card_start()

metrics = [
    "Weight",
    "BMI",
    "BodyFat",
    "MuscleMass",
    "BodyWater",
    "VisceralFat"
]

available_metrics = [m for m in metrics if m in latest_df.columns]

selected_metric = st.selectbox(
    "Select Metric",
    available_metrics
)

chart_df = latest_df.set_index("Name")[selected_metric]

st.bar_chart(chart_df)

card_end()

# -------------------------------------------------------
# INSIGHTS (NON-DESTRUCTIVE ADDITION)
# -------------------------------------------------------

section("Quick Insight")

card_start()

if len(selected_users) >= 2:

    best_user = chart_df.idxmin() if selected_metric in ["BMI", "BodyFat", "VisceralFat"] else chart_df.idxmax()

    st.write(f"Best performer for **{selected_metric}**: **{best_user}**")

else:
    st.info("Select multiple athletes for comparison insights")

card_end()