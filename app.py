# -------------------------------------------------------
# FitCom - AI Fitness Report Analyzer
# Author: Anand Kumar
# -------------------------------------------------------

import streamlit as st
import pandas as pd
import os

from storage import save_report
from comparison_engine import compare_reports
from ai_coach import generate_insights

FILE_NAME = "fitcom_reports.csv"

# -------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------

st.title("🏋️ FitCom - Fitness Report Analyzer")

st.write(
    "Enter your body composition metrics and let **FitCom** analyze and compare performance."
)

# -------------------------------------------------------
# USER ENTRY FORM
# -------------------------------------------------------

st.subheader("👤 Enter Fitness Metrics")

with st.form("fitness_form"):

    name = st.text_input("Name")

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)
        bodyfat = st.number_input("Body Fat (%)", min_value=1.0, max_value=60.0)
        muscle = st.number_input("Muscle Mass (kg)", min_value=10.0, max_value=100.0)

    with col2:
        visceral = st.number_input("Visceral Fat", min_value=1.0, max_value=50.0)
        bmr = st.number_input("BMR", min_value=800.0, max_value=4000.0)
        water = st.number_input("Body Water (%)", min_value=10.0, max_value=80.0)
        protein = st.number_input("Protein (%)", min_value=5.0, max_value=40.0)

    submitted = st.form_submit_button("Save Report")

# -------------------------------------------------------
# VALIDATION
# -------------------------------------------------------

if submitted:

    if not name.strip():

        st.error("Please enter a name.")

    else:

        metrics = {
            "Weight": weight,
            "BMI": bmi,
            "BodyFat": bodyfat,
            "MuscleMass": muscle,
            "VisceralFat": visceral,
            "BMR": bmr,
            "BodyWater": water,
            "Protein": protein
        }

        save_report(name, metrics)

        st.success("Report saved successfully!")

# -------------------------------------------------------
# LOAD SAVED REPORTS
# -------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    st.subheader("📊 All Participant Reports")

    st.dataframe(df)

    # -------------------------------------------------------
    # LEADERBOARD
    # -------------------------------------------------------

    if "BodyFat" in df.columns:

        df_clean = df.dropna(subset=["BodyFat"]).copy()

        df_clean["Score"] = 100 - df_clean["BodyFat"]

        leaderboard = df_clean.sort_values("Score", ascending=False)

        st.subheader("🏆 FitCom Leaderboard")

        st.table(leaderboard[["Name", "BodyFat", "Score"]])

    # -------------------------------------------------------
    # CHART
    # -------------------------------------------------------

    if "Weight" in df.columns and "BodyFat" in df.columns:

        st.subheader("📈 Fitness Comparison")

        chart_df = df.set_index("Name")[["Weight", "BodyFat"]]

        st.bar_chart(chart_df)

    # -------------------------------------------------------
    # PARTICIPANT COMPARISON
    # -------------------------------------------------------

    st.subheader("⚖️ FitCom Participant Comparison")

    comparison = compare_reports(df)

    for metric, data in comparison.items():

        st.write(f"**Metric: {metric}**")

        st.write(
            "🏆 Best:",
            data["best_person"],
            "(",
            data["best_value"],
            ")"
        )

        st.write(
            "⚠️ Lowest:",
            data["worst_person"],
            "(",
            data["worst_value"],
            ")"
        )

        st.write("---")

    # -------------------------------------------------------
    # AI HEALTH COACH
    # -------------------------------------------------------

    st.subheader("🧠 FitCom AI Health Coach")

    insights = generate_insights(df)

    for insight in insights:
        st.write("•", insight)