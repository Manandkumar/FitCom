# ============================================================
# FitCom - Progress Tracking (Final Refactored Version)
# Author: Anand Kumar
#
# Purpose:
# Track member progress over time with clean UI
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

page_header("Progress Tracking", "Track member fitness journey over time")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):
    st.info("No reports available yet.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# Convert date safely
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# MEMBER SELECTION
# -------------------------------------------------------

section("Select Member")

card_start()

members = sorted(df["Name"].dropna().unique())

selected_member = st.selectbox(
    "Choose Member",
    members
)

card_end()

# -------------------------------------------------------
# FILTER DATA
# -------------------------------------------------------

member_df = df[df["Name"] == selected_member].sort_values("Date")

if member_df.empty:
    st.warning("No data found for selected member.")
    st.stop()

# -------------------------------------------------------
# SUMMARY METRICS
# -------------------------------------------------------

section("Latest Snapshot")

latest = member_df.iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    card_start()
    st.metric("Weight (kg)", latest.get("Weight", "NA"))
    card_end()

with col2:
    card_start()
    st.metric("Body Fat (%)", latest.get("BodyFat", "NA"))
    card_end()

with col3:
    card_start()
    st.metric("Muscle Mass (kg)", latest.get("MuscleMass", "NA"))
    card_end()

# -------------------------------------------------------
# HISTORY TABLE
# -------------------------------------------------------

section("Progress History")

card_start()

# Hide less useful columns for readability
display_df = member_df.drop(
    columns=["Photo", "Age"],
    errors="ignore"
)

st.dataframe(display_df, use_container_width=True)

card_end()

# -------------------------------------------------------
# TREND VISUALIZATION
# -------------------------------------------------------

section("Progress Trends")

card_start()

# Allow user to choose metrics dynamically
available_metrics = [
    col for col in [
        "Weight",
        "BodyFat",
        "MuscleMass",
        "BodyWater",
        "VisceralFat"
    ]
    if col in member_df.columns
]

selected_metrics = st.multiselect(
    "Select Metrics to Visualize",
    available_metrics,
    default=["Weight", "BodyFat"]
)

if selected_metrics:
    chart_df = member_df.set_index("Date")[selected_metrics]
    st.line_chart(chart_df)
else:
    st.info("Select at least one metric to display")

card_end()

# -------------------------------------------------------
# INSIGHT (OPTIONAL NICE TOUCH)
# -------------------------------------------------------

section("Quick Insight")

card_start()

if len(member_df) > 1:
    prev = member_df.iloc[-2]

    weight_change = latest["Weight"] - prev["Weight"]
    fat_change = latest["BodyFat"] - prev["BodyFat"]

    st.write(f"Weight Change: **{round(weight_change,2)} kg**")
    st.write(f"Body Fat Change: **{round(fat_change,2)} %**")

    if weight_change < 0:
        st.success("Good progress on weight reduction 💪")
    else:
        st.info("Monitor weight trend")

else:
    st.info("Not enough data for insights")

card_end()