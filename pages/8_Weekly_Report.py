import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar

render_sidebar()

FILE_NAME = "fitcom_reports.csv"

st.title("📅 Weekly Fitness Report")

if not os.path.exists(FILE_NAME):
    st.info("No reports available.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# Ensure Date is datetime
df["Date"] = pd.to_datetime(df["Date"])

# Select athlete
user = st.selectbox("Select Athlete", df["Name"].unique())

user_df = df[df["Name"] == user].sort_values("Date")

if len(user_df) < 2:
    st.info("Need at least two reports to generate a weekly report.")
    st.stop()

# Last and previous report
latest = user_df.iloc[-1]
previous = user_df.iloc[-2]

st.subheader("Weekly Progress Summary")

weight_change = latest["Weight"] - previous["Weight"]
fat_change = latest["BodyFat"] - previous["BodyFat"]
muscle_change = latest["MuscleMass"] - previous["MuscleMass"]

col1, col2, col3 = st.columns(3)

col1.metric("Weight Change (kg)", round(weight_change, 2))
col2.metric("Body Fat Change (%)", round(fat_change, 2))
col3.metric("Muscle Mass Change (kg)", round(muscle_change, 2))

st.subheader("AI Weekly Insight")

insight = []

if weight_change < 0:
    insight.append("Great progress! Weight has decreased since last report.")

if fat_change < 0:
    insight.append("Body fat is reducing. Your training and nutrition plan are working.")

if muscle_change > 0:
    insight.append("Muscle mass has increased. Strength training is effective.")

if not insight:
    insight.append("Body composition is stable. Consider adjusting training intensity.")

for tip in insight:
    st.success(tip)

st.subheader("Progress Chart")

chart_df = user_df.set_index("Date")[["Weight", "BodyFat", "MuscleMass"]]

st.line_chart(chart_df)

st.subheader("Download Weekly Report")

csv = user_df.tail(7).to_csv(index=False)

st.download_button(
    "Download Weekly Data",
    data=csv,
    file_name=f"{user}_weekly_report.csv",
    mime="text/csv"
)