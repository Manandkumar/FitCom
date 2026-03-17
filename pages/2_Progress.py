# ============================================================
# FitCom - Progress Tracking
# Author: Anand Kumar
#
# Notes:
# - Shows historical progress for a selected user
# - Includes table + trend chart
# - Age is hidden from UI for privacy
# ============================================================

import streamlit as st
import pandas as pd
import os

# -------------------------------------------------------
# Load shared sidebar (consistent layout across app)
# -------------------------------------------------------

from sidebar import render_sidebar
render_sidebar()

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

st.title("📈 Progress Tracking")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):

    st.info("No reports available.")
    st.stop()

# Load dataset
df = pd.read_csv(FILE_NAME)

# Convert Date column → datetime (important for sorting/charting)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# CLEAN DATA FOR UI
# -------------------------------------------------------
# Remove sensitive fields (Age hidden)

df_display = df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

users = sorted(df["Name"].unique())

user = st.selectbox("Select User", users)

# Filter selected user's data
user_df = df[df["Name"] == user].sort_values("Date")

user_display = user_df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# TABLE VIEW
# -------------------------------------------------------

st.subheader("📋 Progress History")

st.dataframe(user_display, use_container_width=True)

# -------------------------------------------------------
# TREND CHART
# -------------------------------------------------------
# Only show if we have enough data points

if len(user_df) > 1:

    st.subheader("📈 Progress Trend")

    # Select only available columns (safe)
    metrics = ["Weight", "BodyFat", "MuscleMass"]
    available_metrics = [m for m in metrics if m in user_df.columns]

    if available_metrics:

        chart_df = user_df.set_index("Date")[available_metrics]

        st.line_chart(chart_df)

    else:
        st.warning("No chartable metrics available.")

else:
    st.info("Add more entries to see progress trends.")