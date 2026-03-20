# ============================================================
# FitCom - Athlete Comparison (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from storage import load_reports
from sidebar import render_sidebar

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()

st.title("🏅 Athlete Comparison")

# -------------------------------------------------------
# LOAD DATA (DB)
# -------------------------------------------------------

data = load_reports()

if not data:
    st.info("No reports available yet.")
    st.stop()

# Flatten DB data
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Ensure Date column is proper datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop invalid dates
df = df.dropna(subset=["Date"])

# -------------------------------------------------------
# CLEAN DATA FOR UI
# -------------------------------------------------------

df_display = df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

athletes = sorted(df["Name"].dropna().unique())

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

st.subheader("📊 Metric Comparison")

metrics = ["BMI", "BodyFat", "MuscleMass", "BodyWater", "VisceralFat"]

available_metrics = [m for m in metrics if m in latest.columns]

if available_metrics:
    st.bar_chart(latest[available_metrics])
else:
    st.warning("No comparable metrics available.")

# -------------------------------------------------------
# RADAR CHART
# -------------------------------------------------------

st.subheader("🕸️ Body Composition Radar")

fig = go.Figure()

for athlete in latest.index:

    values = []
    labels = []

    for metric in metrics:
        if metric in latest.columns:
            val = latest.loc[athlete].get(metric, 0)
            values.append(val if pd.notna(val) else 0)
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