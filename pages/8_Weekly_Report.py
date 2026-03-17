# ============================================================
# FitCom - Weekly Fitness Report
# Author: Anand Kumar
#
# Notes:
# - Shows week-over-week changes for a selected user
# - Focuses on key metrics: Weight, Body Fat, Muscle Mass
# - Age is hidden from UI for privacy
# ============================================================

import streamlit as st
import pandas as pd
import os

# -------------------------------------------------------
# Load shared sidebar (keeps UI consistent)
# -------------------------------------------------------

from sidebar import render_sidebar
render_sidebar()

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

st.title("📅 Weekly Fitness Report")

# -------------------------------------------------------
# DATA LOADING
# -------------------------------------------------------
# Basic safety check – if no data file, stop early

if not os.path.exists(FILE_NAME):
    st.info("No reports available.")
    st.stop()

# Load dataset
df = pd.read_csv(FILE_NAME)

# Convert Date column → datetime for sorting & charts
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# CLEAN DATA FOR UI
# -------------------------------------------------------
# Remove sensitive / unnecessary fields (Age hidden)

df_display = df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

user = st.selectbox("Select Athlete", sorted(df["Name"].unique()))

# Filter data for selected user
user_df = df[df["Name"] == user].sort_values("Date")

# Safety check – need at least 2 entries for comparison
if len(user_df) < 2:
    st.info("Need at least two reports to generate a weekly report.")
    st.stop()

# -------------------------------------------------------
# WEEKLY COMPARISON LOGIC
# -------------------------------------------------------
# Compare latest vs previous record

latest = user_df.iloc[-1]
previous = user_df.iloc[-2]

weight_change = latest["Weight"] - previous["Weight"]
fat_change = latest["BodyFat"] - previous["BodyFat"]
muscle_change = latest["MuscleMass"] - previous["MuscleMass"]

# -------------------------------------------------------
# SUMMARY METRICS
# -------------------------------------------------------

st.subheader("📊 Weekly Progress Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Weight Change (kg)", round(weight_change, 2))
col2.metric("Body Fat Change (%)", round(fat_change, 2))
col3.metric("Muscle Mass Change (kg)", round(muscle_change, 2))

# -------------------------------------------------------
# AI-LIKE INSIGHTS (RULE-BASED FOR NOW)
# -------------------------------------------------------

st.subheader("🧠 Weekly Insight")

insight = []

# Weight trend
if weight_change < 0:
    insight.append("🔥 Great progress! Weight has decreased.")

elif weight_change > 0:
    insight.append("⚠️ Weight increased. Review diet and activity.")

# Body fat trend
if fat_change < 0:
    insight.append("💪 Body fat is reducing. Good consistency!")

elif fat_change > 0:
    insight.append("⚠️ Body fat increased. Watch nutrition.")

# Muscle trend
if muscle_change > 0:
    insight.append("🏋️ Muscle mass increased. Strength training is working.")

elif muscle_change < 0:
    insight.append("⚠️ Muscle loss detected. Increase protein intake.")

# Fallback
if not insight:
    insight.append("👍 Body composition is stable. Maintain consistency.")

# Display insights
for tip in insight:
    st.success(tip)

# -------------------------------------------------------
# PROGRESS CHART
# -------------------------------------------------------
# Shows trend over time

st.subheader("📈 Progress Trend")

chart_df = user_df.set_index("Date")[["Weight", "BodyFat", "MuscleMass"]]

st.line_chart(chart_df)

# -------------------------------------------------------
# DOWNLOAD SECTION
# -------------------------------------------------------
# Export last 7 entries as CSV

st.subheader("📥 Download Weekly Report")

weekly_data = user_df.tail(7).drop(columns=["Age"], errors="ignore")

csv = weekly_data.to_csv(index=False)

st.download_button(
    label="Download Weekly Data",
    data=csv,
    file_name=f"{user}_weekly_report.csv",
    mime="text/csv"
)