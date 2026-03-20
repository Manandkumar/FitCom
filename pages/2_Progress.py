# ============================================================
# FitCom - Progress Tracking (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports
from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

page_header("Progress Tracking", "Track member fitness journey over time")

# -------------------------------------------------------
# LOAD DATA (DB)
# -------------------------------------------------------

data = load_reports()

if not data:
    st.info("No reports available yet.")
    st.stop()

# Flatten grouped data → DataFrame
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Convert date safely
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop invalid dates
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
# INSIGHT
# -------------------------------------------------------

section("Quick Insight")

card_start()

if len(member_df) > 1:
    prev = member_df.iloc[-2]

    weight_change = latest.get("Weight", 0) - prev.get("Weight", 0)
    fat_change = latest.get("BodyFat", 0) - prev.get("BodyFat", 0)

    st.write(f"Weight Change: **{round(weight_change,2)} kg**")
    st.write(f"Body Fat Change: **{round(fat_change,2)} %**")

    if weight_change < 0:
        st.success("Good progress on weight reduction 💪")
    elif weight_change > 0:
        st.warning("Weight increased. Monitor diet ⚠️")
    else:
        st.info("Weight stable")

else:
    st.info("Not enough data for insights")

card_end()