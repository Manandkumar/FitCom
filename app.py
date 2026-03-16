# ============================================================
# FitCom - Body Composition Analytics Platform
# Author: Anand Kumar
#
# Description:
# FitCom is a body composition analytics dashboard that allows
# users to enter fitness metrics, track progress, compare
# performance with others, and receive AI-driven health insights.
#
# Core Features
# -------------
# • Body metrics entry form
# • Automatic BMI calculation
# • Health indicator status (Green / Orange / Red)
# • User progress tracking
# • Global comparison across participants
# • Fitness score calculation
# • Leaderboard ranking
#
# Developed by: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Local module responsible for saving reports
from storage import save_report


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

# Configure Streamlit page settings
st.set_page_config(
    page_title="FitCom",
    layout="wide"
)


# ------------------------------------------------------------
# Application Header
# ------------------------------------------------------------

st.title("🏋️ FitCom - Body Composition Dashboard")

st.write(
    "Track body composition metrics, monitor fitness progress, "
    "and compare performance with others."
)


# ------------------------------------------------------------
# Utility Function: Health Status Indicator
# ------------------------------------------------------------
# Returns a colored status icon based on metric value.
#
# Green  -> Healthy range
# Orange -> Moderate attention required
# Red    -> Outside healthy range
# ------------------------------------------------------------

def status_dot(value, green_range, orange_range):

    if value is None:
        return ""

    if green_range[0] <= value <= green_range[1]:
        return "🟢"

    elif orange_range[0] <= value <= orange_range[1]:
        return "🟠"

    else:
        return "🔴"


# ------------------------------------------------------------
# Utility Function: BMI Calculation
# ------------------------------------------------------------
# BMI Formula:
# BMI = Weight(kg) / Height(m)^2
#
# Height is entered in inches and converted to meters.
# ------------------------------------------------------------

def calculate_bmi(weight, height_in):

    if height_in == 0:
        return None

    height_m = height_in * 0.0254

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# ------------------------------------------------------------
# Utility Function: Fitness Score Calculation
# ------------------------------------------------------------
# A simple scoring model based on:
# • BMI
# • Body Fat %
# • Visceral Fat
# • Body Water %
#
# Score ranges between 0 and 100.
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
# User Input Section
# ------------------------------------------------------------

st.subheader("👤 Enter Body Metrics")

with st.form("entry_form"):

    col1, col2, col3 = st.columns(3)

    # Basic user details
    with col1:
        name = st.text_input("Name *")

    with col2:
        age = st.number_input("Age", 10, 100)

    with col3:
        height = st.number_input("Height (inches)", 48, 90)

    st.divider()

    # Body composition metrics
    col1, col2, col3 = st.columns(3)

    with col1:

        weight = st.number_input("Weight (kg)", 30.0, 200.0)

        # Automatically calculate BMI
        bmi_auto = calculate_bmi(weight, height)

        bmi = st.number_input(
            "BMI (auto calculated)",
            value=float(bmi_auto) if bmi_auto else 0.0
        )

        bodyfat = st.number_input("Body Fat (%)", 1.0, 60.0)

    with col2:

        muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)

        skeletal_muscle = st.number_input("Skeletal Muscle (%)", 10.0, 80.0)

        bone_mass = st.number_input("Bone Mass (kg)", 1.0, 10.0)

    with col3:

        body_water = st.number_input("Body Water (%)", 1.0, 80.0)

        visceral_fat = st.number_input("Visceral Fat", 1.0, 50.0)

        bmr = st.number_input("BMR", 800.0, 4000.0)

    submitted = st.form_submit_button("Save Report")


# ------------------------------------------------------------
# Save Report
# ------------------------------------------------------------

if submitted:

    if not name:

        st.error("Name is mandatory")

    else:

        report_date = datetime.now().strftime("%Y-%m-%d")

        metrics = {
            "Name": name,
            "Date": report_date,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BodyFat": bodyfat,
            "MuscleMass": muscle_mass,
            "SkeletalMuscle": skeletal_muscle,
            "BoneMass": bone_mass,
            "BodyWater": body_water,
            "VisceralFat": visceral_fat,
            "BMR": bmr
        }

        save_report(name, metrics)

        st.success("Report saved successfully!")


# ------------------------------------------------------------
# Load Saved Reports
# ------------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    st.subheader("📊 All Reports")

    st.dataframe(df)


# ------------------------------------------------------------
# Progress Tracking
# ------------------------------------------------------------

    st.subheader("📈 Progress Tracking")

    users = df["Name"].unique()

    selected_user = st.selectbox("Select User", users)

    user_df = df[df["Name"] == selected_user].sort_values("Date")

    if len(user_df) > 1:

        chart_df = user_df.set_index("Date")[["Weight","BodyFat","MuscleMass"]]

        st.line_chart(chart_df)

    else:

        st.info("Add more reports to see progress trend.")


# ------------------------------------------------------------
# Health Status Overview
# ------------------------------------------------------------

    st.subheader("🟢 Health Status")

    latest = user_df.iloc[-1]

    st.write(
        "BMI:",
        latest["BMI"],
        status_dot(latest["BMI"], (18.5,24.9),(25,29.9))
    )

    st.write(
        "Body Fat:",
        latest["BodyFat"],
        status_dot(latest["BodyFat"], (10,20),(21,25))
    )

    st.write(
        "Visceral Fat:",
        latest["VisceralFat"],
        status_dot(latest["VisceralFat"], (1,9),(10,14))
    )


# ------------------------------------------------------------
# Global Comparison
# ------------------------------------------------------------

    st.subheader("⚖️ FitCom Global Comparison")

    if len(df) > 1:

        numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
        numeric_cols = [c for c in numeric_cols if c not in ["Age","Height"]]

        comparison_results = []

        for metric in numeric_cols:

            best_idx = df[metric].idxmax()
            worst_idx = df[metric].idxmin()

            comparison_results.append({
                "Metric": metric,
                "Best Performer": df.loc[best_idx]["Name"],
                "Best Value": df.loc[best_idx][metric],
                "Lowest Performer": df.loc[worst_idx]["Name"],
                "Lowest Value": df.loc[worst_idx][metric]
            })

        comparison_df = pd.DataFrame(comparison_results)

        st.dataframe(comparison_df)