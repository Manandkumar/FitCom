# ============================================================
# FitCom - Progress Tracking (ENHANCED WITH DATE FILTER)
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports
from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT UI
# -------------------------------------------------------

render_sidebar()
apply_theme()

page_header("Progress Tracking", "Track member fitness journey over time")

# -------------------------------------------------------
# LOAD DATA FROM DATABASE
# -------------------------------------------------------
# We always use DB (no CSV anymore)
# load_reports() already excludes soft-deleted records

data = load_reports()

if not data:
    st.info("No reports available yet.")
    st.stop()

# Convert grouped dict → flat dataframe
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Convert Date column safely (important for sorting & filtering)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop invalid or corrupted date rows
df = df.dropna(subset=["Date"])

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
# FILTER DATA FOR SELECTED MEMBER
# -------------------------------------------------------

# Always sort → ensures latest record logic works correctly
member_df = df[df["Name"] == selected_member].sort_values("Date")

if member_df.empty:
    st.warning("No data found for selected member.")
    st.stop()

# -------------------------------------------------------
# 🔥 DATE FILTER (NEW FEATURE)
# -------------------------------------------------------
# Allows viewing:
# 1. Full history
# 2. Specific day snapshot

section("Filter by Date")

card_start()

# Convert dates to string for UI dropdown
date_options = member_df["Date"].dt.strftime("%Y-%m-%d").unique()

selected_date = st.selectbox(
    "Select Date (Optional)",
    ["All"] + sorted(date_options, reverse=True)
)

card_end()

# Apply filter only if user selects a specific date
if selected_date != "All":
    member_df = member_df[
        member_df["Date"].dt.strftime("%Y-%m-%d") == selected_date
    ]

# -------------------------------------------------------
# SUMMARY METRICS
# -------------------------------------------------------
# Always show latest record from filtered data

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
# Clean table view (hide unnecessary columns)

section("Progress History")

card_start()

display_df = member_df.drop(
    columns=["Photo", "Age"],
    errors="ignore"
)

st.dataframe(display_df, use_container_width=True)

card_end()

# -------------------------------------------------------
# TREND VISUALIZATION
# -------------------------------------------------------
# Dynamic metric selection → flexible charts

section("Progress Trends")

card_start()

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
# INSIGHT ENGINE
# -------------------------------------------------------
# Simple but effective trend insight (latest vs previous)

section("Quick Insight")

card_start()

if len(member_df) > 1:

    prev = member_df.iloc[-2]

    weight_change = latest.get("Weight", 0) - prev.get("Weight", 0)
    fat_change = latest.get("BodyFat", 0) - prev.get("BodyFat", 0)

    st.write(f"Weight Change: **{round(weight_change,2)} kg**")
    st.write(f"Body Fat Change: **{round(fat_change,2)} %**")

    # Interpretation logic
    if weight_change < 0:
        st.success("Good progress on weight reduction 💪")
    elif weight_change > 0:
        st.warning("Weight increased. Monitor diet ⚠️")
    else:
        st.info("Weight stable")

else:
    st.info("Not enough data for insights")

card_end()