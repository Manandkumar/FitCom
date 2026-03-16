# ============================================================
# FitCom - Body Composition Analytics Platform
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar

FILE_NAME = "fitcom_reports.csv"

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="FitCom",
    page_icon="🏋️",
    layout="wide"
)

# ------------------------------------------------------------
# Sidebar Branding
# ------------------------------------------------------------

render_sidebar()

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def calculate_fitness_score(row):

    score = 100

    if row["BMI"] > 25:
        score -= (row["BMI"] - 25) * 2

    if row["BodyFat"] > 20:
        score -= (row["BodyFat"] - 20) * 1.5

    if row["VisceralFat"] > 10:
        score -= (row["VisceralFat"] - 10) * 2

    if row["BodyWater"] < 50:
        score -= (50 - row["BodyWater"]) * 1.5

    return max(0, round(score))


# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

df = None

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)

# ============================================================
# DASHBOARD
# ============================================================

st.title("📊 FitCom Dashboard")

if df is None or df.empty:

    st.info("No reports available yet.")

else:

    # ------------------------------------------------------------
    # Select User
    # ------------------------------------------------------------

    user = st.selectbox(
        "Select User",
        df["Name"].unique()
    )

    user_df = df[df["Name"] == user].sort_values("Date")

    latest = user_df.iloc[-1]

    # ------------------------------------------------------------
    # Profile + Metrics
    # ------------------------------------------------------------

    col1, col2 = st.columns([1,3])

    with col1:

        if "Photo" in latest and pd.notna(latest["Photo"]):

            if os.path.exists(latest["Photo"]):

                st.image(latest["Photo"], width=150)

        st.write(f"**Name:** {latest['Name']}")
        st.write(f"**Date:** {latest['Date']}")

    with col2:

        st.subheader("Latest Body Metrics")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("BMI", latest["BMI"])
        c2.metric("Body Fat %", latest["BodyFat"])
        c3.metric("Muscle Mass", latest["MuscleMass"])
        c4.metric("Visceral Fat", latest["VisceralFat"])

        score = calculate_fitness_score(latest)

        st.subheader("Fitness Score")

        st.progress(score / 100)

        st.metric("Score", f"{score}/100")

    # ------------------------------------------------------------
    # User History
    # ------------------------------------------------------------

    st.subheader("User History")

    st.dataframe(user_df)

    # ------------------------------------------------------------
    # Progress Chart
    # ------------------------------------------------------------

    if len(user_df) > 1:

        st.subheader("Progress Chart")

        st.line_chart(
            user_df.set_index("Date")[["Weight", "BodyFat", "MuscleMass"]]
        )

# ------------------------------------------------------------
# Most Improved Athlete
# ------------------------------------------------------------

st.subheader("🔥 Most Improved Athlete")

improvements = []

for athlete in df["Name"].unique():

    athlete_df = df[df["Name"] == athlete].sort_values("Date")

    if len(athlete_df) > 1:

        start_fat = athlete_df.iloc[0]["BodyFat"]
        end_fat = athlete_df.iloc[-1]["BodyFat"]

        improvement = start_fat - end_fat

        improvements.append({
            "Name": athlete,
            "FatLoss": improvement
        })

if improvements:

    imp_df = pd.DataFrame(improvements)

    best = imp_df.sort_values("FatLoss", ascending=False).iloc[0]

    st.success(
        f"🏆 {best['Name']} improved the most with {round(best['FatLoss'],2)}% body fat reduction."
    )

else:

    st.info("Add multiple reports to calculate improvement.")