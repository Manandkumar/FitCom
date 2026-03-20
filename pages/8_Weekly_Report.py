# ============================================================
# FitCom - Weekly Fitness Report (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports
from sidebar import render_sidebar

render_sidebar()

st.title("📅 Weekly Fitness Report")

# -------------------------------------------------------
# LOAD DATA (DB)
# -------------------------------------------------------

data = load_reports()

if not data:
    st.info("No reports available.")
    st.stop()

# Flatten DB data
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Convert Date column → datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove invalid dates
df = df.dropna(subset=["Date"])

# -------------------------------------------------------
# CLEAN DATA FOR UI
# -------------------------------------------------------

df_display = df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

user = st.selectbox("Select Athlete", sorted(df["Name"].dropna().unique()))

# Filter data
user_df = df[df["Name"] == user].sort_values("Date")

# Need at least 2 entries
if len(user_df) < 2:
    st.info("Need at least two reports to generate a weekly report.")
    st.stop()

# -------------------------------------------------------
# WEEKLY COMPARISON
# -------------------------------------------------------

latest = user_df.iloc[-1]
previous = user_df.iloc[-2]

# Safe calculations
weight_change = latest.get("Weight", 0) - previous.get("Weight", 0)
fat_change = latest.get("BodyFat", 0) - previous.get("BodyFat", 0)
muscle_change = latest.get("MuscleMass", 0) - previous.get("MuscleMass", 0)

# -------------------------------------------------------
# SUMMARY METRICS
# -------------------------------------------------------

st.subheader("📊 Weekly Progress Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Weight Change (kg)", round(weight_change, 2))
col2.metric("Body Fat Change (%)", round(fat_change, 2))
col3.metric("Muscle Mass Change (kg)", round(muscle_change, 2))

# -------------------------------------------------------
# INSIGHTS
# -------------------------------------------------------

st.subheader("🧠 Weekly Insight")

insight = []

# Weight
if weight_change < 0:
    insight.append("🔥 Great progress! Weight has decreased.")
elif weight_change > 0:
    insight.append("⚠️ Weight increased. Review diet and activity.")

# Fat
if fat_change < 0:
    insight.append("💪 Body fat is reducing. Good consistency!")
elif fat_change > 0:
    insight.append("⚠️ Body fat increased. Watch nutrition.")

# Muscle
if muscle_change > 0:
    insight.append("🏋️ Muscle mass increased. Strength training is working.")
elif muscle_change < 0:
    insight.append("⚠️ Muscle loss detected. Increase protein intake.")

# Default
if not insight:
    insight.append("👍 Body composition is stable. Maintain consistency.")

for tip in insight:
    st.success(tip)

# -------------------------------------------------------
# PROGRESS CHART
# -------------------------------------------------------

st.subheader("📈 Progress Trend")

available_cols = [
    col for col in ["Weight", "BodyFat", "MuscleMass"]
    if col in user_df.columns
]

if available_cols:
    chart_df = user_df.set_index("Date")[available_cols]
    st.line_chart(chart_df)
else:
    st.warning("No valid metrics available for chart")

# -------------------------------------------------------
# DOWNLOAD
# -------------------------------------------------------

st.subheader("📥 Download Weekly Report")

weekly_data = user_df.tail(7).drop(columns=["Age"], errors="ignore")

csv = weekly_data.to_csv(index=False)

st.download_button(
    label="Download Weekly Data",
    data=csv,
    file_name=f"{user}_weekly_report.csv",
    mime="text/csv"
)